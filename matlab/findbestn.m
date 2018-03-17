auc = zeros(10,1);
histology_data = [histology_cell, histology_cytoplasm, histology_nulei];%data_balanced;
data_class = source_class;%class_balanced;
% 
first = size(histology_cell, 2);
second = first + size(histology_cytoplasm, 2);
% 
histology_data(histology_data > 2) = 0;
histology_data(histology_data < -2) = 0;

parfor k = 1:10
    n = 5*k;
    histology_feature_indc = mrmr_miq_d(histology_data, data_class, n);
    data = histology_data(:, histology_feature_indc);
    [histology_feature_indc, sort_index] = sort(histology_feature_indc);
    data = data(:, sort_index);
    cell_count = sum(histology_feature_indc <= first);
    cyto_count = sum(histology_feature_indc <= second);
    nulei_count = size(histology_feature_indc, 2);
    %% histology feature
    result = zeros(size(data_class));
    kernel = {'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian' ...
          'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian'};
    kerneloptionvect = {[0.5 1 2 5 7 10 12 15 17 20] [0.5 1 2 5 7 10 12 ...
                    15 17 20] [5 7 10 12 15 17 20] [5 7 10 12 15 17 ...
                    20 ] [0.5 1 2 5 7 10 12 15 17 20] [0.5 1 2 5 7 ...
                    10 12 15 17 20] [0.5 1 2 5 7 10 12 15 17 20] ...
                    [0.5 1 2 5 7 10 12 15 17 20] [0.5 1 2 5 7 10 12 ...
                    15 17 20] [0.5 1 2 5 7 10 12 15 17 20]};
    variablevec={'random' 'random' 'random' 'random' 'random' 'random' ...
             'all' 1:cell_count cell_count+1:cyto_count ...
             cyto_count+1:nulei_count}
    variablevec
    % variablevec={'random' 'random' 'random' 'random' 'random' 'random' ...
    %          'random' 'random' 'all' 'single'};

    for i=1:10
        [result(indcs==i), ~] = ...
            mklclassify(data(indcs~=i,:), data_class(indcs~=i), ...
                        data(indcs==i,:), data_class(indcs==i), ...
                        300, kernel, kerneloptionvect, variablevec);
    end
    
    auc(k) = fastAUC(data_class == 1, result);
end
auc
