function [net_stats trace_file] = Compute_BetaFactor(trace_file, net_stats, max_win, rho)
% COMPUTE_CPDFs: Computes CPDF and beta factor for a set of data traces.
%
% Copyright @ Pablo Soldati 2011

if nargin < 3,
    error(fprintf('The function needs at least THREE inputs'));
elseif nargin==3,
    task = 'Beta';
elseif nargin ==4,
    task = 'Beta_&_CrossCPDFs';
end

% initialize values
no_links = net_stats.NoLinks;
no_nodes = net_stats.NoNodes;

AllBeta      = zeros(no_links,1);
AllAvgPrSucc = zeros(no_links,1);

% main body
h_waitbar=waitbar(0, 'Processing data for CPDF and beta-factor...');
for nn = 1:no_nodes,
    if mod(nn,10)==0,
        waitbar(nn/no_nodes, h_waitbar, sprintf('Processing data for CPDF and beta-factor...<%d%%>', ceil(100*nn/no_nodes)));
    end;
    if ~isempty(net_stats.Node_Stats(nn).outgoing_links),
        outgoing_links = net_stats.Node_Stats(nn).outgoing_links;
%         neighbors      = net_stats.Node_Stats(nn).neighbors;        

        beta_factor_vec = zeros(length(outgoing_links),1);
        link_PRR_vec    = zeros(length(outgoing_links),1);
        CrossCPDF       = cell(length(outgoing_links));        
        switch task,
            case 'Beta'
                for ll=1:length(outgoing_links),
                    ref_link   = outgoing_links(ll); 
                    main_data  = trace_file.link(ref_link).RxVec;
                    cross_data = main_data;
                    link_PRR_vec(ll) = trace_file.link(ref_link).AvgPrSucc;

                    link_cpdf    = zeros(2*max_win+1,1);
%                   link_CW_meas = zeros(2*max_win+1,1);
%                   link_CW_ind  = zeros(2*max_win+1,1);
                    for window = 1:max_win,
                        cond_evn0 = 0;              % conditioning event is failure
                        cond_evn1 = 1;              % conditioning event is success
                        x0 = CondProbWindow(main_data, cross_data, window, 1, cond_evn0);
                        x1 = CondProbWindow(main_data, cross_data, window, 1, cond_evn1);
                        link_cpdf(max_win+1-window) = x0;
                        link_cpdf(max_win+1+window) = x1;

%                       %% compute terms for CW distance
%                         if x0~=0,
%                           link_CW_meas(max_win+1-window) = x0; 
%                             link_CW_ind(max_win+1-window)  = link_PRR;
%                         end
%                         if x1~=0,
%                             link_CW_meas(max_win+1+window) = 1 - x1;
%                             link_CW_ind(max_win+1+window)  = 1 - link_PRR;
%                         end
                    end
                    beta_factor_vec(ll) = BetaFactor(max_win, link_cpdf, link_PRR_vec(ll));
                end
                % store data for the current link
                trace_file.link(ref_link).BetaFactor      = beta_factor_vec(ll);
                trace_file.link(ref_link).CPDF_max_win    = max_win;                
            case 'Beta_&_CrossCPDFs',                        
                for ll=1:length(outgoing_links),
                    ref_link  = outgoing_links(ll); 
                    main_data = trace_file.link(ref_link).RxVec;
                    link_PRR_vec(ll) = trace_file.link(ref_link).AvgPrSucc;
                    for mm = 1:length(outgoing_links),
                        cross_link = outgoing_links(mm);
                        cross_data = trace_file.link(cross_link).RxVec;

                        link_cpdf    = zeros(2*max_win+1,1);
%                         link_CW_meas = zeros(2*max_win+1,1);
%                         link_CW_ind  = zeros(2*max_win+1,1);
                        for window = 1:max_win,
                            cond_evn0 = 0;              % conditioning event is failure
                            cond_evn1 = 1;              % conditioning event is success
                            x0 = CondProbWindow(main_data, cross_data, window, 1, cond_evn0);
                            x1 = CondProbWindow(main_data, cross_data, window, 1, cond_evn1);
                            link_cpdf(max_win+1-window) = x0;
                            link_cpdf(max_win+1+window) = x1;

%                           %% compute terms for CW distance
%                          if x0~=0,
%                             link_CW_meas(max_win+1-window) = x0; 
%                             link_CW_ind(max_win+1-window)  = link_PRR;
%                          end
%                          if x1~=0,
%                             link_CW_meas(max_win+1+window) = 1 - x1;
%                             link_CW_ind(max_win+1+window)  = 1 - link_PRR;
%                          end
                        end
                
                        % Compute beta
                        if ref_link == cross_link,
                            beta_factor_vec(ll) = BetaFactor(max_win, link_cpdf, link_PRR_vec(ll));
                        end

                        %store cross/self CPDF
                        CrossCPDF{ll,mm} = link_cpdf;
                    end
                end
                % store data for the current link
                trace_file.link(ref_link).BetaFactor      = beta_factor_vec(ll);
                trace_file.link(ref_link).CPDF            = CrossCPDF{ll,ll};
                trace_file.link(ref_link).CPDF_max_win    = max_win;
            otherwise
                error(fprintf('Unknow required statistics'))
        end
        
        % Store the statistics for teh current node
        net_stats.Node_Stats(nn).linksPRR   = link_PRR_vec;
        net_stats.Node_Stats(nn).linksBeta  = beta_factor_vec;
        if strcmp(task,'Beta_&_CrossCPDFs'),
            net_stats.Node_Stats(nn).CrossCPDFs = CrossCPDF;    
        end

        AllBeta(outgoing_links)         = beta_factor_vec;
        AllAvgPrSucc(outgoing_links)    = link_PRR_vec;

%       trace_file.link(ll).CWdist          = link_CW_meas;
%       trace_file.link(ll).CWdist_ind_link = link_CW_ind;
        
    end
end

net_stats.Traces       = trace_file;
net_stats.AllAvgPrSucc = AllAvgPrSucc;
net_stats.AllBeta      = AllBeta;
% trace_file.AllBetaFactors = AllBeta;
% trace_file.AllAvgPrSucc   = AllAvgPrSucc;

close(h_waitbar);