function sorted_trace_file = Sort_PRR(trace_file)
% SORT_PRR: reorder links (and related statistics) contained in the trace
% file by descreasing order of their PRR.
%
% Copyright @ Pablo Soldati 2011

%% sort the links in decreasing order of success provability
[tmp_AvgPrSucc index] = sort(-AllAvgPrSucc);
sorted_trace_file.OriginalLinkIndex = index;

for ll = 1:no_links
    sorted_trace_file.link(ll) = trace_file.link(index(ll));
end
sorted_trace_file.AllBetaFactors = AllBeta(index);
sorted_trace_file.AllAvgPrSucc   = -tmp_AvgPrSucc;
