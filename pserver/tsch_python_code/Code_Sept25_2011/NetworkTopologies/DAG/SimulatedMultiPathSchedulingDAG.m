function rel_DAG = SimulatedMultiPathSchedulingDAG(netdata, deadline, max_no_test, link_trace, node_schedule)
% (netdata, Link_LossProb, max_deadline, MaxNoTests, SimNewTraceFile)
% Find the length of the shorter trace file

no_links  = netdata.No_Links;
no_nodes  = netdata.No_Nodes;
LinkData  = netdata.Link_data;
GatewayID = no_nodes;
DAGdepth  = size(netdata.Nodes_pos,1)-1;

for ll=1:no_links,
    length_traces(ll) = length(link_trace.link(ll).RxVec);
end
min_trace_length = min(length_traces);

max_tx_attmpt = deadline - netdata.depth + 1;

Nodes_depths       = zeros(no_nodes,1);
for hh=1:netdata.depth+1,
    node_depth = netdata.depth-hh+1;
    if hh==1,                                                  % source
        Nodes_depths(1)       = node_depth;
    elseif hh==netdata.depth+1,
        Nodes_depths(end)=0;            % gateway
    else
        Nodes_depths(netdata.Nodes_pos(hh,:))       = node_depth;
    end
end

% initialize simulation:
OutputsTests  = [];
global_time   = 0;
no_test       = 0;
done          = 0; 
source_node   = 1;
while ~done,
    no_test    = no_test + 1;
    tx_node    = source_node;
    trial_time = 0;
    done_trial = 0;                % done_trial = 1 if link L succeed or one of the links fails 
    while ~done_trial,
        global_time  = global_time + 1; 
        trial_time   = trial_time + 1;
        if trial_time > 1,                % note that after trial_time =1 the while loop gets back at this line iff the packet moved one hop  
            tx_node = rx_node;
        end
        % find the max number of transmission attempts left for the current link


        if (DAGdepth-Nodes_depths(tx_node)+1) == trial_time,
            tx_attempts_left = max_tx_attmpt;
        else
            slot_left = deadline - trial_time + 1;
            dist_from_GW = Nodes_depths(tx_node);
            tx_attempts_left = slot_left - dist_from_GW +1;
        end
%         % randomly pick the starting point in the trace file for the current link
%         start_trace = floor(1 + (length(link_trace)-deadline-1).*rand); 
%         index       = start_trace-1;
        done_TxNode   = 0;
        while ~done_TxNode,
            % successfull transmission
            used_link = node_schedule(tx_node).schdeduled_links(trial_time);
%             fprintf('==========================================================\n')
%             fprintf('trial time = %d, with tx_node = %d using link %d \n', trial_time, tx_node, used_link)
            if used_link == 0
                error(sprintf('Node %d has been scheduled too early', tx_node));
            end
            if link_trace.link(used_link).RxVec(global_time) == 1,  % In case of success exit from while loop (done_TxNode = 1) without updating 
%                fprintf('Transmission was successful \n')
                done_TxNode = 1;                                 % trial_time. The trial_time update is performed in the outer loop (line 13).
                rx_node     = LinkData(used_link,2);
                if rx_node == GatewayID,                       % If the current node is one hop from GW, then the deadline is fulfilled 
                    done_trial = 1;                            % (success = 1) and the test ends (done_trial = 1).
                    success    = 1;
                end
            end                                
            % failure transmission
            % NOTE the variable tx_attempts_left INCLUDES the current
            % attempt, hence if tx_attempts_left=1 and we have a failure
            % then the packet will not meet the deadline.
            if link_trace.link(used_link).RxVec(global_time) == 0,  % if the packet is lost and there are transmission attempts left,
%                   fprintf('Transmission failed \n')
                if tx_attempts_left~=1,                        % then update both the trial_time and the tx_attempt_left and try again.
                    global_time = global_time + 1;
                    trial_time  = trial_time + 1;
                    tx_attempts_left = tx_attempts_left - 1; 
                elseif tx_attempts_left == 1,                  % if the packet is lost and there are NOT transmission attempts left,  
                    done_trial  = 1;                             % then the deadline is missed (success = 0) and the test ends (done_trial = 1).
                    done_TxNode = 1;
                    success     = 0;
                end
            end
%             fprintf('==================  end tx attempt ========================= \n')
%             pause
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
rel_DAG = sum(OutputsTests)./length(OutputsTests); 