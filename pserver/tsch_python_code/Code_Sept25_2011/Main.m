%% KTH MEASUREMENTS:
% This files extracts KTH data logs for TSCH measuremets and performs the 
% following actions: 
%   1. Find the connectivity structure of the network (tx-Rx pairs)
%   2. Extract data logs and convert them to Matlab structure
%   3. Compute link statistics:
%       3a. beta factor 
%       3b. kappa factor
%
% Required inputs are:
%   a) Number of nodes involved in the experiment
%   b) Number of channels



% Each experiment consists of a a burst transmission of 10.000 packets 
% broadcasted from each node using a specific channel hopping sequence.
% Each experiment log is associated with a specific Tx-RX pair and contains 
% a matrix of size Kx16 where a entry 1 corresponds to a correctly received 
%

clear all;
% close all;
InitializePaths;
startdir = pwd;
workdir  = pwd;

% % Extract data from original trace files
% fprintf('========================================================================================== \n')
% fprintf('\n')
% fprintf('To process your data, this function needs dedicated inputs that you will next require \n')
% fprintf('you to provide some inputs. Among these, you need to specify: \n')
% fprintf('     - The path to the data logs;\n')
% fprintf('     - The institutions (KTH or Stanford) where the data were collected;\n')
% fprintf('     - The number of nodes used in the experiments;\n')
% fprintf('     - The number of channels;\n')
% fprintf('\n')
% fprintf('Once you feel confident with the code, you may comment the lines 30-51 and uncomment \n')
% fprintf('the lines 53-68 to assign static entries based on the location of the data in your folders.\n')
% fprintf('\n')
% fprintf('========================================================================================== \n')
% fprintf('\n')
% go2path     = input('Enter the path to the data logs: ');
% Institution = input('Enter the Institution: ');
% NoNodes     = input('Enter the number of nodes: ');
% ChannelsID  = input('Enter the Channels ID in vector form Channels: '); 
% switch Institution,
%     case 'KTH'
%         data_format.no_col  = 16;
%     case 'Stanford'
%         data_format.no_col  = 5;
%         data_format.PkSent  = 1e4;
%     otherwise
%         error(fprintf('Unknown institution: %s', Institution));
% end

Institution = 'KTH';
NoNodes     = 100;      %this can be larger than the actual number of nodes
ChannelsID  = 1:4; 
switch Institution,
    case 'KTH'
        data_format.no_col  = 16;
        go2path  = '/Users/pablosoldati/Documents/MATLAB/2011/TSCH_project/Experiments_DataLogs/KTH/May13';
    case 'Stanford'
        %go2path  = '/Users/pablosoldati/Documents/MATLAB/2011/TSCH_project/Experiments_DataLogs/Stanford/chl26_pwr_7_bcast_10k_Apr_20_09';
        go2path  = '/Users/pablosoldati/Documents/MATLAB/2011/TSCH_project/TestTraces4Kappa';

        data_format.no_col  = 5;
        data_format.PkSent  = 1e4;
    otherwise
        error(fprintf('Unknown institution: %s', Institution));
end



fprintf('Step 1 of 4: Nodes'' neighbors discovery and conectivity...')
% net_stats = Network_Connectivity(NoNodes, go2path, Institution);
net_stats = Network_Connectivity(NoNodes, go2path, Institution, ChannelsID);
fprintf('done!\n')

% 
fprintf('Step 2 of 4: Extract trace files and convert to Matlab format...')
[net_stats TraceFile] = Extract_Data(go2path, net_stats, data_format, Institution);
fprintf('done!\n')

% %clear(go2path);clear('no_col'); clear('PkSent');


%% Add CPDF and Beta-Factor to the trace file of each link
max_window  = 50;
fprintf('Step 3 of 4: Computing CPDF and Beta-factor for all links...')
[net_stats TraceFile] = Compute_BetaFactor(TraceFile, net_stats, max_window);
fprintf('done!\n')

% Add Kappa Factor
fprintf('Step 4 of 4: Computing Kappa factor for all links...')
fprintf('done!\n')

[Net_Stats Trace_File] = Compute_KappaFactor(TraceFile, net_stats);

% sort the trace files in decreasing order of PRR
%SortedTrace_File = Sort_PRR(Trace_File);

%
clear('tmp_net_stats'); clear('data_format'); clear('go2path');clear('NoNodes');clear('startdir');
cd('DataLogs/KTH')
filename = sprintf('KTH_TSCH_%dChannels',Net_Stats.NoChannels);
save(filename)
cd(workdir)