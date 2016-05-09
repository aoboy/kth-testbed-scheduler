function stats = Network_Connectivity(NoNodes, path2data, institution, data_format)
% NETWORK_CONNECTIVITY: scans the folder with trace files and returns 
% information on the connectivity of the nodes. The code is applied to read
% files with diferent name, distinguished by the institution that produced
% them. 
% The function requires at leastr the following mandatory inputs:
%   1. NoNodes:     is the number of nodes in the network
%   2. Path2data:   is the path to the data logs
%   3. INSTITUTION: identifies the institution that produced the data and 
%                   can take the folowing value:
%
%                  'Stanford' (files named TX+RX.txt)
%                  'KTH'      (files named BinchannelsCClinkTX-RX.txt)
%                             where TX and RX refer to the transmitter 
%                             and receiver ID, respectively, while CC 
%                             denotes the number of channels. 
%   4. data_format: contains basic information of the format used for the
%                   measurements
%
% The last input, NO_CH, denotes the number of channels used in TSCH
% sequences. This is required for traces produced at KTH.
%
% Copiright @ Pablo Soldati 2011

my_dir = pwd;
cd(path2data);

if nargin<3,
    error(fprintf('The function requires at least 3 inputs: NoNodes, path2data and Institution'))
elseif nargin ==3,
    no_ch = 1;
    data_format.channelsID = 26;
    channelsID = data_format.channelsID;
elseif nargin>3,
    channelsID = data_format.channelsID;    
    % KTH data must be logged into folder separated by the number of channels used
    if strcmp(institution, 'KTH'),
        no_ch = length(data_format.channelsID);
        switch data_format.task,
            case 'Basic',
                no_ch = length(data_format.channelsID);
                new_folder = sprintf('%dchannels', no_ch);       % required for TSCH measurements
                cd(new_folder);
            case 'Task1',
                new_folder = data_format.folder_name; 
                cd(new_folder);
            case 'Task2',
                new_folder = data_format.folder_name;      % required for TSCH measurements
                cd(new_folder);
            otherwise
                error(fprintf('Unknown experiment task for KTH data: %s', data_format.task)),
        end
    end
end


% read file names in the folder and reconstruct the network connectivity
ListOfLinks = dir;
ListOfLinks = ListOfLinks(3:end);                % the function "dir" incluses . and ..

NoLinks = size(ListOfLinks,1);

TxRx_ConnectMat = zeros(NoNodes, NoNodes);
switch institution, 
    case 'KTH',
        for ll = 1:NoLinks,
            file_name = ListOfLinks(ll).name;
            pos0 = strfind(file_name, 'k');
            pos1 = strfind(file_name, '-');
            pos2 = strfind(file_name,'.');
            tx   = str2double(file_name((pos0+1):(pos1-1)));  % this implies that all TX ID have 2 digits.
            rx   = str2double(file_name((pos1+1):(pos2-1)));
            TxRx_ConnectMat(tx, rx) = 1;
        end
    case 'Stanford'
        for ll = 1:NoLinks,
            file_name = ListOfLinks(ll).name;
            pos1 = strfind(file_name, '+');
            pos2 = strfind(file_name,'.');
            tx   = str2double(file_name(1:(pos1-1)));
            rx   = str2double(file_name((pos1+1):(pos2-1)));

            TxRx_ConnectMat(tx,rx) = 1;
        end
    otherwise
        error(fprintf('Unknown institution: %s', institution))
end

for nn = 1:NoNodes,
    Node(nn).neighbors = find(TxRx_ConnectMat(nn,:)==1);
end

stats.NoNodes         = NoNodes;
stats.NoLinks         = NoLinks;
stats.ChannelsID      = channelsID;
stats.NoChannels      = length(channelsID);
stats.TxRx_ConnectMat = sparse(TxRx_ConnectMat);
stats.Node_Stats      = Node;
cd(my_dir);
return;