function [keeps] = delnan(input_table, keeps)

length = size(input_table);
for i = 1:length
    if sum(~isnan(input_table{i,2:end})) == 0
        keeps(i) = false;
    end
end

end