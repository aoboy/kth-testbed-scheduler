function [net_stats trace_file] = Compute_KappaFactor(trace_file, net_stats)
% COMPUTE_KAPPAFACTOR: computes the Kappa Factor for a given set of trace
% files. Two cases are considered:
%
%   - Kappa for spatial correlation: When the trace files are collected over 
%                                    a single channel, the function compute
%                                    the spatial correlation between
%                                    outgoing links from the same
%                                    transmitter as defined in [1] 
%   - Kappa for frequency correlation: When the trace files are collected
%                                      using a multi-channel TSCH MAC, the 
%                                      computed kappa yields the correlation 
%                                      between two channels
%
% References:
%   [1] K. Srinivasan, M. Jain, J II Choi, T. Azim, E.S. Kim P. Levis and 
%       B. Krishnamachari, "The \kappa factor: Inferring Protocol Performance 
%       Using Inter-link Reception Correlation. In the ACM Mobicom 2010. 
% 
% Copyright @ Pablo Soldati 2011.

% initialize values
% no_links    = net_stats.NoLinks;
no_nodes    = net_stats.NoNodes;
no_channels = net_stats.NoChannels;

% Based on the number of channels, establish which correlation should be
% computed
if no_channels == 1,
    Kappa = 'Spatial_Correlation';   % Computes the Kappa factor defined in [1]
elseif no_channels > 1,
    Kappa = 'Frequency_Correlation'; % Computes a Kappa factor based on frequency correlation. 
end

AllKappaFactors = [];
% main body
h_waitbar=waitbar(0, 'Computing Kappa Factor...');
for nn = 1:no_nodes,
    if mod(nn,10)==0,
        waitbar(nn/no_nodes, h_waitbar, sprintf('Computing Kappa Factor...<%d%%>', ceil(100*nn/no_nodes)));
    end;
    
    % Check whether the index nn correspond to an effective transmitter
    if ~isempty(net_stats.Node_Stats(nn).neighbors),
%         tx_node = nn;
%         Rx_nodes       = net_stats.Node_Stats(nn).neighbors;
        outgoing_links = net_stats.Node_Stats(nn).outgoing_links;
        switch Kappa,
            case 'Spatial_Correlation',
                % In this case, the Kappa factor is a spatial-domain correlation statistic of the outgoing 
                % links from the same transmitter. As such, there is a the KF is computed separately for 
                % each transmitter as (L x L) matrix, where L is the number of outgoing links  
                KF_mat = zeros(length(outgoing_links));
                for ll=1:length(outgoing_links),
                    ref_link  = outgoing_links(ll); 
                    ref_trace = trace_file.link(ref_link).RxVec;
                    for jj = 1:length(outgoing_links)
                        if jj>ll,
                            cross_link  = outgoing_links(jj); 
                            cross_trace = trace_file.link(cross_link).RxVec;

                            KF = KappaFactor(ref_trace, cross_trace);
                            KF_mat(ll,jj) = KF;
                            KF_mat(jj,ll) = KF;
                            AllKappaFactors = [AllKappaFactors KF];
                        end
                    end
                end
                net_stats.Node_Stats(nn).KF_mat = KF_mat;                
            case 'Frequency_Correlation',
                no_ch  = no_channels;
                % In this case, the Kappa factor is a frequency-domain statistic of each separate link. 
                % As such, there is a the KF is a (no_ch x no_ch) matrix computed for each outgoing link 
                for ll=1:length(outgoing_links),
                    link      = outgoing_links(ll);
                    tmp_trace = [];
                    for cc = 1:no_ch,
                        tmp_trace(cc).RxVec = trace_file.link(link).RxVec(cc:no_ch:end);
                    end
                    KF_mat = zeros(no_ch,no_ch);
                    KF_vec = zeros(no_ch,1);
                    for ch1=1:no_ch,
                        ref_trace = tmp_trace(ch1).RxVec;
                        for ch2 = 1:no_ch,
                            if ch2>ch1,
                                cross_trace = tmp_trace(ch2).RxVec;
                                KF = KappaFactor(ref_trace, cross_trace);
                                KF_mat(ch1,ch2) = KF;
                                KF_mat(ch2,ch1) = KF;
                                AllKappaFactors = [AllKappaFactors KF];
                                if ch2==(ch1+1),
                                    KF_vec(ch2-1) = KF;
                                elseif ch2 == no_ch,
                                    KF_vec(ch2) = KF;
                                end
                            end
                        end
                    end
                end
                trace_file.link(link).KFmat_freq_domain = KF_mat;
                trace_file.link(link).KFvec_freq_domain = KF_vec;
            otherwise
                error(fprintf('Unknown Kappa factor: %s', Kappa));
        end
    end
end

net_stats.Traces     = trace_file;
net_stats.AllKappa   = AllKappaFactors;
net_stats.Kappa_case = Kappa;

close(h_waitbar);
return;
