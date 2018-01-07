addpath(genpath('~/Documents/MATLAB/tools/'))

if ~exist('clinical', 'var')
    echo "loading data"
    [histology_cell, histology_cytoplasm, histology_nulei, ...
     clinical, data_expression, data_cna, data_mrna] = loaddata();

    class = clinical{:,2} > 365*2;
    class = class * 2 - 1;

    tcga_data = [data_expression{:,2:end}, data_cna{:, 2:end}, ...
                 data_mrna{:,2:end}];
    tcga_data(tcga_data > 2) = 0;
    tcga_data(tcga_data < -2) = 0;
    tcga_feature_indc = mrmr_miq_d(tcga_data, class, 150);
    tcga_data = tcga_data(:, tcga_feature_indc);

    histology_data = [histology_cell{:,2:end}, histology_cytoplasm{:,2: ...
                        end},histology_nulei{:,2:end}];
    histology_data(histology_data > 2) = 0;
    histology_data(histology_data < -2) = 0;
    histology_feature_indc = mrmr_miq_d(histology_data, class, 150);
    histology_data = histology_data(:, histology_feature_indc);

    indcs = crossvalind('Kfold', length(class), 10);
    [~, pos] = sort(indcs);
end

data = [tcga_data, histology_data];

rowDist = cell(10, 1);
parfor i=1:10
    [rowDist{i}, ~] = ...
        mklclassify(data(indcs~=i, :), class(indcs~=i), ...
                    data(indcs==i,:), class(indcs==i), 300); %#ok
end
result = cell2mat(rowDist);
result(pos) = result;

experiment.combined = fastAUC(class == 1, result);


data = tcga_data;
parfor i=1:10
    [rowDist{i}, ~] = ...
        mklclassify(data(indcs~=i,:), class(indcs~=i), ...
                    data(indcs==i,:), class(indcs==i), 300); %#ok
end
result = cell2mat(rowDist);
result(pos) = result;

experiment.tcga = fastAUC(class == 1, result);


data = histology_data;
parfor i=1:10
    [rowDist{i}, ~] = ...
        mklclassify(data(indcs~=i,:), class(indcs~=i), ...
                    data(indcs==i,:), class(indcs==i), 300); %#ok
end
result = cell2mat(rowDist);
result(pos) = result;

experiment.histology = fastAUC(class == 1, result);

experiment %#ok
