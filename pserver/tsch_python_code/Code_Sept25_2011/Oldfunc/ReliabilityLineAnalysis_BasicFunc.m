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
startdit = pwd;

% load link data
% path2data = 'SimulationData/SimLogs/Test';
% cd(path2data);
% load 'LinkData';
% cd(startdir)
% 
% LinkRxPkt = LinkData.RxVec; 

a = 0; b = 1;
LinkRxPkt = round((a+(b-a).*rand(10000,1))./(b-a));
AvgPloss  = 1-(sum(LinkRxPkt)./10000);

%% Simlulation setup
NoLinks     = 10;
MinDeadline = NoLinks;
MaxDeadline = 5.*NoLinks;
NoTests     = 5000;                % number of test per deadline


%% Simulation body
SimulRelVec = zeros(NoLinks-1, 1);
for T = MinDeadline:MaxDeadline,
    SimRel      = SimulatedReliabilityLine_BasicFunc(NoLinks, T, NoTests, LinkRxPkt);
    
    SimulRelVec = [SimulRelVec; SimRel];
end


%% Analytical Model from Globecom 2010:

LinkLossProb = AvgPloss.*ones(NoLinks,1);

AnalyticRelVec = zeros(NoLinks-1, 1);
for T = MinDeadline:MaxDeadline,
    AnalyticRel = AnalyticalModelRelLine(NoLinks, T, LinkLossProb);
    
    AnalyticRelVec = [AnalyticRelVec; AnalyticRel];
end

%% figure
figure(1)
plot(1:length(AnalyticRelVec), AnalyticRelVec,'--ro')
hold on
plot(1:length(SimulRelVec), SimulRelVec,'-bs')
grid on;
xlabel('Deadline')
ylabel('Reliability')
legend('Analytical Model','Simulation',2)
