%% Comapre simulation and Analytical model for Line
%
% SETUP: - We use a line with 10 links and use the same trace file for all of
%          them. This means links with the same average probability.
%        - We change deadline from T = 10 to T = 50 slots.
%        - For a given deadline T, we use the trace file for all links and
%          we start the simulation in a random point

clear all;
close all;
InitializePaths;
startdir = pwd;


%% ======================  Experimental Data   ============================

% 1. load Trace file (TraceFile)
No_nodes = 8;

path2data = sprintf('SimulationData/SimLogs/Test1_%dnodes', No_nodes);
cd(path2data);
FileName = sprintf('DataSim_%dNodes',No_nodes);
load(FileName);
load('GEmodel')
cd(startdir)


% 2. Experiment setup
NoLinks     = 7;
MinDeadline = NoLinks;
MaxDeadline = 5.*NoLinks;
NoTests     = 4000;                % number of test per deadline

% % 2b. Undersample data to make the samples independent
% for ll=1:NoLinks,
%     new_samples = TraceFile.link(ll).RxVec(1:10:end);
%     TraceFile.link(ll).RxVec = repmat(new_samples, 10, 1);
%     TraceFile.link(ll).AvgPrSucc = sum(TraceFile.link(ll).RxVec)./length(TraceFile.link(ll).RxVec);
% end

% Experiment body
ExperRelVec = zeros(NoLinks-1, 1);
for T = MinDeadline:MaxDeadline,
    ExperRel      = SimulatedReliabilityLine(NoLinks, T, NoTests, TraceFile);
    
    ExperRelVec = [ExperRelVec; ExperRel];
end

%% ======================    Simulated Data    ============================ 
% 1. Extract average link loss probability from the trace file 
LinkLossProb = [];
for ll = 1:NoLinks
    LinkLossProb = [LinkLossProb; (1-TraceFile.link(ll).AvgPrSucc)];
end

% 2. Create a trace file that uniform distribution of packet losses/success 
% centered around the varage experienced in the experiments
a = 0;
for ll=1:NoLinks,
    p_succ = TraceFile.link(ll).AvgPrSucc; % Probability of success
    n = 40000; % Number of flips per trial
    N = 1; % Number of trials
    rand('state',sum(1000*clock)) % Set base generator
    sims = unifrnd(0,1,n,N) < p_succ; % 1 for heads; 0 for tails
      
    SimTraceFile.link(ll).RxVec     = sims;
    SimTraceFile.link(ll).AvgPrSucc = sum(sims)/n;
    phat = sum(sims)/n;
end

% Simulation body
SimRelVec = zeros(NoLinks-1, 1);
for T = MinDeadline:MaxDeadline,
    SimRel      = SimulatedReliabilityLine2(NoLinks, T, NoTests, SimTraceFile);    
    SimRelVec = [SimRelVec; SimRel];
end



%% ==============   Analytical Model from Globecom 2010  ==================
% The imput to the model is the average loss probability coming from the
% experiments



% 1. Use the analytical model from globecom to find the expeced
% deadline-reliability curve
AnalyticRelVec = zeros(NoLinks-1, 1);
for T = MinDeadline:MaxDeadline,
    AnalyticRel = AnalyticalModelRelLine(NoLinks, T, LinkLossProb);
    
    AnalyticRelVec = [AnalyticRelVec; AnalyticRel];
end

%% ==================== Plots and comparison ============================== 
% Links quality
figure(1)
for nn=1:No_nodes
    subplot(No_nodes,1,nn)
    plot(1:length(TraceFile.link(nn).RxVec), TraceFile.link(nn).RxVec,'.b')
    hold on
    plot(1:length(TraceFile.link(nn).AvgPrSuccVec), TraceFile.link(nn).AvgPrSuccVec,'--r', 'linewidth',2)
end

% Comparison Model/data
figure(2)
plot(1:length(AnalyticRelVec), AnalyticRelVec,'-ro')
hold on
plot(1:length(ExperRelVec), ExperRelVec,'--bs')
hold on
plot(1:length(SimRelVec), SimRelVec,'-.kd')
hold on
plot(1:length(R),R,':*')
grid on;
xlabel('Deadline')
ylabel('Reliability')
legend('Analytical Model','Experimental results','Simulated','GE Model',4)
