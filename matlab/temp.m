histology_feature_indc = mrmr_miq_d(histology_data, class, 10);
data = histology_data(:, histology_feature_indc);
rowDist = cell(10, 1);
parfor i=1:10
    [rowDist{i}, ~] = ...
        mklclassify(data(indcs~=i, :), class(indcs~=i), ...
                    data(indcs==i,:), class(indcs==i)); %#ok
end
result = cell2mat(rowDist);
result(pos) = result;

