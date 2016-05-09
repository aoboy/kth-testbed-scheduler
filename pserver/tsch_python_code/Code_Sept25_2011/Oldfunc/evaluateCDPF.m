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
cd(startdir)


% 2. Experiment setup
NoLinks     = 7;
MinDeadline = NoLinks;
MaxDeadline = 5.*NoLinks;
NoTests     = 4000;                % number of test per deadline
max_window  = 50;

TraceFile = ConditionalPacketDeliveryFunction(TraceFile, NoLinks, max_window);

%% figures

% figure(1)
subplot(2,1,1)
bar(-max_window:max_window, TraceFile.link(1).CPDF)
hold on
plot(-max_window:max_window, TraceFile.link(1).AvgPrSucc.*ones(2*max_window+1,1),'r','Linewidth', 2)
axis([-max_window max_window 0 1])
xlabel('Consecutive faiulure/success')
ylabel('CPDF')
title('Measurements')
subplot(2,1,2)
bar(-max_window:max_window, TraceFile.link(1).CPDF_indep_link)
hold on
plot(-max_window:max_window, TraceFile.link(1).AvgPrSucc_fake.*ones(2*max_window+1,1),'r','Linewidth', 2)
axis([-max_window max_window 0 1])
xlabel('Consecutive faiulure/success')
ylabel('CPDF')
title('independent link with same PRR')


figure(2)
for ll=1:NoLinks,
    plot(ll, TraceFile.link(ll).BetaFactor, 'sr','Linewidth', 2)
    hold on
end
grid on
xlabel('Link ID')
ylabel('\beta factor')
axis([1 NoLinks 0 1])