function [results, bestresult, feature_indc] = copy_number_main(data_cna, clinical, mrmr, runname)

[filter1, filter2, ~] = match(clinical{:, 1}, data_cna{:, 1});
clinical = clinical(filter1, :);
data_cna = data_cna(filter2, :);
%% data preprocess
source_class = clinical{:,2} > 365*2;
source_class = source_class * 2 - 1;

positive_count = sum(source_class + 1) / 2;
positive_indc = crossvalind('Kfold', positive_count, 10);
negative_indc = crossvalind('Kfold', ...
                    length(source_class) - positive_count, 10);

[~, sort_indc] = sort(source_class);

indcs = [negative_indc; positive_indc];% crossvalind('Kfold', length(source_class), 10);
indcs(sort_indc) = indcs;

data = normalizemeanstd(data_cna{:,2:end});
data(data > 2) = 0;
data(data < -2) = 0;
if mrmr
    feature_indc = mrmr_miq_d(data, source_class, mrmr);
    data = data(:, feature_indc);
else
    feature_indc = 1:size(data, 2);
end
iteration = 10;

results = zeros(iteration, 2);
max_auc = 0;
bestresult = 0;
for k = 1:iteration
    params = [0.001 0.002 0.005 0.01 0.05 0.1 0.25 0.5 1 2 5 7 10 12 15 17 20]; %2^-10:10;

    kernel = {'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian' ...
              'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian'};
    kerneloptionvect = {params params params params params params params ...
                        params params params};
    variablevec={'random' 'random' 'random' 'random' 'random' 'random' ...
    'random' 'random' 'random' 'random'};
    %kernel = {'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian'};
    %kerneloptionvect = {params params params params params};
    %variablevec={'random' 'random' 'random' 'random' 'random'};

    [kernel1, kerneloptionvect1, variableveccell1] = ...
        CreateKernelListWithVariable(variablevec, size(data, 2),...
                                     kernel, kerneloptionvect);

    result = cross_valid(data, source_class, indcs, kernel1, kerneloptionvect1, variableveccell1, 0);
    if exist('runname', 'var')
        results(k, 1) = fastAUC(source_class == 1, result, 1, runname, 0);
    else
        results(k, 1) = fastAUC(source_class == 1, result, 0, 'yjh', 0);
    end
    results(k, 2) = acan_concordance_index(source_class, result);
    k %#ok
    fprintf('auc %f\n', results(k, 1));
    fprintf('cindex %f\n', results(k, 2));

    if max_auc < results(k, 1)
        bestresult = [clinical{:, 2}, result];
    end

%     if max_improve < experiment.combined - experiment.tcga
%         bestexperiment = experiment;
%         max_improve = experiment.combined - experiment.tcga;
%     end
end

% for i=1:iteration
%     overall_result(i)
% end

end
