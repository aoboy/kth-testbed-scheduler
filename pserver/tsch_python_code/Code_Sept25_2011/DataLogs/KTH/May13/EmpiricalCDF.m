function [xx range_samples] = EmpiricalCDF(data_vec, data_range, no_samples)
% DATA_CDF: Compute the Cumulative Distribution Function (CDF)for a set of
% empirical data. It requires the following two inputs:
%   - 'data_vec' is a vector containing the empirical data to analyze
%   - 'data range' is a two-valued vector [a b] containing the min and max 
%                  values, 'a' and 'b' respectively, that the empirical
%                  data can take.
%
% The output is the daya CDF.
%
% Copyright @ Pablo Soldati 2011.

if nargin < 2,
    error(fprintf('The function needs at least two inputs'));
end
if nargin == 2,
    no_samples = 1e3;
end

N = length(data_vec);                       % number of data samples

data_vec   = sort(data_vec);                % The data set is sorted in increasing order
size_range = data_range(2) - data_range(1); % Maimum size of the range of values
stepsize   = size_range/no_samples;         

range_samples = data_range(1):stepsize:data_range(2); % sanples in the range [a, b] used to compute CDF

xx = zeros(length(range_samples),1);      % used to store the CDF values

for ii=1:length(range_samples),
    d_index  = find(data_vec <= range_samples(ii)); % Index of all elemnts smaller then the current sample
    if isempty(d_index),                            
        if ii>1,
            xx(ii) = xx(ii-1);
        end
    else
        xx(ii) = d_index(end)/N;    % Since the data has been sorted, the last index correspond with the 
    end                             % number of element in the set (that are smaller than the sample)
end
return;