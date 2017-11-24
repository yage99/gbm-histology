function [histology_cell, histology_cytoplasm, histology_nulei,...
          clinical, data_expression, data_cna, data_mrna] = ...
        loaddata()

histology_cell = readtable('../source/cell.csv', 'TreatAsEmpty', 'NA');
histology_cytoplasm = readtable('../source/cytoplasm.csv');
histology_nulei = readtable('../source/nulei.csv');

clinical = readtable('../source/clinical.csv');

data_expression = readtable('../source/data_expression_Zscores.txt', ...
                            'TreatAsEmpty', 'NA');
% TODO: change to zscore
data_cna = readtable('../source/data_linear_CNA.txt');
data_mrna = readtable('../source/data_mRNA_median_Zscores.txt', ...
                      'TreatAsEmpty', 'NA');

keeps = true(height(clinical), 1);
[keeps] = delnan(histology_cell, keeps);
[keeps] = delnan(histology_cytoplasm, keeps);
[keeps] = delnan(histology_nulei, keeps);
[keeps] = delnan(data_expression, keeps);
[keeps] = delnan(data_cna, keeps);
[keeps] = delnan(data_mrna, keeps);

histology_cell = histology_cell(keeps, :);
histology_cell{:,2:end} = normalizemeanstd(histology_cell{:,2:end});
histology_cytoplasm = histology_cytoplasm(keeps, :);
histology_cytoplasm{:,2:end} = ...
    normalizemeanstd(histology_cytoplasm{:,2:end});
histology_nulei = histology_nulei(keeps, :);
histology_nulei{:,2:end} = ...
    normalizemeanstd(histology_nulei{:,2:end});
clinical = clinical(keeps, :);
data_expression = data_expression(keeps, :);
data_expression{:,2:end} = ...
    normalizemeanstd(data_expression{:,2:end});
data_cna = data_cna(keeps, :);
data_cna{:,2:end} = normalizemeanstd(data_cna{:,2:end});
data_mrna = data_mrna(keeps, :);
data_mrna{:,2:end} = normalizemeanstd(data_mrna{:, 2:end});

end