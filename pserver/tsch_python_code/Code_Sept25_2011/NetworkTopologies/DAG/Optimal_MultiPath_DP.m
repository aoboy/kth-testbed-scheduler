function XX = Optimal_MultiPath_DP(tx_node, node_depth, link_data, Rx_Set, link_prob, Rel_Mat, T, DAGdepth)
%% OPTIMAL_MULTIPATH_DP: find the optimal reliability for nultipath
%% scheduling via dynamic programming (DP).

%% find the outgoing links and the corresponding link loss probabilities

links = find(link_data(:,1)== tx_node);

P = link_prob(links);   % link loss probability

Rel_sub_mat = Rel_Mat(Rx_Set,:);


rel_vec     = zeros(1,T);
sched_links = zeros(1,T);
init_sched_time = DAGdepth - node_depth;
for tt = node_depth:T,
    init_sched_time = init_sched_time+1;
    if tt==1,
        tmp_rel = 1.*(1-P);
    else
        tmp_rel = Rel_sub_mat(:,tt-1).*(1-P) + P.*rel_vec(tt-1);
    end
    
    % scheduling decision for the deadline tt
    [rel index] = max(tmp_rel);
    
    rel_vec(tt)             = rel;
    sched_links(init_sched_time) = links(index);
end
XX.rel_vec     = rel_vec;
XX.sched_links = sched_links;

    
    