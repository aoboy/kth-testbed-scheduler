function xx = BetaFactor(max_win, link_cpdf, link_PRR)


%% compute terms for CW distance
link_CW_meas = zeros(2*max_win+1,1);
link_CW_ind  = zeros(2*max_win+1,1);
for window = 1:max_win,
    x0 = link_cpdf(max_win+1-window);
    x1 = link_cpdf(max_win+1+window);
    if x0~=0,
        link_CW_meas(max_win+1-window) = x0; 
        link_CW_ind(max_win+1-window)  = link_PRR;
    end
    if x1~=0,
        link_CW_meas(max_win+1+window) = 1 - x1;
        link_CW_ind(max_win+1+window)  = 1 - link_PRR;
    end
end

if any(link_CW_ind),
    term1 = mean(link_CW_ind(link_CW_ind~=0));         % if link_CW_ind has at least a nonzero element, 
                                                       % the average is taken only on the positive elements                                                                                                                      
else
    term1 = 0;                                         % if all elements of link_CW_ind are zero, the average is zero
end
if any(link_CW_meas),
    term2 = mean(link_CW_meas(link_CW_meas~=0));       % if link_CW_meas has at least a nonzero element, 
                                                       % the average is taken only on the positive elements                                                                                                                      
else
    term2 = 0;                                         % if all elements of link_CW_meas are zero, the average is zero
end

if (term1 == 0) && (term2 == 0),
    beta_factor = 0;                                   % this can happen only when I have either all losses or all success
else 
    beta_factor  = (term1-term2)./term1;   
%         beta_factor  = (mean(link_CW_ind(find(link_CW_ind~=0)))-mean(link_CW_meas(find(link_CW_meas~=0))))./mean(link_CW_ind(find(link_CW_ind~=0)))
end

xx = beta_factor;
return;