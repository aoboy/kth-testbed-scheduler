function rel_line = SimulatedReliabilityLine(no_links, deadline, max_no_test, link_trace)

% Find the length of the shorter trace file
for ll=1:no_links,
    length_traces(ll) = length(link_trace.link(ll).RxVec);
end
min_trace_length = min(length_traces);


OutputsTests = [];
max_tx_attmpt =  deadline - no_links  + 1;
global_time = 0;
no_test     = 0;
done        = 0; 
while ~done,
    no_test   = no_test+1;
    test_time = 0;
    link      = 0;
    done_test = 0;                % done_test = 1 if link L succeed or one of the links fails 
    while ~done_test,
        global_time = global_time + 1; 
        test_time   = test_time + 1;
        link        = link + 1;
        % find the max number of transmission attempts left for the current link
        if link == test_time,
            tx_attempts_left = max_tx_attmpt;
        else
            tx_attempts_left = max_tx_attmpt - (test_time - link);
        end
%         % randomly pick the starting point in the trace file for the current link
%         start_trace = floor(1 + (length(link_trace)-deadline-1).*rand); 
%         index       = start_trace-1;
        done_link   = 0;
        while ~done_link,
            % successfull transmission
%            index = index +1;
            if link_trace.link(link).RxVec(global_time) == 1,  % In case of success exit from while loop (done_link = 1) without updating 
                done_link = 1;                                 % test_time. The test_time update is performed in the outer loop (line 13).
                if link == no_links,                           % If the current link was the lase one, then the deadline is fulfilled 
                    done_test = 1;                             % (success = 1) and the test ends (done_test = 1).
                    success   = 1;
                end
            end                                
            % failure transmission
            % NOTE the variable tx_attempts_left INCLUDES the current
            % attempt, hence if tx_attempts_left=1 and we have a failure
            % then the packet will not meet the deadline.
            if link_trace.link(link).RxVec(global_time) == 0,  % if the packet is lost and there are transmission attempts left,
                if tx_attempts_left~=1,                        % then update both the test_time and the tx_attempt_left and try again.
                    global_time = global_time + 1;
                    test_time = test_time + 1;
                    tx_attempts_left = tx_attempts_left - 1; 
                elseif tx_attempts_left == 1,                  % if the packet is lost and there are NOT transmission attempts left,  
                    done_test = 1;                             % then the deadline is missed (success = 0) and the test ends (done_test = 1).
                    done_link = 1;
                    success   = 0;
                end
            end
        end
    end
    OutputsTests = [OutputsTests; success];
    
    % EXIT PROCEDURES:
    % case 1: we exceed the maximum number of trials
    if no_test == max_no_test,
        done =1;
    end
    % case 1: we exceed the length of the shortest trace file
    if global_time>= min_trace_length-deadline
        done = 1;
    end
end

%% compute reliability line
% The vector OutputsTests contains 1 for a successful test (deadline met)
% and 0 otherwise. Hence the reliability is:
rel_line = sum(OutputsTests)./length(OutputsTests); 