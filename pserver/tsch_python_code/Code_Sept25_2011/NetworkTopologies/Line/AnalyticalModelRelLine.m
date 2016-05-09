function X = AnalyticalModelRelLine(N, deadline, LinkProb)
%% REL_INTERLEAVED_SCHEDULING (in Globecom2010): Given a line routing topology, with N
% nodes/links (gateway in N+1),a time deadline T>=N, and the link LOSS
% probabilities, compute the reliability.

No_Tx = deadline - N + 1;      % Number of transmission ajjempt per node

%% The transition Probability are stored in a matrix P\in N x No_tx
P = zeros(N, No_Tx);
P(1,1) = 1;                  % P_{1,0}

% Transition probability for the first link % P_{1,t} t=1,...,No_Tx-1
for jj=2:No_Tx,
    P(1,jj) = LinkProb(1).^(jj-1);     % Note that we use jj-1 since we start from index jj=1 and not jj=0.
end
% Transition probability P_{n,t} for n>1, t=1,...,No_Tx-1
for nn = 2:N,
    for jj = 1:No_Tx,
        if jj==1
            P(nn,1)  = (1-LinkProb(nn-1)).*P(nn-1,1);   % compute % P_{n,0}
        elseif jj>1,
            P(nn,jj) = (1-LinkProb(nn-1)).*P(nn-1,jj) + LinkProb(nn).*P(nn,jj-1);
        end
    end
end
X = sum((1-LinkProb(N)).*P(N,:)');     % Reliability