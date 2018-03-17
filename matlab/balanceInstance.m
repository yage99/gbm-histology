function [filter] = balanceInstance(class)

[class, index] = sort(class);

pos = sum(class == 1);
neg = sum(class == -1);

if pos > neg
    pick = neg;
else
    pick = pos;
end

pos_index = randperm(pos, pick) + neg;
neg_index = randperm(neg, pick);
picked = [pos_index neg_index];
origin_index = index(picked);

filter = false(size(class));
filter(origin_index) = true;

end
