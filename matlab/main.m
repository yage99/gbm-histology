addpath(genpath('~/Documents/MATLAB/tools/'))

if ~exist('clinical')
    [histology_cell, histology_cytoplasm, histology_nulei, ...
     clinical, data_expression, data_cna, data_mrna] = loaddata();
end

class = clinical{:,2} > 365*2;
class = class*2 - 1;

data = [data_expression{:,2:end}, data_cna{:, 2:end}, data_mrna{:, ...
                    2:end}];
feature_indc = mrmr_miq_d(data, class, 100);



