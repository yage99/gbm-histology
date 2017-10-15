import numpy

def loadCNV(file):
    """
data_linear_CNA.txt is recommended for this function.
"""
    with open(file) as f:
        firstLine = f.readline().split("\t")
        ncols = len(firstLine)
        ids = numpy.array(firstLine)[2:]
        
        matrix = numpy.loadtxt(file,
                               skiprows=1,
                               usecols=range(2, ncols-1))

        matrix = matrix.T

    return (matrix, ids)

        
def loadExpression(file):
    """
data_expression_Zscores.txt is recommended
"""
    with open(file) as f:
        firstline = f.readline().split("\t")
        ncols = len(firstline)
        ids = numpy.array(firstline)[2:]

        matrix = numpy.loadtxt(file, skiprows=1, usecols=range(2, ncols-1))
        matrix = matrix.T

    return (matrix, ids)



