%% STANFORD MEASUREMENTS:
% This files extracts the data from the Stanford measuremets. Each experiment 
% consists of a burst transmission of 10.000 packets from one node. 

% Each *.txt files contains 5 columns which refers to:
%    1. packet sequence number
%    2.
%    3.
%    4. unknown
%    5. unkown
%
% In what follows we are only interested in extracting the first column
% (sequence number) and reconstruct the series of packet success/loss as a
% one/zeros.

clear all;
close all;
InitializePaths;
startdir = pwd;
workdir  = pwd;

%% Extract data from original trace files
go2path  = 'C:\Program Files\MATLAB\R2010a\work\2011\Reroute-Retransmit\Code_Jan21_2011\DataLogs\Stanford\chl26_pwr_7_bcast_10k_Apr_20_09';

data_format.no_col  = 5;
data_format.PkSent  = 1e4;

NoNodes = 100;

fprintf('Step 1 of 3: Nodes'' neighbors discovery and conectivity... \n')
tmp_net_stats = Network_Connectivity(NoNodes, go2path, 'Stanford');
% 
fprintf('Step 2 of 3: Extract trace files and convert to Matlab format... \n')
[tmp_net_stats TraceFile] = Extract_Data(go2path, tmp_net_stats, data_format, 'Stanford');
% %clear(go2path);clear('no_col'); clear('PkSent');


%% Add CPDF and Beta-Factor to the trace file of each link
max_window  = 50;
fprintf('Step 3 of 3: Computing CPDF and Beta-factor for all links... \n')
[Net_Stats Sorted_Trace_File] = Compute_CPFDs(TraceFile, tmp_net_stats, max_window);

% %%
clear('tmp_net_stats'); clear('data_format'); clear('go2path');clear('NoNodes');clear('startdir');
cd('DataLogs\Stanford')
% filename = sprintf('MatlabTrace_chl26_pwr_7_bcast_10k_Apr_20_09');
% save(filename)
cd(workdir)