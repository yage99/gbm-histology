function [histology_cell, histology_cytoplasm, histology_nuclei,...
          clinical, data_expression, data_cna, data_mrna, data_meth] = ...
        loaddata(source, include_meth)

histology_cell = source.histology_cell; %readtable('../source/cell.csv', 'TreatAsEmpty', ...
                           %'NA');
% histology_cell{:, 2:end} = str2double(histology_cell{:, 2:end});
histology_cytoplasm = source.histology_cytoplasm; %readtable('../source/cytoplasm.csv', ...
                                %'TreatAsEmpty', 'NA');
% histology_cytoplasm{:, 2:end} = str2double(histology_cytoplasm{:, ...
%                    2:end});
histology_nuclei = source.histology_nuclei;%readtable('../source/nulei.csv', 'TreatAsEmpty', ...
                            %'NA');
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
    data_meth = source.data_meth{:, 1};
end

%keeps = true(height(clinical), 1);
[~, ~, patients] = match(histology_cell{:,1}, clinical{:,1});
[~, ~, patients] = match(data_expression{:,1}, patients);
[~, ~, patients] = match(data_cna{:,1}, patients);
[~, ~, patients] = match(data_mrna{:, 1}, patients);
if include_meth
    [~, ~, patients] = match(data_meth{:, 1}, patients);
end

patients = sort(patients);

[~, indc] = match(patients, clinical{:, 1});
clinical = clinical(indc, :);
[~, indc] = match(patients, histology_cell{:, 1});
histology_cell = histology_cell(indc, :);
histology_cytoplasm = histology_cytoplasm(indc, :);
histology_nuclei = histology_nuclei(indc, :);
[~, indc] = match(patients, data_expression{:, 1});
data_expression = data_expression(indc, :);
[~, indc] = match(patients, data_cna{:, 1});
data_cna = data_cna(indc, :);
[~, indc] = match(patients, data_mrna{:, 1});
data_mrna = data_mrna(indc, :);
if include_meth
    [~, indc] = match(patients, data_meth{:, 1});
    data_meth = data_meth(indc, :);
end

histology_cell{:,2:end} = normalizemeanstd(histology_cell{:,2:end});
histology_cytoplasm{:,2:end} = ...
    normalizemeanstd(histology_cytoplasm{:,2:end});
histology_nuclei{:,2:end} = ...
    normalizemeanstd(histology_nuclei{:,2:end});
data_expression{:,2:end} = ...
    normalizemeanstd(data_expression{:,2:end});
data_cna{:,2:end} = normalizemeanstd(data_cna{:,2:end});
data_mrna{:,2:end} = normalizemeanstd(data_mrna{:,2:end});
if include_meth
    data_meth{:,2:end} = normalizemeanstd(data_meth{:,2:end});
end

end
