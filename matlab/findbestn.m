function [] = findbestn(data, class, indcs)
auc = zeros(10,1);
% histology_data = [histology_cell, histology_cytoplasm, histology_nulei];%data_balanced;
% data_class = source_class;%class_balanced;
% 
% first = size(histology_cell, 2);
% second = first + size(histology_cytoplasm, 2);
% 
data(data > 2) = 0;
data(data < -2) = 0;

parfor k = 1:10
    n = k+5;
    histology_feature_indc = mrmr_miq_d(data, class, n);
    % data = data(:, sort_index);
    loop_data = data(:, histology_feature_indc);
    % cell_count = sum(histology_feature_indc <= first);
    % cyto_count = sum(histology_feature_indc <= second);
    % nulei_count = size(histology_feature_indc, 2);
    %% histology feature
    result = zeros(size(class));
    kernel = {'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian' ...
          'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian'};
    %kernel = {'gaussian' 'gaussian' 'gaussian'};
    params = [0.001 0.002 0.005 0.01 0.05 0.1 0.25 0.5 1 2 5 7 10 12 15 17 20]; %2^-10:10;
    kerneloptionvect = {params params params params params params params ...
                        params params params};
    % kerneloptionvect = {[0.5 1 2 5 7 10 12 15 17 20] [0.5 1 2 5 7 10 12 15 ...
    %                      17 20] [0.5 1 2 5 7 10 12 15 17 20]};
    % variablevec={'random' 'random' 'random' 'random' 'random' 'random' ...
    %          'all' 1:cell_count cell_count+1:cyto_count ...
    %          cyto_count+1:nulei_count}
    % variablevec = {1:cell_count cell_count+1:cyto_count ...
    %                cyto_count+1:nulei_count};
    variablevec={'random' 'random' 'random' 'random' 'random' 'random' ...
                 'random' 'random' 'random' 'random'};

    for i=1:10
        [result(indcs==i), weight] = ...
            mklclassify(loop_data(indcs~=i,:), class(indcs~=i), ...
                        loop_data(indcs==i,:), class(indcs==i), ...
                        300, kernel, kerneloptionvect, variablevec);
        reshape(weight, length(weight) / length(kernel), length(kernel))
    end
    
    auc(k) = fastAUC(class == 1, result);
end
auc
end
