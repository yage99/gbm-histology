function output = removedump(input)

i = 1;
while i < size(input, 1)
    current = input{i, 1};
    if strcmp(current, input{i+1, 1})
        input(i+1, :) = [];
        i = i - 1;
    end
    i = i + 1;
end

output = input;

end