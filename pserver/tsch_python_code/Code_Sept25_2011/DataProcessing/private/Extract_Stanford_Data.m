function xx = Extract_Stanford_Data(tx, rx, no_cols, tot_pkt_sent)
% EXTRACT_KTH_DATA: this function extract data from a Stanford trace. The
% requited inputs are:
%   'tx': transmitter ID
%   'rx': receiver ID
%
% Copyright @ Pablo Soldati 2011.

filename = sprintf('%d+%d.txt',tx, rx);
file     = fopen(filename,'r');
raw_data = fscanf(file,'%f');
fclose(file);

% reshape data in matrix form
K        = length(raw_data);
no_rows  = floor(K/no_cols);
filename = sprintf('%d+%d.txt',tx, rx);
file     = fopen(filename,'r');
raw_data = fscanf(file,'%f',[no_cols, no_rows])';
fclose(file);

%% process received packets
received_pkt = zeros(tot_pkt_sent,1);
for tt=1:no_rows,
    if raw_data(tt,1)<tot_pkt_sent+1,
        received_pkt(raw_data(tt,1))=1;
    else
        sprintf('WARNING: Link %d received a unknown pkt ID number %d larger than ID %d', link_index, raw_data(tt,1), tot_pkt_sent)
    end
end
xx.rx_pkt = received_pkt;
return;