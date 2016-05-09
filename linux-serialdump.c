#include <stdio.h>
#include <stdlib.h>

//#define __USE_GNU 1


#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <errno.h>
#include <sys/time.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>

#include <signal.h>
#include <time.h>

typedef enum{
    FALSE,
    TRUE
}bool;

#define LIKE_O_DIRECT  040000	/* Direct disk access.	*/

#define BAUDRATE B115200
#define SLIP_END     0300
#define SLIP_ESC     0333
#define SLIP_ESC_END 0334
#define SLIP_ESC_ESC 0335

#define CSNA_INIT 0x01

#define BUFSIZE 40
#define HCOLS 20
#define ICOLS 18

#define MODE_START_DATE	0
#define MODE_DATE	1
#define MODE_START_TEXT	2
#define MODE_TEXT	3
#define MODE_INT	4
#define MODE_HEX	5
#define MODE_SLIP_AUTO	6
#define MODE_SLIP	7
#define MODE_SLIP_HIDE	8

#define MODE_FILE_REQ       10
#define MODE_FILE_RECV      11
#define MODE_DATA_REQ       12
#define MODE_DATA_RECV      13
#define MODE_FLUSH          14
#define MODE_FLUSH_RECV     15

#define MODE_NOTHING 100

static unsigned char rxbuf[2048];

struct devices_list{   
    char*  dev_name;
    struct devices_list *next;
};
/*----------------------------------------------------------------------------*/
struct devices_list *head = NULL;    
/*----------------------------------------------------------------------------*/
void strncopy(char* dest, char* src, int n){
    int i;
    for(i = 0; (src[i] != '\n') && i < n; i++){
        dest[i] = src[i];
    }
}
/*----------------------------------------------------------------------------*/
struct devices_list *create_device( char* device_name){
    struct devices_list *node = malloc(sizeof(struct devices_list));
    if(node != NULL){
        node->dev_name = malloc(strlen(device_name)+1);
        if(node->dev_name != NULL){
            strcpy(node->dev_name, device_name);
            //node->dev_name[strlen(device_name)]='\n';
            node->next = NULL;
            return node;
        }
    }
    return NULL;
}
/*----------------------------------------------------------------------------*/
void insert_device(struct devices_list **node,  char* device_name){
    if(*node == NULL){
        *node = create_device(device_name);
    }else{
        insert_device(&(*node)->next, device_name);
    }
}
/*----------------------------------------------------------------------------*/
void remove_device(struct devices_list *node){
    if(node != NULL){
        remove_device(node->next);
        free(node);
    }
}
/*----------------------------------------------------------------------------*/
void devices_print(struct devices_list *node){
    struct devices_list *p = node;
    
    for(;  p != NULL; p = p->next){
        printf("%s ", p->dev_name);
    }
    printf("]\n");
}
/*----------------------------------------------------------------------------*/
#define DEV_NUM 14
#define CMD_FILE_REQ  "file_name\n\0"
#define CMD_DATA_REQ  "data_request\n\0"
#define CMD_FLUSH     "flush\n\0"
#define CMD_OK        "ok\n\0"

static  char devices[][DEV_NUM]={"/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2",
                             "/dev/ttyUSB3", "/dev/ttyUSB4", "/dev/ttyUSB5",
                             "/dev/ttyUSB6", "/dev/ttyUSB7", "/dev/ttyUSB8",
                             "/dev/ttyUSB9", "/dev/ttyUSB10", "/dev/ttyUSB11",
                             "/dev/ttyUSB12", "/dev/ttyUSB13", "/dev/ttyUSB14"};


/*----------------------------------------------------------------------------*/
void signal_handler(int signum){
     remove_device(head);
     devices_print(head);
     printf("SIGINT issued by user! aborting program....\n");
     exit(signum);
}
/*----------------------------------------------------------------------------*/
bool has_substring(const char* str, int size_1, const char* find){
   int i,j, not_found = 0;
    if(str[0] == '\0' && find[0] == '\0'){
	return TRUE;
    }
    for(i = 0;  i < size_1; i++){
         not_found = 0;
         for(j = 0; find[j] !='\0'; j++){
	    if(str[i+j] != find[j]){
		not_found = TRUE;
		break;
            }
         }
         if(not_found == FALSE){          
           return TRUE;
         }
    }
  return FALSE;
}
/*----------------------------------------------------------------------------*/
bool is_data_correct(FILE* f){
    int n = 0, curr_n = 0, next_n = 0;
    char buf[40];
    FILE* fp = f;
    
    //rewind(fp); //� 
    if(fseek(fp, 0L, SEEK_SET) == 0){
        
        printf("checking data integrity...\n");
        while(fgets(buf, 40, fp) != NULL){
            
            sscanf(buf, "%x", &n);            
            //printf("%s", buf);
            
            if(n != next_n){
                printf("data not correctly received. :(\n");
                return FALSE;
            }else{
                next_n = n + 16;
            }
            //printf("%d %d\n", n, next_n);
        }
        printf("data OK..\n");
                
        return TRUE;
    }else{
        printf("file parse failed..\n");
        return FALSE;
    }
}
/*----------------------------------------------------------------------------*/
int main(int argc, char** argv){
    int n_dev,  k, index;
    
    struct termios options;
    fd_set mask, smask;
    int fd;
    speed_t speed = B115200;
    char *speedname = "115200";
    char *device = devices[0];
    //char *timeformat = NULL;
    unsigned char buf[BUFSIZE], outbuf[HCOLS];
    unsigned char outfile[BUFSIZE];
    //unsigned char mode = MODE_START_TEXT; //MODE_FILE_REQ
    unsigned char mode = MODE_FILE_REQ; //MODE_FILE_REQ
    int nfound, flags = 0, indexFileIn = 0;
    unsigned char lastc = '\0';
    
    static bool exit_req_loop = FALSE;
    FILE* fout=NULL;
    struct devices_list *devices_ptr = NULL;
    
  
    n_dev = atoi(argv[1]);
    
    signal(SIGINT, signal_handler);
    
    
    for(k = 0; k <= n_dev; k++){
        insert_device(&head, devices[k]);
    }
    printf("===========================================================\n");    
    printf("**Connection will be established on the following devices**\n[");
    devices_print(head);  
    printf("===========================================================\n");
    
    devices_ptr = head;
    for( ; devices_ptr != NULL; devices_ptr = devices_ptr->next){
        
        device = devices_ptr->dev_name;
        
        fprintf(stderr, "connecting to %s (%s)\n", device, speedname);
        
        fd = open(device, O_RDWR | O_NOCTTY | O_NDELAY /*| LIKE_O_DIRECT*/ | O_SYNC );

        if (fd < 0) {
            fprintf(stderr, "error: fd < 0\n");
            perror(device);
            exit(-1);
        }        
        printf("device opened correctly..\n");
        if (fcntl(fd, F_SETFL, 0) < 0) {
            perror("could not set fcntl");
            exit(-1);
        }
        printf("fcntl set correctly..\n");
        if (tcgetattr(fd, &options) < 0) {
            perror("could not get options");
            exit(-1);
        }
        
        fprintf(stderr, " [OK ...!]\n");
        
        /*   fprintf(stderr, "serial options set\n"); */
        cfsetispeed(&options, speed);
        cfsetospeed(&options, speed);
        /* Enable the receiver and set local mode */
        options.c_cflag |= (CLOCAL | CREAD);
        /* Mask the character size bits and turn off (odd) parity */
        options.c_cflag &= ~(CSIZE|PARENB|PARODD);
        /* Select 8 data bits */
        options.c_cflag |= CS8;
        
        /* Raw input */
        options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
        /* Raw output */
        options.c_oflag &= ~OPOST;
        
        if (tcsetattr(fd, TCSANOW, &options) < 0) {
            perror("could not set options");
            exit(-1);
        }
        
        printf("OK till here...\n");
        
        FD_ZERO(&mask);
        FD_SET(fd, &mask);
        FD_SET(fileno(stdin), &mask);
        
        index = 0;
        
        
        int init_request = 0;
        exit_req_loop = FALSE;
        
        mode = MODE_FILE_REQ;
        
        for (;;) {
            
            if(mode == MODE_FILE_REQ){
                if(init_request == 0){
                    init_request = 1;
                    
                    int l;
                    
                    //sleep(1);
                    for (l = 0;  CMD_FILE_REQ[l] != '\0'; l++) {
                        
                        int nw = write(fd, &CMD_FILE_REQ[l], 1);
                        
                        if (nw <= 0) {
                            perror("write");
                            exit(1);
                        } else {
                            fflush(NULL);
                            usleep(6000);
                            //printf("%c", CMD_FILE_REQ[l]);
                        }
                    }
                }
                usleep(6000);
                printf("waiting file name...\n");
                indexFileIn = 0;
                mode = MODE_FILE_RECV;
                memset((void*)outfile, (int)'\0', sizeof(outfile));
            }
            
            
            if(mode == MODE_DATA_REQ){
                int l;
                
                //sleep(1);
                for (l = 0;  CMD_DATA_REQ[l] != '\0'; l++) {
                    
                    int nw = write(fd, &CMD_DATA_REQ[l], 1);
                    
                    if (nw <= 0) {
                        perror("write");
                        exit(1);
                    } else {
                        fflush(NULL);
                        usleep(6000);
                        //printf("%c", CMD_DATA_REQ[l]);
                    }
                }
                printf("receiving data\n");               
                mode = MODE_DATA_RECV;
            }
            
            if(mode == MODE_FLUSH){
                int l;
                
                printf("flusing data..\n");
                
                //sleep(1);
                for (l = 0;  CMD_FLUSH[l] != '\0'; l++) {
                    
                    int nw = write(fd, &CMD_FLUSH[l], 1);
                    
                    if (nw <= 0) {
                        perror("write");
                        exit(1);
                    } else {
                        fflush(NULL);
                        usleep(6000);
                        //printf("%c", CMD_DATA_REQ[l]);
                    }
                }
                
                //sleep(0.5);
                mode = MODE_FLUSH_RECV;
            }
            

            smask = mask;
            nfound = select(FD_SETSIZE, &smask, (fd_set *) 0, (fd_set *) 0,
                    (struct timeval *) 0);
            if(nfound < 0) {
                if (errno == EINTR) {
                    fprintf(stderr, "interrupted system call\n");
                    continue;
                }
                // something is very wrong!
                perror("select");
                exit(1);
            }
            
            if(FD_ISSET(fd, &smask)) {
                int i, j, n = read(fd, buf, BUFSIZE);
                if (n < 0) {
                    perror("could not read");
                    printf("error in read\n");
                    exit(-1);
                }
                
                
                if(mode == MODE_FILE_RECV){
                    if(has_substring(buf, n, "node_tx")){
                        exit_req_loop = TRUE;
                        printf("skip node_tx..\n");
                        break;
                    }
                    
                    if(has_substring(buf, n, "r:") &&
                            has_substring(buf, n, ".txt")){
                        printf("filename transfer finished...\n");
                    }
                    for(i = 0; i < n; i++){
                        if(buf[i]== 'r' && buf[i+1]== ':'){
                            
                            strncopy(outfile, &buf[i+2], n-2);
                            printf("filename: %s\n", &buf[i+2]);
                            
                            fout = fopen(outfile, "w+");
                            if(fout == NULL){
                                perror("unable to create file");
                                exit(1);
                            }else{
                                printf("file created....\n");
                                
                                mode = MODE_DATA_REQ;
                                break;
                            }                            
                        }
                    }
                } //end of mode == mode == MODE_FILE_RECV
                
                if(mode == MODE_DATA_RECV){
                    for(i = 0; i < n; i++){
                        if(buf[i] != 'E'){
                            //if(buf[i] != '�'){
                            if(fputc(buf[i], fout) == EOF){
                                perror("error writing to file\n");
                            }
                            //}
                        }else{
                            break;
                        }
                    }
                    if(has_substring(buf, n, "END")){
                        if(is_data_correct(fout)){
                            fclose(fout);
                            printf("data transfer finished...\n");
                            fout = NULL;
                            
                            mode = MODE_FLUSH;
                        }else{
                            rewind(fout);
                            mode = MODE_DATA_REQ;
                        }
                    }
                } //end of mode == MODE_DATA_RECV
                
                if(mode == MODE_FLUSH_RECV){
                    if(has_substring(buf, n, "FLUSH_OK")){
                        exit_req_loop = TRUE;
                        printf("sensor flushed..\n");
                    }
                    break;
                } //mode == MODE_FLUSH_RECV
                
                fflush(stdout);
            } //end of //if(FD_ISSET(fd, &smask))
            
            if(exit_req_loop){
                break;
            }
        } //end of request for
        
        //we must clear all the options so that we can use the same descriptor to
        //to open another device.
        if(close(fd) == 0){
            printf("device correctly closed ..\n");
        }

       
        exit_req_loop = FALSE;
       
        memset(buf, (int)'\0', sizeof(buf));
        memset(outfile, (int)'\0', sizeof(outfile));
        memset(&options, (int)'\0', sizeof(options));
        memset(&mask, (int)'\0', sizeof(mask));
        memset(&smask, (int)'\0', sizeof(smask));
        
    } //end of for(; devices_ptr!= NULL; devices_ptr->next)
    
    //we get rid of the linked list of device names..
    remove_device(head);
    devices_print(head);
    
    return (EXIT_SUCCESS);
}
