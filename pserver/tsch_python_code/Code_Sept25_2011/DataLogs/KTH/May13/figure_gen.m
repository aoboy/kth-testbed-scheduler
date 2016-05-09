%%
clear all; close all;

channels = [4 8 16];
no_cases = length(channels);
kappa_range = [-1 1];
beta_range  = kappa_range;


for ii=1:no_cases,
    no_ch = channels(ii);
    filename = sprintf('KTH_TSCH_%dChannels',no_ch);
    load(filename);
    
    Data(ii).Kappa_vec = Net_Stats.AllKappa;
    [Data(ii).Kappa_CDF.CDF Data(ii).Kappa_CDF.range_samples] = EmpiricalCDF(Data(ii).Kappa_vec, kappa_range);
    
    Data(ii).Beta_vec  = Net_Stats.AllBeta;
    [Data(ii).Beta_CDF.CDF Data(ii).Beta_CDF.range_samples] = EmpiricalCDF(Data(ii).Beta_vec, beta_range);
end

figure(1)
for ii = 1:no_cases,
    if ii==1,
        plot(Data(ii).Kappa_vec,'-s', 'Color', 0.*[1 1 1],'Linewidth', 2);
        hold on
    elseif ii==2,
        plot(Data(ii).Kappa_vec,'--o', 'Color', 0.3.*[1 1 1],'Linewidth', 2)
        hold on
    elseif ii==3,
    plot(Data(ii).Kappa_vec,'-.d', 'Color', 0.6.*[1 1 1],'Linewidth', 2)
    end
end
xlabel('link ID')
ylabel('\kappa')
legend('4 channels', '8 channels', '16 channels')

figure(2)
for ii = 1:no_cases,
    if ii==1,
        plot(Data(ii).Kappa_CDF.range_samples, 1-Data(ii).Kappa_CDF.CDF,'-', 'Color', 0.*[1 1 1],'Linewidth', 2);
        hold on
    elseif ii==2
        plot(Data(ii).Kappa_CDF.range_samples, 1-Data(ii).Kappa_CDF.CDF,'--', 'Color', (ii-1)*0.25*[1 1 1],'Linewidth', 2);
        hold on
    elseif ii ==3.
        plot(Data(ii).Kappa_CDF.range_samples, 1-Data(ii).Kappa_CDF.CDF,'-.', 'Color', (ii-1)*0.25*[1 1 1],'Linewidth', 2);
        hold on        
    end
end
% for ii = 1:no_cases,
%     if ii==1,
%         plot(Data(ii).Kappa_CDF.range_samples, 1-Data(ii).Kappa_CDF.CDF,'-', 'Color', 0.*[1 1 1],'Linewidth', 2);
%         hold on
%     else
%         plot(Data(ii).Kappa_CDF.range_samples, 1-Data(ii).Kappa_CDF.CDF,'-', 'Color', (ii-1)*0.25*[1 1 1],'Linewidth', 2);
%         hold on
%     end
% end
grid on;
xlabel('\kappa')
ylabel('Complemetary CDF')
legend('4 channels', '8 channels', '16 channels')


figure(3)
for ii = 1:no_cases,
    if ii==1,
        plot(Data(ii).Beta_CDF.range_samples, Data(ii).Beta_CDF.CDF,'-', 'Color', 0.*[1 1 1],'Linewidth', 2);
        hold on
    elseif ii==2,
        plot(Data(ii).Beta_CDF.range_samples, Data(ii).Beta_CDF.CDF,'--', 'Color', 0.3.*[1 1 1],'Linewidth', 2);
        hold on
    elseif ii==3,
        plot(Data(ii).Beta_CDF.range_samples, Data(ii).Beta_CDF.CDF,'-.', 'Color', 0.6*[1 1 1],'Linewidth', 2);
        hold on
    end
end
% for ii = 1:no_cases,
%     if ii==1,
%         plot(Data(ii).Beta_CDF.range_samples, Data(ii).Beta_CDF.CDF,'-', 'Color', 0.*[1 1 1],'Linewidth', 2);
%         hold on
%     else
%         plot(Data(ii).Beta_CDF.range_samples, Data(ii).Beta_CDF.CDF,'-', 'Color', (ii-1)*0.25*[1 1 1],'Linewidth', 2);
%         hold on
%     end
% end
grid on;
xlabel('\beta')
ylabel('CDF')
legend('4 channels', '8 channels', '16 channels')

