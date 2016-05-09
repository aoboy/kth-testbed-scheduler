#
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def condProbWindow(data_ref, data_cross, window_size, value, cond_evn):
    ''''''
    no_data     = len(data_ref)
    doneFlag    = False

    scan_index  = 0
    no_tot_evn  = 0
    no_pos_evn  = 0

    while not doneFlag:
        counter = 0        

        for idx in range(0, window_size):
            if (scan_index - idx) >= 0:
                if data_ref[scan_index - idx] == cond_evn:
                    counter = counter + 1

        if counter == window_size:
            no_tot_evn = no_tot_evn + 1
            if data_cross[scan_index] == value:
                no_pos_evn = no_pos_evn + 1

        if (scan_index + 1) == no_data:
            doneFlag = True
        #increment scan_index
        scan_index = scan_index + 1
    #end of the while Loop
    output = 0.0
    if no_tot_evn > 100:
        output = float(no_pos_evn)/no_tot_evn

    return output