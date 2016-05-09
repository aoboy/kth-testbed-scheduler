function xx = Extract_KTH_Data(tx, rx, no_cols, no_ch, data_param)
% EXTRACT_KTH_DATA: this function extract data from a KTH trace. The
% requited inputs are:
%   'tx': transmitter ID
%   'rx': receiver ID
%   'no_ch': numver of channels in TSCH sequence
%
% Copyright @ Pablo Soldati 2011.

if nargin < 5,
    task = 'Basic';
else
    task     = data_param.task;
    ChID_vec = data_param.channelsID;
    if strcmp(task, 'Task1'),
        trial = data_param.trial; % the first task consists of several trials saved in different folders
    end
end

switch task,
    case 'Basic'
        filename = sprintf('Binchannels%dlink%d-%d.txt',no_ch, tx, rx);
    case 'Task1',
        filename = sprintf('link%d-%d.TXT', tx, rx);
    case 'Task2',
        filename = sprintf('link%d-%d.TXT', tx, rx);
    otherwise
        error(fprintf('Unknown experiment task for KTH data: %s', task));
end
file     = fopen(filename,'r');
%filename
raw_data = fscanf(file,'%f');
%raw_data = fscanf(file,'%c');
fclose(file);

% reshape data in matrix form
tot_pkt_sent = length(raw_data);
no_rows      = floor(tot_pkt_sent/no_cols);


xx.rx_pkt     = raw_data;
xx.rx_pkt_mat = reshape(raw_data, no_cols, no_rows)';



%% Identify the first and second long bursts of packet losses
xx.burst = bursts_finder(xx.rx_pkt_mat, no_rows, no_cols);

return;