addpath(genpath('~/Documents/MATLAB/tools/'))

if ~exist('source', 'var')
    source = loadsource();
end

if ~exist('data_expression', 'var')
    [histology_cell, histology_cytoplasm, histology_nulei, ...
     clinical, data_expression, data_cna, data_mrna] = loaddata(source);

    %% data preprocess
    source_class = clinical{:,2} > 365*2;
    source_class = source_class * 2 - 1;

    indcs = crossvalind('Kfold', length(source_class), 10);
    [~, pos] = sort(indcs);

end

tcga_data = [data_expression, data_cna, ...
             data_mrna];
tcga_data(tcga_data > 2) = 0;
tcga_data(tcga_data < -2) = 0;
class = source_class;
tcga_feature_indc = mrmr_miq_d(tcga_data, class, 150);
tcga_data = tcga_data(:, tcga_feature_indc);

histology_data = [histology_cell, histology_cytoplasm, histology_nulei];
histology_data(histology_data > 2) = 0;
histology_data(histology_data < -2) = 0;

histology_feature_indc = mrmr_miq_d(histology_data, class, 20);
histology_data = histology_data(:, histology_feature_indc);

%% combined feature
data = [tcga_data, histology_data];

rowDist = cell(10, 1);
parfor i=1:10
    [rowDist{i}, ~] = ...
        mklclassify(data(indcs~=i, :), class(indcs~=i), ...
                    data(indcs==i,:), class(indcs==i)); %#ok
end
result = cell2mat(rowDist);
result(pos) = result;

experiment.combined = fastAUC(class == 1, result);

%% tcga feature
data = tcga_data;
parfor i=1:10
    [rowDist{i}, ~] = ...
        mklclassify(data(indcs~=i,:), class(indcs~=i), ...
                    data(indcs==i,:), class(indcs==i)); %#ok
end
result = cell2mat(rowDist);
result(pos) = result;

experiment.tcga = fastAUC(class == 1, result);

%% histology feature
data = histology_data;
parfor i=1:10
    [rowDist{i}, ~] = ...
        mklclassify(data(indcs~=i,:), class(indcs~=i), ...
                    data(indcs==i,:), class(indcs==i)); %#ok
end
result = cell2mat(rowDist);
result(pos) = result;

experiment.histology = fastAUC(class == 1, result);

experiment %#ok
