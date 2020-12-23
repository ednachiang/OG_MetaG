import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes
import numpy as np
    # Import numpy to pull out unique values
import csv

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryeCAMI = '../eCAMI/sig_cazymes/cazymes/'
    # Path to eCAMI outputs
directoryOutput = '../eCAMI/sig_cazymes/output/'
    # Path to output folder
pathClass = '../dbcan/sig_cazyme_possible_ECs.csv'
    # Path to doc of ECs to identify for each CAZymes

##### Define function: Pull out ECs from eCAMI output
def pullEC(eCAMIFilePath, use):
    eCAMI = open(eCAMIFilePath, mode = 'r')
    keep = []

    for line1 in eCAMI.readlines():
        # Read eCAMI file line-by-line
        if '>' in line1:
            # For lines w/ contig name & eCAMI classification
                string = line1.split('\t')
                ec = string[-1]
                
                for entry in use:
                    if entry in ec:
                        keep.append(ec)
                        break

    classUnique = np.unique(keep)
    return(classUnique)


### Load CAZyme-EC matches
matches = pd.read_csv(pathClass)
colnames = matches.columns
colnames = colnames.tolist()

##### Create EC count output
for file1 in os.listdir(directoryeCAMI):
    # Iterate through all folders in eCAMI output directory
    cazymePath = directoryeCAMI + file1
    cazyme = file1
    matchesDict = { }

    for name in colnames:
        if cazyme == name:
            use = matches[name]
            use = use.dropna()
            use = use.tolist()
            break

    for file2 in os.listdir(cazymePath):
        # Iterate through all eCAMI outputs for a specific CAZyme
        sample = str(file2[:4])
            # Pull out sample ID
        inputPath = cazymePath + '/' + file2
        matchList = pullEC(inputPath, use)
        matchesDict[sample] = matchList
        
    outputPath = directoryOutput + cazyme + '.EC.match.csv'

    # Save dictionary as csv
    with open(outputPath, 'w') as f:
        for key in matchesDict.keys():
            f.write("%s,%s\n"%(key,matchesDict[key]))