addpath(genpath('~/Documents/MATLAB/tools/'));
addpath(genpath('./simplemkl'));

if ~exist('source', 'var')
    source = loadsource();
end

if ~exist('data_expression', 'var')
    [histology_cell, histology_cytoplasm, histology_nulei, ...
     clinical, data_expression, data_cna, data_mrna, data_meth] = loaddata(source, 0);

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
end

tcga_data = [data_expression{:, 2:end}, data_cna{:, 2:end}, ...
             data_mrna{:, 2:end}, data_meth{:, 2:end}];
tcga_data(tcga_data > 2) = 0;
tcga_data(tcga_data < -2) = 0;
class = source_class;
tcga_feature_indc = mrmr_miq_d(tcga_data, class, 290);
tcga_data = tcga_data(:, tcga_feature_indc);

overall_result = struct('combined', {}, 'tcga', {}, 'histology', {},...
                        'kernel1', {}, 'kernel2', {});
histology_data = [histology_cell{:, 2:end}, histology_cytoplasm{:, 2:end}, histology_nulei{:, 2:end}];
histology_data(histology_data > 2) = 0;
histology_data(histology_data < -2) = 0;
histology_feature_indc = mrmr_miq_d(histology_data, class, 50);
histology_data = histology_data(:, histology_feature_indc);
iteration = 10;

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
    %          cyto_count+1:nulei_count}
    % variablevec = {1:cell_count cell_count+1:cyto_count ...
    %                cyto_count+1:nulei_count};

    [kernel1, kerneloptionvect1, variableveccell1] = ...
        CreateKernelListWithVariable(variablevec, size(tcga_data, 2),...
                                     kernel, kerneloptionvect);
    [kernel2, kerneloptionvect2, variableveccell2] = ...
        CreateKernelListWithVariable(variablevec, size(histology_data, 2), ...
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

    %result = cross_valid(tcga_data, class, indcs, kernel, kerneloptionvect, experiment.kernel1, 0);
    %experiment.tcga = fastAUC(class == 1, result, 1, 'tcga', 0);
    
    %% histology feature
    result = cross_valid(histology_data, class, indcs, kernel, kerneloptionvect, experiment.kernel2, 5000);
    experiment.histology = fastAUC(class == 1, result, 1, 'histology', 0);
    acan_concordance_index(
    %% combined feature
    %for cellidx = 1:length(variableveccell2)
    %    variableveccell2{cellidx} = experiment.kernel2{cellidx} + size(tcga_data, 2);
    %end
    %variableveccell = [experiment.kernel1 variableveccell2];
    %result = cross_valid([tcga_data, histology_data], class, indcs, kernel, ...
    %        kerneloptionvect, variableveccell, 50000);
    %experiment.combined = fastAUC(class == 1, result, 1, 'combined', 0);
    
    k
    experiment
    overall_result(k) = experiment;

    if max_improve < experiment.combined - experiment.tcga
        bestexperiment = experiment;
        max_improve = experiment.combined - experiment.tcga;
    end
end

for i=1:iteration
    overall_result(i)
end
