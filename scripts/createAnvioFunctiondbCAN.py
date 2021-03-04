import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directorydbCANinput = 'test_createAnvioFunctiondbCAN/dbCAN/'
directoryGeneIDinput = 'test_createAnvioFunctiondbCAN/geneID/'
directoryOutput = 'test_createAnviofunctiondbCAN/output/'


def makeFunctionTable(inputdbCAN, inputID):
    input_dbCAN = open(inputdbCAN, mode = 'r')
    input_ID = open(inputID, mode = 'r')

    functionDict = {}
    geneDict = {}

    for line1 in input_ID.readlines()[1:]:
        line1Split = line1.split()
        geneDict[line1Split[0]] = line1Split[1]


    for line2 in input_dbCAN.readlines()[1:]:
        line2Split = line2.split('\t')

        if len(line2Split) == 2:
            continue

        else:
            contigName = line2Split[4]
            contigName = contigName.replace('\n', '')
            callerID = geneDict[contigName]

            cazyme = line2Split[1]
            cazyme = cazyme.replace('.hmm', '')

            orfDict = {}
            orfDict['gene_callers_id'] = callerID
            orfDict['source'] = 'dbCAN'
            orfDict['accession'] = cazyme
            orfDict['function'] = cazyme
            orfDict['e_value'] = line2Split[2]

        functionDict[callerID] = orfDict

    return(functionDict)



### Run Code ###
for file in os.listdir(directorydbCANinput):
    # Iterate for all files in the directory

    dbCANpath = directorydbCANinput + file
    sample = str(file[:4])
    genePath = directoryGeneIDinput + str(sample + '.anvio.gene.id.txt')
    
    print(sample + ' start')
    print(dbCANpath)
    print(genePath)

    output = makeFunctionTable(dbCANpath, genePath)
    
    outputPath = directoryOutput + sample + '.function.txt'

    outputdf = pd.DataFrame.from_dict(output, orient = 'index')

    outputdf.to_csv(outputPath, sep = '\t', index = False)
    print(sample + ' end')
print('Completed!')