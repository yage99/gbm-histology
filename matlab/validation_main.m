addpath(genpath('~/Documents/MATLAB/tools/'));
addpath(genpath('./simplemkl'));

if ~exist('source', 'var')
    source = loadsource();
    load validation_patients.mat
    max_improve = 0;
end

%% load data
histology_cell = source.histology_cell;
histology_cytoplasm = source.histology_cytoplasm;
histology_nuclei = source.histology_nuclei;
clinical = source.clinical;
data_expression = source.data_expression;
data_cna = source.data_cna;
data_mrna = source.data_mrna;

[~, ~, patients] = match(histology_cell{:,1}, clinical{:,1});
[~, ~, patients] = match(data_expression{:,1}, patients);
[~, ~, patients] = match(data_cna{:,1}, patients);
[~, ~, patients] = match(data_mrna{:, 1}, patients);

patients = sort(patients);
%[valid_indc, ~] = match(patients, common_patients);
%filter = false(size(patients));
%filter(valid_indc) = true;

[~, indc] = match(patients, clinical{:, 1});
clinical = clinical(indc, :);
[~, indc] = match(patients, histology_cell{:, 1});
histology_cell = histology_cell(indc, :);
histology_cytoplasm = histology_cytoplasm(indc, :);
histology_nuclei = histology_nuclei(indc, :);
[~, indc] = match(patients, data_expression{:, 1});
data_expression = data_expression(indc, :);
[~, indc] = match(patients, data_cna{:, 1});
data_cna = data_cna(indc, :);
[~, indc] = match(patients, data_mrna{:, 1});
data_mrna = data_mrna(indc, :);

histology_cell{:,2:end} = normalizemeanstd(histology_cell{:,2:end});
histology_cytoplasm{:,2:end} = ...
    normalizemeanstd(histology_cytoplasm{:,2:end});
histology_nuclei{:,2:end} = ...
    normalizemeanstd(histology_nuclei{:,2:end});
data_expression{:,2:end} = ...
    normalizemeanstd(data_expression{:,2:end});
data_cna{:,2:end} = normalizemeanstd(data_cna{:,2:end});
data_mrna{:,2:end} = normalizemeanstd(data_mrna{:,2:end});

%% data preprocess
source_class = clinical{:,2} > 365*2;
source_class = source_class * 2 - 1;

tcga_data = [data_expression{:, 2:end}, data_cna{:, 2:end}, ...
             data_mrna{:, 2:end}];
%tcga_data = [data_expression, data_cna, ...
%             data_mrna, data_meth];
tcga_data(tcga_data > 2) = 0;
tcga_data(tcga_data < -2) = 0;
tcga_feature_indc = mrmr_miq_d(tcga_data, source_class, 290);
tcga_data = tcga_data(:, tcga_feature_indc);

overall_result = struct('combined', {}, 'tcga', {}, 'histology', {},...
                        'kernel1', {}, 'kernel2', {});
histology_data = [histology_cell{:, 2:end}, histology_cytoplasm{:, 2:end}, histology_nuclei{:, 2:end}];

histology_data(histology_data > 2) = 0;
histology_data(histology_data < -2) = 0;
histology_feature_indc = mrmr_miq_d(histology_data, source_class, 50);
histology_data = histology_data(:, histology_feature_indc);

positive_count = sum(source_class + 1) / 2;
positive_indc = crossvalind('Kfold', positive_count, 10);
negative_indc = crossvalind('Kfold', ...
                    length(source_class) - positive_count, 10);
[~, sort_indc] = sort(source_class);
indcs = [negative_indc; positive_indc];
indcs(sort_indc) = indcs;

filter = false(size(source_class));
filter(indcs==10) = true;
histology_train = histology_data(~filter, :);
histology_test = histology_data(filter, :);
class_train = source_class(~filter, :);
class_test = source_class(filter, :);
tcga_train = tcga_data(~filter, :);
tcga_test = tcga_data(filter, :);

positive_count = sum(class_train + 1) / 2;
positive_indc = crossvalind('Kfold', positive_count, 10);
negative_indc = crossvalind('Kfold', ...
                    length(class_train) - positive_count, 10);
[~, sort_indc] = sort(class_train);
indcs = [negative_indc; positive_indc];
indcs(sort_indc) = indcs;

iteration = 100;
results = zeros(iteration, 1);
for k = 1:iteration
    kernel = {'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian' ...
              'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian'};
    %kernel = {'gaussian' 'gaussian' 'gaussian'};

    params = [0.001 0.002 0.005 0.01 0.05 0.1 0.25 0.5 1 2 5 7 10 12 15 17 20]; %2^-10:10;
    kerneloptionvect = {params params params params params params params ...
                        params params params};
    variablevec={'random' 'random' 'random' 'random' 'random' 'random' ...
    'random' 'random' 'random' 'random'};
    % fixed kernel
    % kerneloptionvect = {[0.5 1 2 5 7 10 12 15 17 20] [0.5 1 2 5 7 10 12 15 ...
    %                      17 20] [0.5 1 2 5 7 10 12 15 17 20]};
    % variablevec={'random' 'random' 'random' 'random' 'random' 'random' ...
    %          'all' 1:cell_count cell_count+1:cyto_count ...
    %          cyto_count+1:nuclei_count}
    % variablevec = {1:cell_count cell_count+1:cyto_count ...
    %                cyto_count+1:nuclei_count};

    [kernel1, kerneloptionvect1, variableveccell1] = ...
        CreateKernelListWithVariable(variablevec, size(tcga_train, 2),...
                                     kernel, kerneloptionvect);
    [kernel2, kerneloptionvect2, variableveccell2] = ...
        CreateKernelListWithVariable(variablevec, size(histology_train, 2), ...
                                     kernel, kerneloptionvect);

    kernel = [kernel1 kernel2];
    kerneloptionvect = [kerneloptionvect1 kerneloptionvect2];

    experiment.kernel1 = variableveccell1;
    experiment.kernel2 = variableveccell2;
    % experiment.kernel1 = bestexperiment.kernel1;
    % experiment.kernel2 = bestexperiment.kernel2;

    %variableveccell = bestkernel;
    
    %% tcga feature
    % data = tcga_data;
    % parfor i=1:10
    %     [rowDist{i}, ~] = ...
    %         mklclassify(data(indcs~=i,:), class(indcs~=i), ...
    %                     data(indcs==i,:), class(indcs==i), 300,...
    %                     kernel, kerneloptionvect, experiment.kernel1, 0); %#ok
    % end
    % result = cell2mat(rowDist);
    % result(pos) = result;
    % 

    %result = cross_valid(tcga_train, class_train, indcs, kernel, kerneloptionvect, experiment.kernel1, 0);
    %experiment.tcga = fastAUC(class_train == 1, result, 1, 'tcga', 0);
    
    %% histology feature
    %result = cross_valid(histology_train, class_train, indcs, kernel, kerneloptionvect, experiment.kernel2, 5000);
    %experiment.histology = fastAUC(class_train == 1, result, 1, 'histology', 0);
    
    %% combined feature
    for cellidx = 1:length(variableveccell2)
        variableveccell2{cellidx} = experiment.kernel2{cellidx} + size(tcga_train, 2);
    end
    variableveccell = [experiment.kernel1 variableveccell2];
    %result = cross_valid([tcga_train, histology_train], class_train, indcs, kernel, ...
    %        kerneloptionvect, variableveccell, 0);
    %experiment.combined = fastAUC(class_train == 1, result, 1, 'combined', 0);
    [predict, weights] = ...
        mklclassify([tcga_train, histology_train], class_train, ...
                    [tcga_test, histology_test], class_test, 300,...
                    kernel, kerneloptionvect, variableveccell, 0);
    results(k) = fastAUC(class_test == 1, predict, 1, 'valid', 0);
    
end
