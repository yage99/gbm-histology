function [result] = parallelClassify(data, class, indcs)

[~, pos] = sort(indcs);
rowDist = cell(10, 1);
parfor i=1:10
    [temp, ~] = ...
        mklclassify(data(indcs~=i,:), class(indcs~=i), ...
                    data(indcs==i,:), class(indcs==i), 300);
    rowDist{i} = temp;
end
result = cell2mat(rowDist);
result(pos) = result;

end
