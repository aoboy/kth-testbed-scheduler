function trace_file = ConditionalPacketDeliveryFunction(trace_file, no_links, max_win)
%

%% evaluate CPDF
fprintf('evaluating CPDF for all data traces... \n')
for ll = 1:no_links,
    tmp_data = trace_file.link(ll).RxVec;

    link_cpfd = zeros(2*max_win+1,1);
    for window = 1:max_win,
        cond_evn0 = 0;              % conditioning event is failure
        cond_evn1 = 1;              % conditioning event is success
        
        x0 = CondProbWindow(tmp_data, window, 1, cond_evn0);
        x1 = CondProbWindow(tmp_data, window, 1, cond_evn1);

        link_cpfd(max_win+1-window) = x0;
        link_cpfd(max_win+1+window) = x1;

    end
    trace_file.link(ll).CPDF            = link_cpfd;
    trace_file.link(ll).CPDF_max_window = max_win;
end

%% Evaluate the Earth Mover's Distance (EMD) for the current CPDF

fprintf('evaluating Earth Movers Distance for all data traces... \n')

beam_pos_ref = (-max_win:max_win)';
beam_amp_ref = [zeros(max_win+1,1); ones(max_win,1)];

beam_pos_data = beam_pos_ref;
for ll=1:no_links,
    beam_amp_data = trace_file.link(ll).CPDF;
    
    f1 = beam_pos_data;
    f2 = beam_pos_ref;
    
    % Weights
    w1 = beam_amp_data / sum(beam_amp_data);
    w2 = beam_amp_ref / sum(beam_amp_ref);

    % Earth Mover's Distance
    [f, fval] = EarthMoverDistance(f1, f2, w1, w2, @gdf);
    trace_file.link(ll).CWdist = fval;
end

%% compute Beta-factor:
% For each link, we need to find the CPDF of an independent link with the
% same avereage packet loss probability
fprintf('Computing Beta-factors... \n')

for ll=1:no_links,
    Psucc = trace_file.link(ll).AvgPrSucc;
    no_trials = 40000;                                   % Number of flips per trial
    N = 1;                                               % Number of trials
    rand('state',sum(1000*clock))                        % Set base generator
    Sim_trace_file = unifrnd(0,1,no_trials,N) < Psucc;   % 1 for heads; 0 for tails
    
    trace_file.link(ll).AvgPrSucc_fake = sum(Sim_trace_file)./no_trials;
    
    % Compute the CPDF of the simulated independent link
    link_cpfd = zeros(2*max_win+1,1);
    for window=1:max_win,
        cond_evn0 = 0;              % conditioning event is failure
        cond_evn1 = 1;              % conditioning event is success
        x0 = CondProbWindow(Sim_trace_file, window, 1, cond_evn0);
        x1 = CondProbWindow(Sim_trace_file, window, 1, cond_evn1);
        
        link_cpfd(max_win+1-window) = x0;
        link_cpfd(max_win+1+window) = x1;
    end
    trace_file.link(ll).CPDF_indep_link = link_cpfd;

    % compute Earth Mover's Distance of the simulated independent link from
    % the reference CPDF
    %beam_pos_data = beam_pos_ref;
    
    beam_amp_data = link_cpfd;
    
    f1 = beam_pos_data;
    f2 = beam_pos_ref;
    
    % Weights
    w1 = beam_amp_data / sum(beam_amp_data);
    w2 = beam_amp_ref / sum(beam_amp_ref);

    % Earth Mover's Distance
    [f, fval] = EarthMoverDistance(f1, f2, w1, w2, @gdf);
    
    % Beta-Factor
    beta_factor = (fval-trace_file.link(ll).CWdist)./fval;
    
    trace_file.link(ll).CWdist_indep_link = fval;
    trace_file.link(ll).BetaFactor = beta_factor;
end                    