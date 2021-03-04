import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryTaxInput = 'test_createAnvioTaxonomy/tax/'
directoryGeneIDinput = 'test_createAnvioTaxonomy/geneID/'
directoryOutput = 'test_createAnvioTaxonomy/output/'


def renameORFs(inputTax, inputID):
    input_tax = open(inputTax, mode = 'r')
    input_ID = open(inputID, mode = 'r')

    taxDict = {}
    geneDict = {}

    for line1 in input_ID.readlines()[1:]:
        line1Split = line1.split()
        geneDict[line1Split[0]] = line1Split[1]


    for line2 in input_tax.readlines()[1:]:
        line2Split = line2.split('\t')

        contigName = line2Split[0]
        contigName = contigName.replace('\n', '')
        callerID = geneDict[contigName]

        orfDict = {}
        orfDict['gene_callers_id'] = callerID
        orfDict['t_domain'] = line2Split[1].replace('\n', '')
        orfDict['t_phylum'] = line2Split[2].replace('\n', '')
        orfDict['t_class'] = line2Split[3].replace('\n', '')
        orfDict['t_order'] = line2Split[4].replace('\n', '')
        orfDict['t_family'] = line2Split[5].replace('\n', '')
        orfDict['t_genus'] = line2Split[6].replace('\n', '')
        orfDict['t_species'] = line2Split[7].replace('\n', '')

        taxDict[callerID] = orfDict

    return(taxDict)



### Run Code ###
for file in os.listdir(directoryTaxInput):
    # Iterate for all files in the directory

    taxPath = directoryTaxInput + file
    sample = str(file[:4])
    genePath = directoryGeneIDinput + str(sample + '.anvio.gene.id.txt')
    
    print(sample + ' start')
    print(taxPath)
    print(genePath)

    output = renameORFs(taxPath, genePath)
    
    outputPath = directoryOutput + sample + '.tax.txt'

    outputdf = pd.DataFrame.from_dict(output, orient = 'index')

    outputdf.to_csv(outputPath, sep = '\t', index = False)
    print(sample + ' end')
print('Completed!')