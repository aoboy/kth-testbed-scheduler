function new_trace_file = ConditionalPacketDeliveryFunction(trace_file, net_stats, max_win)
%

%% evaluate CPDF
no_links = net_stats.NoLinks;

AllBeta      = [];
AllAvgPrSucc = [];
h_waitbar=waitbar(0, 'Processing data for CPDF and beta-factor...');
for ll=1:no_links,
    if mod(ll,10)==0,
        waitbar(ll/no_links, h_waitbar, sprintf('Processing data for CPDF and beta-factor...<%d%%>', ceil(100*ll/no_links)));
    end;
    
    tmp_data = trace_file.link(ll).RxVec;
    link_PRR = trace_file.link(ll).AvgPrSucc;
    
    link_cpfd    = zeros(2*max_win+1,1);
    link_CW_meas = zeros(2*max_win+1,1);
    link_CW_ind  = zeros(2*max_win+1,1);
    for window = 1:max_win,
        cond_evn0 = 0;              % conditioning event is failure
        cond_evn1 = 1;              % conditioning event is success
        x0 = CondProbWindow(tmp_data, window, 1, cond_evn0);
        x1 = CondProbWindow(tmp_data, window, 1, cond_evn1);
        link_cpfd(max_win+1-window) = x0;
        link_cpfd(max_win+1+window) = x1;
        
        %% compute terms for CW distance
        if x0~=0,
            link_CW_meas(max_win+1-window) = x0; 
            link_CW_ind(max_win+1-window)  = link_PRR;
        end
        if x1~=0,
            link_CW_meas(max_win+1+window) = 1 - x1;
            link_CW_ind(max_win+1+window)  = 1 - link_PRR;
        end
    end
    
    % compute Beta-factor
%     if isempty(mean(link_CW_ind(find(link_CW_ind~=0)))
%     ,
    if any(link_CW_ind),
        term1 = mean(link_CW_ind(find(link_CW_ind~=0)));   % if link_CW_ind has at least a nonzero element, 
                                                           % the average is taken only on the positive elements                                                                                                                      
    else
        term1 = 0;                                         % if all elements of link_CW_ind are zero, the average is zero
    end
    if any(link_CW_meas),
        term2 = mean(link_CW_meas(find(link_CW_meas~=0))); % if link_CW_meas has at least a nonzero element, 
                                                           % the average is taken only on the positive elements                                                                                                                      
    else
        term2 = 0;                                         % if all elements of link_CW_meas are zero, the average is zero
    end

    if (term1 == 0) && (term2 == 0),
        beta_factor = 0;       % this can happen only when I have either all losses or all success
    else 
        beta_factor  = (term1-term2)./term1;   
%         beta_factor  = (mean(link_CW_ind(find(link_CW_ind~=0)))-mean(link_CW_meas(find(link_CW_meas~=0))))./mean(link_CW_ind(find(link_CW_ind~=0)))
    end
            
        
    AllBeta      = [AllBeta; beta_factor];
    AllAvgPrSucc = [AllAvgPrSucc; trace_file.link(ll).AvgPrSucc];

    % store data for the current link
    trace_file.link(ll).BetaFactor      = beta_factor;
    trace_file.link(ll).CPDF            = link_cpfd;
    trace_file.link(ll).CPDF_max_win    = max_win;
    trace_file.link(ll).CWdist          = link_CW_meas;
    trace_file.link(ll).CWdist_ind_link = link_CW_ind;
end
% trace_file.AllBetaFactors = AllBeta;
% trace_file.AllAvgPrSucc   = AllAvgPrSucc;

%% sort the links in decreasing order of success provability
[tmp_AvgPrSucc ind]     = sort(-AllAvgPrSucc);

for ll = 1:no_links
    new_trace_file.link(ll) = trace_file.link(ind(ll));
end
new_trace_file.AllBetaFactors = AllBeta(ind);
new_trace_file.AllAvgPrSucc   = -tmp_AvgPrSucc;
close(h_waitbar);