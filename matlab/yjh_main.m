addpath(genpath('~/Documents/MATLAB/tools/'));
addpath(genpath('./simplemkl'));

data_cna = readtable('../source/data_linear_CNA.txt', 'TreatAsEmpty', ...
                     'NA');
data_cna = rotate_table(data_cna);

clinical = readtable('../source/clinical.csv');



result_mrmr_20 = copy_number_main(data_cna, clinical, 20);