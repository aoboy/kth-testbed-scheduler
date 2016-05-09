function xx = KappaFactor (trace_x, trace_y)
% KAPPA_ FACTOR: Computes the spatial correlation (the Kappa Factor)
% between two trace files received at different receivers upon a burst of
% transmission from the same sender.
%
% The computation follows the expression in [1]
%
% References:
%   [1] K. Srinivasan, M. Jain, J II Choi, T. Azim, E.S. Kim P. Levis and 
%       B. Krishnamachari, "The \kappa factor: Inferring Protocol Performance 
%       Using Inter-link Reception Correlation. In the ACM Mobicom 2010. 
% 
% Copyright @ Pablo Soldati 2011.

% Reshape the trace files in case of different length
if length(trace_x)~= length(trace_y)
    M = min(length(trace_x), length(trace_y));
    trace_x = trace_x(1:M);
    trace_Y = trace_y(1:M);
end
trace_xy = trace_x.*trace_y;


P_x  = mean(trace_x);    % The mean of the trace X corresponds to the PRR of the corresponding link
P_y  = mean(trace_y);    % The mean of the trace Y corresponds to the PRR of the corresponding link
P_xy = mean(trace_xy);   % P^{t}_{xy}(1,1): probability that both nodes X and Y receive the same packet

sigma_x = sqrt(P_x*(1-P_x));
sigma_y = sqrt(P_y*(1-P_y));

% Compute the correlation metric \rho, \rho_max, and \rho_min basd on
% equations (3), (4) and (5) from [1], respectively
if (sigma_x*sigma_y)~=0,
    rho_txy = (P_xy-P_x*P_y)/(sqrt(sigma_x*sigma_y));
    rho_max = (min(P_x,P_y)-P_x*P_y)/(sqrt(sigma_x*sigma_y));
    if P_x + P_y <= 1,        
        rho_min = -P_x*P_y/(sqrt(sigma_x*sigma_y));
    else 
        rho_min = (P_x+P_y-1-P_x*P_y)/(sqrt(sigma_x*sigma_y));
    end
else
    rho_txy = 0;
end

if rho_txy > 0,
    kappa_txy = rho_txy/rho_max;
elseif rho_txy < 0,
    kappa_txy = -rho_txy/rho_min;
else
    kappa_txy = 0;
end

xx = kappa_txy;
return;
