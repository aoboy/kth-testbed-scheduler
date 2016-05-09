function [net_stats trace_stats] = Extract_Data(go2path, net_stats, data_format, institution)
% EXTRACTDATA_STANFORDTRACE: Extract data from Stanford traces and converts
% them into a convenient Matlab form. The function handles data produced 
% from different institutions and saved with different names.
%
% Here INSTITUTION can take the folowing value:
%
%   'Stanford' (files named TX+RX.txt)
%   'KTH'      (files named BinchannelsCClinkTX-RX.txt)
%
% where TX and RX refer to the transmitter and receiver ID, respectively,
% while CC denotes the number of channels. 
%
% Copiright @ Pablo Soldati 2011

work_dir = pwd;
cd(go2path);

% KTH data must be logged into folder separated by the number of channels used
if strcmp(institution, 'KTH'),
    no_ch = length(data_format.channelsID);
    switch data_format.task,
        case 'Basic'
            new_folder = sprintf('%dchannels',no_ch);       % required for TSCH measurements
            cd(new_folder);
        case 'Task1'
            new_folder = data_format.folder_name;
            cd(new_folder);
        case 'Task2'
            new_folder = data_format.folder_name;           % required for TSCH measurements
            cd(new_folder);            
        otherwise
            error(fprintf('Unknown experiment task for KTH data: %s', data_format.task)),
    end
end

no_nodes     = net_stats.NoNodes;
no_links     = net_stats.NoLinks;
no_col       = data_format.no_col;

if strcmp(institution, 'Stanford')
    tot_pkt_sent = data_format.PkSent;
end

link_data    = zeros(no_links,2);
link_index   = 0;
h_waitbar = waitbar(0, 'Extracting data from original trace files...');
for tx=1:no_nodes,
    if mod(tx,floor(no_nodes/10))==0,
        waitbar(tx/no_nodes, h_waitbar, sprintf('Extracting data from original trace files...<%d%%>', ceil(100*tx/no_nodes)));
    end;
    neighbors_set = net_stats.Node_Stats(tx).neighbors;
        
    if ~isempty(neighbors_set),
        for jj = 1:length(neighbors_set),
            link_index = link_index+1;
            rx = neighbors_set(jj);
            link_data(link_index, :) = [tx rx];
            
            switch institution,
                case 'Stanford',
                    XX = Extract_Stanford_Data(tx, rx, no_col, tot_pkt_sent);
                    received_pkt = XX.rx_pkt;
                case 'KTH',
                    XX = Extract_KTH_Data(tx, rx, no_col, no_ch, data_format);
                    received_pkt = XX.rx_pkt;
                    tot_pkt_sent = length(received_pkt);
                otherwise
                    error(fprint('Unknown institution: %s', institution));
            end
            AvgPrSucc = sum(received_pkt)./tot_pkt_sent;
            
%             AvgPrSuccVec = [];
%             for tt=1:tot_pkt_sent,
%                 AvgPrSuccVec = [AvgPrSuccVec; (sum(received_pkt(1:tt))./tt)];
%             end
            trace_stats.link(link_index).TxID      = tx;
            trace_stats.link(link_index).RxID      = rx;
            trace_stats.link(link_index).RxVec     = received_pkt;
            trace_stats.link(link_index).AvgPrSucc = AvgPrSucc;
%             trace_stats.link(link_index).AvgPrSuccVec = AvgPrSuccVec;

            % For TSCH traces produced at KTH we also analyze the length of
            % the first and second bursts.
            if strcmp(institution, 'KTH')
                trace_stats.link(link_index).RxMat     = XX.rx_pkt_mat;
                Bursts.first_burst.init(link_index)    = XX.burst.first_burst.init;
                Bursts.first_burst.length(link_index)  = XX.burst.first_burst.length;
                Bursts.second_burst.init(link_index)   = XX.burst.second_burst.init;
                Bursts.second_burst.length(link_index) = XX.burst.second_burst.length;
            end
        end
    end
end


%% Polish the link data and their index. 
% The Network_connectivity.m function estimates that there are as many
% links as the number of files it finds in the data folder. However, if
% other files are also stored in the folder, one need to reshape the LINK_DATA. 
% In this case, the correct amount of links is given by the last value of LINK_INDEX.  
if link_index~=no_links,
%     error(fprintf('Mismatch in the total number of links'));
    net_stats.NoLinks = link_index;
    trace_stats.Link_Data = link_data(1:link_index, :);
    net_stats.Link_Data   = link_data(1:link_index, :);    
else
    trace_stats.Link_Data = link_data;
    net_stats.Link_Data   = link_data;
end

for nn = 1: no_nodes,
    net_stats.Node_Stats(nn).outgoing_links = find(link_data(:,1)==nn)';
end

close(h_waitbar);
clear('K'); clear('no_rows'); clear('filename'); clear('file'); clear('raw_data');
cd(work_dir);
return;