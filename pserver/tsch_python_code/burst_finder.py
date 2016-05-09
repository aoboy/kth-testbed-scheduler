#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,  getopt, getpass
import os.path, time
import numpy as np
import Burst

def burst_finder(recvd_data, no_rows, no_cols):

    link_Burst = Burst()
    burst = np.zeros((1, no_cols), int)
    
    row_idx     = 0
    fb_length   = 0 
    first_burst = 0       
    done_1burst = True

    link_Burst.first_burst_init   = 0
    link_Burst.first_burst_length = 0

    while done_1burst == True:

        if np.sum(recvd_data[row_idx]) + np.sum(burst) == 0:
            if first_burst == 0: #found first  burst
                first_burst = 1
                fb_length = 16
                if row_idx == 0:
                    link_Burst.first_burst_init = 0
                else:
                    link_Burst.first_burst_init = (row_idx*16) -15
            elif first_burst == 1:
                    fb_length = fb_length +16

        if np.sum(recvd_data[row_idx]) + np.sum(burst) > 3:
            if first_burst == 1:
                done_1burst = False
                link_Burst.first_burst_length = fb_length

        if row_idx == no_rows:
            if first_burst == 0:
                done_1burst = False
            elif first_burst == 1:
                done_1burst = False
                link_Burst.first_burst_length = fb_length
        #increment the row number
        row_idx = row_idx + 1

    link_Burst.second_burst_init   = 0
    link_Burst.second_burst_length = 0

    if row_idx < no_rows:
        done_2burst  = True
        second_burst = 0
        sb_length    = 0

        while done_2burst:
            if np.sum(recvd_data[row_idx]) + np.sum(burst) == 0:
                if second_burst == 0: #found first  burst
                    second_burst = 1
                    bb_length = 16
                    if row_idx == 0:
                        link_Burst.second_burst_init = 0
                    else:
                        link_Burst.second_burst_init = (row_idx*16) -15
                elif second_burst == 1:
                        sb_length = sb_length +16

            if np.sum(recvd_data[row_idx]) + np.sum(burst) > 3:
                if second_burst == 1:
                    done_2burst = False
                    link_Burst.second_burst_length = sb_length

            if row_idx == no_rows:
                if second_burst == 0:
                    done_2burst = False
                elif second_burst == 1:
                    done_2burst = False
                    link_Burst.second_burst_length = sb_length
            #increment the row number
            row_idx = row_idx + 1

    return link_Burst