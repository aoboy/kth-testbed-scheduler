% Analysis of Task 1;
clear all; close all;
NoNodes = 32; NoLinks = 31;
Channel_case(1).chID = 15;
Channel_case(2).chID = 20;
Channel_case(3).chID = 25;
Channel_case(4).chID = 26;
Channel_case(5).chID = [15 20];
Channel_case(6).chID = [15 20 25 26];
no_cases = 6; trials = [1:7 9:14 16:15 27:30 33:38 41:43 45:87 89:94 96:100]; no_trials = length(trials);
for jj = 1:no_cases,
    if length(Channel_case(jj).chID)==1,
        file_name   = sprintf('KTH_Task%d_SingleChannel%d',1, Channel_case(jj).chID);
    elseif length(Channel_case(jj).chID)==2,
        file_name = sprintf('KTH_Task%d_TSCH_Sequence%d_%d',1, Channel_case(jj).chID);   
    elseif length(Channel_case(jj).chID)==4,
        file_name = sprintf('KTH_Task%d_TSCH_Sequence%d_%d_%d_%d',1,Channel_case(jj).chID);
    end
    
    load(file_name)
    Stats(jj).beta_mat    = zeros(31,no_trials);
    Stats(jj).AvgPsuc_mat = zeros(31,no_trials);
    
    no_kappa = length(AllStats(1).net_stats.AllKappa);
    Stats(jj).kappa_mat = zeros(no_kappa, no_trials);

    for ii = 1:length(trials),
        trial = trials(ii);
        Stats(jj).beta_mat(:, trial)    = AllStats(trial).net_stats.AllBeta;
        Stats(jj).kappa_mat(:, trial)   = AllStats(trial).net_stats.AllKappa';
        Stats(jj).AvgPsuc_mat(:, trial) = AllStats(trial).net_stats.AllAvgPrSucc;
    end
    clear('AllStats')
end


%% Plot mean beta for each link on the 6 cases (4 single channel and 2 TSCH sequences)
mean_beta = [];
for jj =1:no_cases,
    mean_beta = [mean_beta mean(Stats(jj).beta_mat,2) ];
end

figure(1)
plot([1:6 8:32], mean_beta(:,1),'*')
hold on
plot([1:6 8:32], mean_beta(:,2),'s')
hold on
plot([1:6 8:32], mean_beta(:,5),'ok')
%
hold on
plot([1:6 8:32], mean_beta(:,3),'d')
hold on
plot([1:6 8:32], mean_beta(:,4),'>')
hold on
plot([1:6 8:32], mean_beta(:,6),'<k')
grid on;
legend('Channel 15', 'Channel 20', 'Channel hopping 15-20', 'Channel 25', 'Channel 26', 'Channel hopping 15-20-25-26');
xlabel('Receiver ID')
ylabel('AveraGe \beta')

%% Compute beta CDF over all experiments
kappa_range = [-1 1];
beta_range  = kappa_range;
for jj = 1:no_cases,
    [n1 n2]  = size(Stats(jj).beta_mat);
    Psuc_vec = reshape(Stats(jj).AvgPsuc_mat, 1 , n1*n2);
    beta_vec = reshape(Stats(jj).beta_mat, 1 , n1*n2);
    pos_index = find(Psuc_vec>0);
    beta_vec = beta_vec(pos_index);
    [Stats(jj).Beta_CDF.CDF Stats(jj).Beta_CDF.range_samples] = EmpiricalCDF(beta_vec, beta_range);

%     [Stats(jj).Kappa_CDF.CDF Stats(jj).Kappa_CDF.range_samples] = EmpiricalCDF(Kappa_vec, kappa_range);
end
keyboard;
figure(2)
for jj=1:no_cases,
    if jj==1
        plot(Stats(jj).Beta_CDF.range_samples, Stats(jj).Beta_CDF.CDF, '-', 'Linewidth', 2, 'Color', 0.2.*[1 1 1]) 
        hold on
    elseif jj == 2
        plot(Stats(jj).Beta_CDF.range_samples, Stats(jj).Beta_CDF.CDF, '-', 'Linewidth', 2, 'Color', 0.4.*[1 1 1]) 
        hold on
    elseif jj == 3
        plot(Stats(jj).Beta_CDF.range_samples, Stats(jj).Beta_CDF.CDF, '-', 'Linewidth', 2, 'Color', 0.6.*[1 1 1]) 
        hold on
    elseif jj == 4
        plot(Stats(jj).Beta_CDF.range_samples, Stats(jj).Beta_CDF.CDF, '-', 'Linewidth', 2, 'Color', 0.8.*[1 1 1]) 
        hold on
    elseif jj == 5
        plot(Stats(jj).Beta_CDF.range_samples, Stats(jj).Beta_CDF.CDF, '--', 'Linewidth', 2, 'Color', 0.*[1 1 1]) 
        hold on
    elseif jj == 6
        plot(Stats(jj).Beta_CDF.range_samples, Stats(jj).Beta_CDF.CDF, '-.', 'Linewidth', 2, 'Color', 0.*[1 1 1]) 
        hold on
    end
end
grid on;
xlabel('\beta')
ylabel('CDF')
legend('Channel 15', 'Channel 20', 'Channel 25', 'Channel 26', 'Channel hopping 15-20', 'Channel hopping 15-20-25-26');

        
   
        
        
%% Analyze average success probality
figure(3)
plot([1:6 8:32], Stats(6).AvgPsuc_mat(:,:),'k+')
xlabel('Receiver ID')
ylabel('Links PRR')
title('Transmitter ID = 7, TSCH seq. \{15 20 25 26\}')
axis([1 32 0 1])

AvgLinksPRR = zeros(NoLinks, no_cases);
for jj=1:no_cases,
    AvgLinksPRR(:,jj) = mean(Stats(jj).AvgPsuc_mat,2);
    %AvgLinksPRR(:,2*jj)   = NaN;
end

figure(4)
bar3(AvgLinksPRR', 0.3)
set(gca,'YTickLabel', {'Channel 15', 'Channel 20', 'Channel 25', 'Channel 26', 'TSCH 15-20', 'TSCH 15-20-25-26'})
set(gca,'XTickLabel', {'5', '11', '16','21','26','31'})

xlabel('Receiver ID')
zlabel('Average Links PRR')


figure(5)
PRR_Link_71_seq1 = [Stats(1).AvgPsuc_mat(1,1) Stats(2).AvgPsuc_mat(1,1) Stats(3).AvgPsuc_mat(1,1) Stats(4).AvgPsuc_mat(1,1) Stats(5).AvgPsuc_mat(1,1) Stats(6).AvgPsuc_mat(1,1)];
PRR_Link_71_seq2 = [Stats(2).AvgPsuc_mat(1,5) Stats(2).AvgPsuc_mat(1,5) Stats(3).AvgPsuc_mat(1,5) Stats(4).AvgPsuc_mat(1,5) Stats(5).AvgPsuc_mat(1,5) Stats(6).AvgPsuc_mat(1,5)];
PRR_Link_71_seq3 = [Stats(2).AvgPsuc_mat(1,10) Stats(2).AvgPsuc_mat(1,10) Stats(3).AvgPsuc_mat(1,10) Stats(4).AvgPsuc_mat(1,10) Stats(5).AvgPsuc_mat(1,10) Stats(6).AvgPsuc_mat(1,10)];
PRR_Link_71_seq4 = [Stats(2).AvgPsuc_mat(1,20) Stats(2).AvgPsuc_mat(1,20) Stats(3).AvgPsuc_mat(1,20) Stats(4).AvgPsuc_mat(1,20) Stats(5).AvgPsuc_mat(1,20) Stats(6).AvgPsuc_mat(1,20)];
PRR_Link_71_seq5 = [Stats(2).AvgPsuc_mat(1,50) Stats(2).AvgPsuc_mat(1,50) Stats(3).AvgPsuc_mat(1,50) Stats(4).AvgPsuc_mat(1,50) Stats(5).AvgPsuc_mat(1,50) Stats(6).AvgPsuc_mat(1,50)];

plot(PRR_Link_71_seq1,'*', 'Color', 0.*[1 1 1], 'MarkerSize', 10)
hold on
plot(PRR_Link_71_seq2,'s', 'Color', 0.*[1 1 1], 'MarkerSize', 10)
hold on
plot(PRR_Link_71_seq3,'d', 'Color', 0.*[1 1 1], 'MarkerSize', 10)
hold on
plot(PRR_Link_71_seq4,'o', 'Color', 0.*[1 1 1], 'MarkerSize', 10)
hold on
plot(PRR_Link_71_seq5,'>', 'Color', 0.*[1 1 1], 'MarkerSize', 10)
grid on;
set(gca,'XTickLabel', {'Ch. 15', '',  'Ch. 20','', 'Ch. 25','', 'Ch. 26', '','TSCH 15-20', '','TSCH all'})
xlabel('Channels')
ylabel('PRR for link 7-1')
legend('Trial 1', 'Trial 5', 'Trial 10', 'Trial 20', 'Trial 50')



