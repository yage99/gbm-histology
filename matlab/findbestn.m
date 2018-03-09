auc = zeros(10,1);
histology_data = [histology_cell, histology_cytoplasm, histology_nulei];
histology_data(histology_data > 2) = 0;
histology_data(histology_data < -2) = 0;
for n = 10:10:200
    histology_feature_indc = mrmr_miq_d(histology_data, class, n);
    data = histology_data(:, histology_feature_indc);
    %% histology feature
    parfor i=1:10
        [rowDist{i}, ~] = ...
            mklclassify(data(indcs~=i,:), class(indcs~=i), ...
                        data(indcs==i,:), class(indcs==i)); %#ok
    end
    result = cell2mat(rowDist);
    result(pos) = result;
    
    auc(n/10) = fastAUC(class == 1, result);
end
auc
