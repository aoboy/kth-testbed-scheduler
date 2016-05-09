function net_data = LayeredDAG(Max_Nodes, Max_Links, depth)
%% function LayeredDAG: given the number of levels, the number of nodes per
%% level, and the number of link per node, it returns a layered DAG
%% structure.

if Max_Links>Max_Nodes,
    error(sprintf('Each node at level d can have at most as many links as the number of nodes at level d+1'))
end

%% Position of nodes
N = Max_Nodes * (depth-1) + 2; % at level 1 we have only the source node and at level D the destination


Nodes_pos = [];
for dd = 1:(depth+1),
    if dd ==1,
        Nodes_pos = ones(1,Max_Nodes);
        node_counter = 1;
    elseif (dd>1) && (dd < (depth+1)),
        Nodes_pos = [Nodes_pos; (node_counter+1):(node_counter+Max_Nodes)];
        node_counter = node_counter + Max_Nodes;
    elseif dd == (depth+1),
        Nodes_pos = [Nodes_pos; N*ones(1,Max_Nodes)];
    end
end
No_nodes = N;

%% create links
link_data = [];
for dd = 1:depth,
    % find the transmitter and reciver set at depth dd (source is at depth 1)
    if dd ==1,
        tx_set = 1;                     % in this case tx_set contains only the source
        rx_set = Nodes_pos(dd+1,:);
    else
        tx_set = Nodes_pos(dd,:);
        if dd < depth
            rx_set = Nodes_pos(dd+1,:);
        else
            rx_set = Nodes_pos(dd+1,1);  % in this case rx_set contains only the gateway
        end
    end
    
        if dd ==1,
        tx_set = 1;
    else
        tx_set = Nodes_pos(dd,:);
    end
    
    
    % create at most Max_links from any transmitter at depth d to any
    % receiver at depth d+1 (note that the source is at depth 1)
    for nn=1:length(tx_set),
        % the transmitter is node is tx_set(nn)
        for ll = 1:min(Max_Links, length(rx_set)),
            link_data = [link_data; tx_set(nn) rx_set(ll)];
        end
    end
end
No_links = size(link_data,1);


%% create routing structures:
% here we assume the gateway at level 0 and the source at level "depth", so
% we read the Nodes_pos from bottom to top
level = 0;
Paths_NodeOr = N;             % this structure will record the paths in terms of nodes
for dd = 0:depth-1,
    level  = depth+1-dd; % it refers to the level of the receovers in the Nodes_pos structure (rwo number)
    % find the number of receivers and transmitters at depth d and d-1
    % respectively
    if dd==0,
        Rx_nodes = N;                  % only the gateway
        Tx_nodes = Nodes_pos(level-1,:);
        No_rx    = length(Rx_nodes);
        No_tx    = length(Tx_nodes);
    elseif (dd>0) && (dd<depth-1)
        Rx_nodes = Nodes_pos(level,:);
        Tx_nodes = Nodes_pos(level-1,:);
        No_rx    = length(Rx_nodes);
        No_tx    = length(Tx_nodes);
    elseif dd == depth-1,
        Rx_nodes = Nodes_pos(level,:);
        Tx_nodes = Nodes_pos(level-1,1);
        No_rx    = length(Rx_nodes);
        No_tx    = length(Tx_nodes);
    end
    % update routing table
    %No_paths = No_tx.*No_rx;
    No_old_paths     = size(Paths_NodeOr,1);
    Paths_NodeOr_tmp = Paths_NodeOr;
    Paths_NodeOr     = [];
    for tt = 1:No_tx,
        tmp_vec = Tx_nodes(tt).*ones(No_old_paths,1);
        Paths_NodeOr = [Paths_NodeOr; tmp_vec Paths_NodeOr_tmp];
    end
end
No_paths = size(Paths_NodeOr,1);


Paths_LinkOr = [];
for pp = 1:No_paths,
    nodes_in_path = Paths_NodeOr(pp,:);
    links_in_path = [];
    for nn=1:(length(nodes_in_path)-1),
        link = [nodes_in_path(nn) nodes_in_path(nn+1)];
        done       = 0;
        link_index = 0; 
        while ~done,
            link_index = link_index+1;
            if link_data(link_index,:)==link,
                links_in_path = [links_in_path link_index];
                done =1;
            end
        end
    end
    Paths_LinkOr = [Paths_LinkOr; links_in_path];
end

Rmat = zeros(No_links, No_paths);
for pp=1:No_paths,
    link_indeces          = Paths_LinkOr(pp,:);
    Rmat(link_indeces,pp) = 1;
end

    
net_data.No_Nodes  = No_nodes;                 % this number inclused both source (ID=1) and gateway (ID=N)
net_data.No_Links  = No_links;
net_data.depth     = depth;
net_data.Link_data = link_data;
net_data.Link_prob = rand(size(link_data,1),1);
net_data.Nodes_pos = Nodes_pos;
%
net_data.Routing.Rmat         = Rmat;
net_data.Routing.Paths_NodeOr = Paths_NodeOr;
net_data.Routing.Paths_LinkOr = Paths_LinkOr;

                