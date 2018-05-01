kernel = {'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian' ...
          'gaussian' 'gaussian' 'gaussian' 'gaussian' 'gaussian'};

params = [0.001 0.002 0.005 0.01 0.05 0.1 0.25 0.5 1 2 5 7 10 12 15 17 20]; %2^-10:10;
kerneloptionvect = {params params params params params params params ...
                    params params params};
variablevec={'random' 'random' 'random' 'random' 'random' 'random' ...
'random' 'random' 'random' 'random'};

tcga_data = [data_expression, data_cna, ...
             data_mrna];
tcga_data(tcga_data > 2) = 0;
tcga_data(tcga_data < -2) = 0;
class = source_class;
tcga_feature_indc = mrmr_miq_d(tcga_data, class, 290);
tcga_data = tcga_data(:, tcga_feature_indc);

tcga_max = 0;
for j=1:10
    [kernel1, kerneloptionvect1, variableveccell1] = ...
        CreateKernelListWithVariable(variablevec, size(tcga_data, 2),...
                                     kernel, kerneloptionvect);

    data = tcga_data;
    parfor i=1:10
        [rowDist{i}, ~] = ...
            mklclassify(data(indcs~=i,:), class(indcs~=i), ...
                        data(indcs==i,:), class(indcs==i), 300,...
                        kernel, kerneloptionvect, kernel1); %#ok
    end
    result = cell2mat(rowDist);
    result(pos) = result;
    
    auc = fastAUC(class == 1, result, 1, 'tcga', 0);
    if auc > tcga_max
        tcga_max = auc;
        tcga_bestexperiment = kernel1;
    end
end
