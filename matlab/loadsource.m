function [source] = loadsource()
clinical = readtable('../source/clinical.csv');

data_expression = readtable('../source/data_expression_Zscores.txt', ...
                            'TreatAsEmpty', 'NA');
data_expression = rotate_table(data_expression);
% TODO: change to zscore source data
data_cna = readtable('../source/data_linear_CNA.txt', 'TreatAsEmpty', ...
                     'NA');
data_cna = rotate_table(data_cna);
data_mrna = readtable('../source/data_mRNA_median_Zscores.txt', ...
                      'TreatAsEmpty', {'NA'});
data_mrna = rotate_table(data_mrna);
data_meth= readtable('../source/data_methylation_hm27.txt', ...
                      'TreatAsEmpty', {'NA'});
data_meth = rotate_table(data_meth);

source.clinical = clinical;
source.data_expression = data_expression;
source.data_cna = data_cna;
source.data_mrna = data_mrna;
source.data_meth = data_meth;

end
