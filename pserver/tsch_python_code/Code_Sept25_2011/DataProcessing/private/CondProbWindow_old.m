function  output = CondProbWindow (data_vec, window_size, value, cond_evn)
%% CondProbWindow: returns the probability to have a value 1 
%                  conditioned to a series of zeros/ones of lenght
%                  window_size
%
%                  VALUE: is always 1 and corresponds to a successful event
%                  COND_EVN: is either 0 or 1, and represents the conditioning event            
%% Debug lines
% data_vec = round(rand(20,1))'
% window_size = 2;
% value = 1;
% cond_evn = 1;

%% Main body
no_data    = length(data_vec);
done       = 0;
scan_index = 0;
no_tot_evn = 0;
no_pos_evn = 0;
while ~done,
    scan_index = scan_index+1;
    % sliding window step: from the current position X (excluded) check if
    % the values in the positions X-1, X-window_size  
    counter = 0;
    for tt=1:window_size,
        if scan_index-tt>0, % control step since we need to have positive indeces
            if data_vec(scan_index-tt) == cond_evn,
                counter = counter+1;                % count how many time the prevous "Window_size" position
            end                                     % contain the "Value"
        end
    end
    %% Check the next event: 
    if counter == window_size,
        if data_vec(scan_index) == value,
            no_tot_evn = no_tot_evn + 1;
            no_pos_evn = no_pos_evn + 1;
        else
            no_tot_evn = no_tot_evn + 1;
        end
    end
    % Exit procedure
    if scan_index == no_data,
        done = 1;
    end
end

if no_tot_evn>100,
    output = no_pos_evn./no_tot_evn;
else
    output = 0;
end
return;