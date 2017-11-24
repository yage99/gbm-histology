function [keeps] = delnan(input_table, keeps)

length = size(input_table);
for i = 1:length
    if isnan(table2array(input_table(i,2)))
        keeps(i) = false;
    end
end

end