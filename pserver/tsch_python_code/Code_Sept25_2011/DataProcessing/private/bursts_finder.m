function xx = bursts_finder(received_pkt_mat, no_rows, no_cols)
% BURSTS_FINDER: finds the first and second burst of losses. It returns 
% their starting point and length. Here a burst is defined as a sequence of 
% at least 16 consecutive packet losses.

% we define burst = zeros(1,16) and compare it with each row os the
% received trace file (matrix of size 640x16). The condition to identify a
% burst is that sum(burst+row)==0
%
% To identigfy the end of the burst we require that at leat 4 packets are
% recovered over 16, i.e. sum(received_pkt_mat(row_index,:) + burst)>3


% min burst definition
burst = zeros(1, no_cols);

% initialization first burst (used if no burst is found)
xx.first_burst.init   = 0;
xx.first_burst.length = 0;

row_index    = 0;
first_burst  = 0;
done_fb      = 0;
while~done_fb
    row_index = row_index + 1;
    if sum(received_pkt_mat(row_index,:) + burst)==0,
        if first_burst == 0,             % found the init of the first burst
            xx.first_burst.init = (row_index*16)-15;
            first_burst = 1;
            fb_length   = 16;
        elseif first_burst == 1,         % found anothe rpiece of the first burst
            fb_length   = fb_length + 16;
        end
    end

    if sum(received_pkt_mat(row_index,:) + burst)>3
        if first_burst == 1,
            done_fb = 1;
            xx.first_burst.length = fb_length;
        end
    end
    if row_index == no_rows,
        if first_burst  == 0,
            done_fb = 1;                         % no burst was found 
        elseif first_burst ==1,
            done_fb = 1;                         % a burst was found and it terminates 
            xx.first_burst.length = fb_length;   % at the end of the trace file
        end
    end
end


%% find second burst:
%initialize
xx.second_burst.init   = 0;
xx.second_burst.length = 0;

if row_index < no_rows
    second_burst = 0;
    done_sb = 0;
    while~done_sb,
        row_index = row_index +1;
        if sum(received_pkt_mat(row_index,:) + burst)==0,
            if second_burst == 0,             % found the init of the first burst
                xx.second_burst.init = (row_index*16)-15;
                second_burst = 1;
                sb_length   = 16;
            elseif second_burst == 1,         % found anothe rpiece of the first burst
                sb_length   = sb_length + 16;
            end
        end

        if sum(received_pkt_mat(row_index,:) + burst)>3
            if second_burst == 1,
                done_sb = 1;
                xx.second_burst.length = sb_length;
            end
        end
        if row_index == no_rows,
            if second_burst  == 0,
                done_sb = 1;                          % no burst was found
            elseif second_burst ==1,
                done_sb = 1;                          % a burst was found and it terminates 
                xx.second_burst.length = sb_length;   % at the end of the trace file
            end
        end
    end
end