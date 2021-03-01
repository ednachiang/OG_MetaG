import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryFaa = 'test_saveAnvioGeneID/faa/'
directoryOutput = 'test_saveAnvioGeneID/output/'

def findAnvioGeneID(faaPath):

    faaInput = open(faaPath, mode = 'r')
    counter = 0
    idDict = {}

    for line1 in faaInput.readlines():
        
        if '>' in line1:
            counter += 1
            
            if counter % 10000 == 0:
                print("Still running. On ORF" + str(counter))


            #df.at[counter, 'gene_callers_id'] = counter
            line1Split = line1.split('#')

            nodeName = line1Split[0]
            nodeName = nodeName.replace('>', '')

            idDict[nodeName] = counter
            #df.at[counter, 'contig'] = nodeName
    return(idDict)


### Run Code ###

for file in os.listdir(directoryFaa):
    # Iterate for all files in the directory

    faaPath = directoryFaa + file
    sample = str(file[:4])
    
    print(sample + ' start')
    print(faaPath)

    output = findAnvioGeneID(faaPath)
    # print(output)
    # print(type(output))

    outputPath = directoryOutput + sample + '.anvio.gene.id.txt'

    outputdf = pd.DataFrame.from_dict(output, orient = 'index')
    print(outputdf)


    outputdf.to_csv(outputPath, sep = '\t', index = True, header = ['gene_callers_id'])
    print(sample + ' end')
print('Completed!')