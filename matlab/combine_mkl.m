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

histology_feature_indc = mrmr_miq_d(histology_data, class, 15);
histology_data = histology_data(:, histology_feature_indc);

data = [tcga_data, histology_data];
kernel = {'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian' ...
          'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian'};
%kernel = {'gaussian' 'gaussian' 'gaussian'};
params = [0.5 1 2 5 7 10 12 15 17 20]; %2^-10:10;
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
             'random' 'random' 151:165 151:165};


rowDist = cell(10, 1);
for i=1:10
    [rowDist{i}, weight] = ...
        mklclassify(data(indcs~=i, :), class(indcs~=i), ...
                    data(indcs==i,:), class(indcs==i), 300, ...
                    kernel, kerneloptionvect, variablevec); %#ok
    weight
end
result = cell2mat(rowDist);
result(pos) = result;

fastAUC(class == 1, result)
