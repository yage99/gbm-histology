addpath(genpath('~/Documents/MATLAB/tools/'));
addpath(genpath('./simplemkl'));

data_cna = readtable('../source/data_linear_CNA.txt', 'TreatAsEmpty', ...
                     'NA');
data_cna = rotate_table(data_cna);
data_cna_origin = readtable('../data/cbioportal/data_CNA.txt', 'TreatAsEmpty', ...
                     'NA');
data_cna_origin = rotate_table(data_cna_origin);
%data_exp = readtable('../source/data_expression_Zscores.txt', 'TreatAsEmpty', ...
%                     'NA');
%data_exp = rotate_table(data_exp);

clinical = readtable('../source/clinical.csv');

[result_cna_mrmr_all, ~, feature_indc] = copy_number_main(data_cna, clinical, 0, 'mrmr');
