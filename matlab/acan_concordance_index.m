function [ci] = acan_concordance_index(targets, predicts)
  [~,i] = sort(targets,'descend');
  predicts = predicts(i);
  n = length(targets);
  total  = 0;
  norm_z = 0;
  for j=1:n
      for k=j:n
          if j ~= k
              h = step_function(predicts(j) - predicts(k));
              total = total + h;
              norm_z = norm_z + 1;
          end
      end
  end
  ci = total / norm_z;
end
 function h = step_function(diff)
    if diff > 0
        h = 1;
    elseif diff == 0
        h = 0.5;
    else
        h = 0;
    end
 end