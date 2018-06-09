function [histology_cell, histology_cytoplasm, histology_nulei,...
          clinical, data_expression, data_cna, data_mrna, data_meth] = ...
        loaddata(source, include_meth)

histology_cell = readtable('../source/cell.csv', 'TreatAsEmpty', ...
                           'NA');
% histology_cell{:, 2:end} = str2double(histology_cell{:, 2:end});
histology_cytoplasm = readtable('../source/cytoplasm.csv', ...
                                'TreatAsEmpty', 'NA');
% histology_cytoplasm{:, 2:end} = str2double(histology_cytoplasm{:, ...
%                    2:end});
histology_nulei = readtable('../source/nulei.csv', 'TreatAsEmpty', ...
                            'NA');
%histology_nulei{:, 2:end} = str2double(histology_nulei{:, 2:end});

clinical = source.clinical;%readtable('../source/clinical.csv');

data_expression = source.data_expression;
%readtable('../source/data_expression_Zscores.txt', ...
                  %          'TreatAsEmpty', 'NA');
%data_expression = rotate_table(data_expression);
% TODO: change to zscore source data
data_cna = source.data_cna;
% data_cna = readtable('../source/data_linear_CNA.txt', 'TreatAsEmpty', ...
%                      'NA');
% data_cna = rotate_table(data_cna);
data_mrna = source.data_mrna;
% data_mrna = readtable('../source/data_mRNA_median_Zscores.txt', ...
%                       'TreatAsEmpty', {'NA'});
% data_mrna = rotate_table(data_mrna);
if include_meth
    data_meth = source.data_meth;
else
    data_meth = [];
end

keeps = true(height(clinical), 1);
[keeps, histology_cell] = delnan(histology_cell, keeps, clinical);
[keeps, histology_cytoplasm] = delnan(histology_cytoplasm, keeps, clinical);
[keeps, histology_nulei] = delnan(histology_nulei, keeps, clinical);
[keeps, data_expression] = delnan(data_expression, keeps, clinical);
[keeps, data_cna] = delnan(data_cna, keeps, clinical);
[keeps, data_mrna] = delnan(data_mrna, keeps, clinical);
if include_meth
    [keeps, data_meth] = delnan(data_meth, keeps, clinical);
end

clinical(~keeps, :) = [];
histology_cell(~keeps, :) = [];
histology_cytoplasm(~keeps, :) = [];
histology_nulei(~keeps, :) = [];
data_expression(~keeps, :) = [];
data_cna(~keeps, :) = [];
data_mrna(~keeps, :) = [];
if include_meth
    data_meth(~keeps, :) = [];
end

histology_cell = normalizemeanstd(histology_cell);
histology_cytoplasm = ...
    normalizemeanstd(histology_cytoplasm);
histology_nulei = ...
    normalizemeanstd(histology_nulei);
data_expression = ...
    normalizemeanstd(data_expression);
data_cna = normalizemeanstd(data_cna);
data_mrna = normalizemeanstd(data_mrna);
if include_meth
    data_meth = normalizemeanstd(data_meth);
end

end
