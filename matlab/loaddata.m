function [histology_cell, histology_cytoplasm, histology_nulei,...
          clinical, data_expression, data_cna, data_mrna] = ...
        loaddata()

histology_cell = readtable('../source/cell.csv');
histology_cytoplasm = readtable('../source/cytoplasm.csv');
histology_nulei = readtable('../source/nulei.csv');

clinical = readtable('../source/clinical.csv');

data_expression = ...
    readtable('../source/data_expression_Zscores.txt');
% TODO: change to zscore
data_cna = readtable('../source/data_linear_CNA.txt');
data_mrna = readtable('../source/data_mRNA_median_Zscores.txt');

keeps = true(height(clinical), 1);
[keeps] = delnan(histology_cell, keeps);
[keeps] = delnan(histology_cytoplasm, keeps);
[keeps] = delnan(histology_nulei, keeps);
[keeps] = delnan(data_expression, keeps);
[keeps] = delnan(data_cna, keeps);
[keeps] = delnan(data_mrna, keeps);

histology_cell = histology_cell(keeps, :);
histology_cytoplasm = histology_cytoplasm(keeps, :);
histology_nulei = histology_nulei(keeps, :);
clinical = clinical(keeps, :);
data_expression = data_expression(keeps, :);
data_cna = data_cna(keeps, :);
data_mrna = data_mrna(keeps, :);

end