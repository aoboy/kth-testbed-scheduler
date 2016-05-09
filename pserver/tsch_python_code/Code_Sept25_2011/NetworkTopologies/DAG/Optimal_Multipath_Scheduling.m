function stats_OMP = Optimal_Multipath_Scheduling(netdata, Link_Prob, deadline)
% 
% OPTIMAL_MULTIPATH_SCHEDULING: finds the reliability of the best multi-path
% ARQ-based routing strategy.

%% Extract network structure

N = netdata.No_Nodes;                 % this number inclused both source (ID=1) and gateway (ID=N)
L = netdata.No_Links;
H = netdata.depth;

Link_data = netdata.Link_data;
Rmat         = netdata.Routing.Rmat;          % No_links x No_paths
Paths_NodeOr = netdata.Routing.Paths_NodeOr;  % No_paths x depth+1
Paths_LinkOr = netdata.Routing.Paths_LinkOr;  % No_paths x depth
Nodes_pos    = netdata.Nodes_pos;             % Nodes position in the graph 

No_paths = size(Rmat,2);
NodesDepth = zeros(N,1);
for hh = 1:size(Nodes_pos,1),
    % find all nodes at level h 
    if hh==1, 
        Nodes_At_hh = 1;
        NodesDepth(Nodes_At_hh)  = H+1-hh; 
    else
        Nodes_At_hh = Nodes_pos(hh,:);
        NodesDepth(Nodes_At_hh)  = H+1-hh;
    end
end

%%  Step 1: starting from the destination, we find teh R_n(T) as the
%%  reliability of the nodes for all deadlines from t=H:T
NodesRelMatrix = zeros(N,deadline);
NodesRelMatrix(N,:)= 1;          % initialize the gateway reliability to 1

for hh=H+1:-1:2,
    % find set of transmitters al depth h-1
    if hh==2
        Tx_nodes_Set = Nodes_pos(hh-1,1);
    else
        Tx_nodes_Set = Nodes_pos(hh-1,:);
    end

    
    for nn=1:length(Tx_nodes_Set),
        tx_node = Tx_nodes_Set(nn);
        depth = NodesDepth(tx_node);
        % find the set of receivers at depth h
        if hh == (H+1),
            Rx_nodes_Set = Nodes_pos(hh,1);
        else 
            Rx_nodes_Set = Nodes_pos(hh,:);
        end
        % use Dynamic programming to estimate the node reliability and the
        % corresponding link schedule for a given deadline
        DP_sol = Optimal_MultiPath_DP(tx_node, depth, Link_data, Rx_nodes_Set, Link_Prob, NodesRelMatrix, deadline, H);
        rel_vec_node  = DP_sol.rel_vec;
        node_schedule = DP_sol.sched_links; 
        
        NodesRelMatrix(tx_node,:)    = DP_sol.rel_vec;
        stats_OMP.node_sched(tx_node).schdeduled_links = DP_sol.sched_links;
    end
    
end
stats_OMP.NodesRelMatrix = NodesRelMatrix;
