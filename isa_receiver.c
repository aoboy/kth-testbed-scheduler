#include "contiki.h"
#include "net/rime.h"
#include "node-id.h"

#include "dev/leds.h"

#define DEBUG 1
#if DEBUG
#include <stdio.h>
#define PRINTF(...) printf(__VA_ARGS__)
#else
#define PRINTF(...)
#endif
/*---------------------------------------------------------------------------*/
/*---------------------------------------------------------------------------*/
PROCESS(isa_receiver_process, "isa_receiver_process");
AUTOSTART_PROCESSES(&isa_receiver_process);
/*---------------------------------------------------------------------------*/
/*---------------------------------------------------------------------------*/
static void leds_set(uint8_t count){
    if(count & LEDS_GREEN){
        leds_on(LEDS_GREEN);
    }else{
        leds_off(LEDS_GREEN);
    }

    if(count & LEDS_YELLOW){
        leds_on(LEDS_YELLOW);
    }else{
        leds_off(LEDS_YELLOW);
    }
    
    if(count & LEDS_RED){
        leds_on(LEDS_RED);
    }else{
        leds_off(LEDS_RED);
    }
}
/*----------------------------------------------------------------------------*/
/*----------------------------------------------------------------------------*/
static const struct broadcast_callbacks broadcast_call = {NULL, NULL};
static struct broadcast_conn broadcast;
/*----------------------------------------------------------------------------*/
PROCESS_THREAD(isa_receiver_process, ev, data) {
    
    static struct etimer et;
    char *command;
    
    PROCESS_EXITHANDLER(broadcast_close(&broadcast);)
            
    PROCESS_BEGIN();
    
    command = data;
    
    broadcast_open(&broadcast, 129, &broadcast_call);

    PRINTF("RTIMER_SECOND: %u, ", RTIMER_SECOND);
    #if CONF_CHANNEL_POOL_SIZE
    PRINTF("N_CHANNELS: %u\n", CONF_CHANNEL_POOL_SIZE);
    #endif
    
    if((command != NULL) && !strcmp(command, "p")){
        PRINTF("Gonga...\n");
    }
    
    while(1) {        
        etimer_set(&et, CLOCK_SECOND);
        PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
        
        packetbuf_copyfrom("gonga\n", sizeof("gonga\n"));
        
        broadcast_send(&broadcast);
        
        PROCESS_YIELD();
    }
    
    PROCESS_END();
}
