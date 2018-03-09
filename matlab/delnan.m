function [keeps, target] = delnan(input_table, keeps, clinical)

length = size(input_table);
% expand input table

clinical_length = size(clinical, 1);
this_keeps = false(clinical_length, 1);

target = zeros(clinical_length, size(input_table, 2) - 1);

for i = 1:length
    if sum(~isnan(input_table{i,2:end})) == 0
        continue;
    end
    for j = 1:clinical_length
        if this_keeps(j) == true || keeps(j) == false
            continue;
        end
        if strcmp(clinical{j, 1}, input_table{i, 1})
            target(j, :) = input_table{i, 2:end};
            this_keeps(j) = true;
            break;
        end
    end
end

keeps = keeps & this_keeps;

end
