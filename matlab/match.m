function [index1, index2, name] = match(input1, input2)

index1 = [];
index2 = [];
name = {};
count = 1;
for i = 1:length(input1)
    for j = 1:length(input2)
        if strcmp(input1{i}, input2{j})
            index1(count) = i;
            index2(count) = j;
            name{count} = input1{i};
            count = count + 1;
        end
    end
end

end