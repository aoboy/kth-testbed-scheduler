#include <stdio.h>
#include <stdlib.h>
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

#define DEV_NUM 14
#define BUFSIZE 40

#define MODE_NODE_TX       1
#define MODE_NODE_TX_RECV  2
#define CMD_NODE_ID   "node-id\n\0"

static  char devices[][DEV_NUM]={"/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2",
                             "/dev/ttyUSB3", "/dev/ttyUSB4", "/dev/ttyUSB5",
                             "/dev/ttyUSB6", "/dev/ttyUSB7", "/dev/ttyUSB8",
                             "/dev/ttyUSB9", "/dev/ttyUSB10", "/dev/ttyUSB11",
                             "/dev/ttyUSB12", "/dev/ttyUSB13", "/dev/ttyUSB14"};

/*----------------------------------------------------------------------------*/
void signal_handler(int signum){
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
int main(int argc, char** argv){
    int n_dev, nfound;

    struct termios options;
    fd_set mask, smask;
    int fd;
    speed_t speed = B115200;
    char *speedname = "115200";

    //char *timeformat = NULL;
    unsigned char buf[BUFSIZE];
    unsigned char outfile[BUFSIZE];
    //unsigned char mode = MODE_START_TEXT; //MODE_FILE_REQ
    unsigned char mode = MODE_NODE_TX; //MODE_FILE_REQ

    n_dev = atoi(argv[1]);

    char *device = devices[n_dev];
    

    signal(SIGINT, signal_handler);

    printf("===========================================================\n");
    printf("called by a remote app[cmd ./sconnect %s]\n", device);
    printf("**Connection will be established on the following devices**\n[");
    printf("===========================================================\n");



    fprintf(stderr, "connecting to %s (%s)", device, speedname);

    fd = open(device, O_RDWR | O_NOCTTY | O_NDELAY | O_SYNC);
    if (fd < 0) {
        fprintf(stderr, "error Gonga\n");
        perror(device);
        exit(-1);
    }
    fprintf(stderr, " [OK]\n");

    if (fcntl(fd, F_SETFL, 0) < 0) {
        perror("could not set fcntl");
        exit(-1);
    }

    if (tcgetattr(fd, &options) < 0) {
        perror("could not get options");
        exit(-1);
    }

    /*   fprintf(stderr, "serial options set\n"); */
    cfsetispeed(&options, speed);
    cfsetospeed(&options, speed);
    /* Enable the receiver and set local mode */
    options.c_cflag |= (CLOCAL | CREAD);
    /* Mask the character size bits and turn off (odd) parity */
    options.c_cflag &= ~(CSIZE | PARENB | PARODD);
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


    FD_ZERO(&mask);
    FD_SET(fd, &mask);
    FD_SET(fileno(stdin), &mask);

    int init_request = 0;
    int exit_req_loop = FALSE;

    for (;;) {
        switch (mode) {
            case MODE_NODE_TX:
                if (init_request == 0) {
                    init_request = 1;

                    int l;

                    sleep(1);
                    for (l = 0; CMD_NODE_ID[l] != '\0'; l++) {

                        int nw = write(fd, &CMD_NODE_ID[l], 1);

                        if (nw <= 0) {
                            perror("write");
                            exit(1);
                        } else {
                            fflush(NULL);
                            usleep(6000);
                            //printf("%c", CMD_NODE_ID[l]);
                        }
                    }
                }
                printf("command %s sent\n", CMD_NODE_ID);
		sleep(1);
                mode = MODE_NODE_TX_RECV;
                memset((void*) outfile, (int) '\0', sizeof (outfile));

                break;

        }

        smask = mask;
        nfound = select(FD_SETSIZE, &smask, (fd_set *) 0, (fd_set *) 0,
                (struct timeval *) 0);
        if (nfound < 0) {
            if (errno == EINTR) {
                fprintf(stderr, "interrupted system call\n");
                continue;
            }
            // something is very wrong!
            perror("select");
            exit(1);
        }

        if (FD_ISSET(fd, &smask)) {
            int i, j, n = read(fd, buf, BUFSIZE);
            if (n < 0) {
                perror("could not read");
                exit(-1);
            }

            switch (mode) {

                case MODE_NODE_TX_RECV:

                    for (i = 0; i < n; i++) {
                        if (buf[i] != 'E') {
                            printf("%c", buf[i]);
                        } else {
                            exit_req_loop = TRUE;
                            break;
                        }
                    }
                    if (has_substring(buf, n, "node_tx")) {
                        exit_req_loop = TRUE;
                        printf("node_tx\n");
                        break;
                    }
                    if (has_substring(buf, n, "END")) {
                        exit_req_loop = TRUE;
                        break;
                    }
            }
        } //end of //if(FD_ISSET(fd, &smask))

        if (exit_req_loop) {
            printf("END\n");
            printf("END\n");
            break;
        }
    } //end of request for

    return (EXIT_SUCCESS);
}
