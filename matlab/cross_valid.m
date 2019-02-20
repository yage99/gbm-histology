function [result, weights] = cross_valid(data, class, indcs, kernel, kerneloptionvect, kernelvariable, P)
    rowDist = cell(10, 1);

    %% tcga feature
    parfor i=1:10
        [rowDist{i}, weights] = ...
            mklclassify(data(indcs~=i,:), class(indcs~=i), ...
                        data(indcs==i,:), class(indcs==i), 300,...
                        kernel, kerneloptionvect, kernelvariable, P); %#ok
    end
    result = cell2mat(rowDist);
    [~, pos] = sort(indcs);
    result(pos) = result;
end
