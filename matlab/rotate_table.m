function [newTable] = rotate_table(table)
    instance = table.Properties.VariableNames(3:end)';
    for i=1:length(instance)
        instance{i} = regexp(instance{i}, 'TCGA[-_]\w{2}[-_]\w{4}', 'match');
        instance{i} = strrep(instance{i}, '_', '-');
    end
    variable = table{:,1}';
    variable = [{'id'} variable];
    data = table{:, 3:end}';
    data = array2table(data);
    newTable = [instance data];
    newTable.Properties.VariableDescriptions = variable;
end
