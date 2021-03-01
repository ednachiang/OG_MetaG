import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryCOGinput = 'test_createAnvioFunction/cog/'
directoryGeneIDinput = 'test_createAnvioFunction/geneID/'
directoryOutput = 'test_createAnviofunction/output/'


def convert_list_to_string(org_list, seperator=' '):
    #""" Convert list to string, by joining all item in list with given separator.
    #    Returns the concatenated string """
    return seperator.join(org_list)


def makeFunctionTable(inputCOG, inputID):
    input_COG = open(inputCOG, mode = 'r')
    input_ID = open(inputID, mode = 'r')

    functionDict = {}
    geneDict = {}

    for line1 in input_ID.readlines()[1:]:
        line1Split = line1.split()
        geneDict[line1Split[0]] = line1Split[1]


    for line2 in input_COG.readlines()[1:]:
        line2Split = line2.split('\t')
        contigName = line2Split[0]
        callerID = geneDict[contigName]

        orfDict = {}
        orfDict['source'] = 'COG'
        orfDict['accession'] = line2Split[13]
        func = line2Split[-1].replace('\n', '')
        orfDict['function'] = func
        orfDict['e_value'] = line2Split[10]

        functionDict[callerID] = orfDict

    return(functionDict)



### Run Code ###
for file in os.listdir(directoryCOGinput):
    # Iterate for all files in the directory

    cogPath = directoryCOGinput + file
    sample = str(file[:4])
    genePath = directoryGeneIDinput + str(sample + '.anvio.gene.id.txt')
    
    print(sample + ' start')
    print(cogPath)
    print(genePath)

    output = makeFunctionTable(cogPath, genePath)
    
    outputPath = directoryOutput + sample + '.function.txt'

    outputdf = pd.DataFrame.from_dict(output, orient = 'index')

    outputdf.to_csv(outputPath, sep = '\t', index = True)
    print(sample + ' end')
print('Completed!')