%% Initialization
clear all;
close all;
InitializePaths;
startdir = pwd;

%% Extract and process data
No_nodes  = 8;
path2data = sprintf('SimulationData/SimLogs/Test1_4nodes');

TraceFile = ExtractData(path2data,No_nodes);

%% Add CPDF, Earth Movers Distance, and Beta-Factor to the trace file of each link
max_window  = 10;

TraceFile = ConditionalPacketDeliveryFunction(TraceFile, NoLinks, max_window);



%% Save data
cd(path2data)
clear('path2data')
FileName = sprintf('DataSim_%dNodes',No_nodes);
save(FileName)
cd(startdir);



%% Figure 1: Link quality
figure(1)
for nn=1:No_nodes
    subplot(No_nodes,1,nn)
    plot(1:length(TraceFile.link(nn).RxVec), TraceFile.link(nn).RxVec,'.b')
    hold on
    plot(1:length(TraceFile.link(nn).AvgPrSuccVec), TraceFile.link(nn).AvgPrSuccVec,'--r', 'linewidth',2)
    text = sprintf('Node %d',No_nodes-nn+1);
    ylabel(text)
end
xlabel('packet index')

%% Fifure 2 :
figure(2)
link_index = 1; 
AvgPrSucc  = TraceFile.link(link_index).AvgPrSucc.*ones(length(TraceFile.link(link_index).AvgPrSuccVec),1);
plot(1:length(TraceFile.link(link_index).AvgPrSuccVec), TraceFile.link(link_index).AvgPrSuccVec,'.b')
hold on
plot(1:length(TraceFile.link(link_index).AvgPrSuccVec), AvgPrSucc,'.r')


%% Figure 3: CPDF for a link
figure(3)
bar(-max_window:max_window, TraceFile.link(7).CPDF)
axis([-max_window max_window 0 1])
title('CPDF')
xlabel('Consecutive failure/success')
ylabel('Conditional probability')