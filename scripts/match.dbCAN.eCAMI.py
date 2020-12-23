import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes
import numpy as np
    # Import numpy to pull out unique values

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryeCAMI = 'test_match.dbCAN.eCAMI/eCAMI/'
    # Path to eCAMI outputs
directoryOutput = 'test_match.dbCAN.eCAMI/output/'
    # Path to output folder
pathClass = 'test_match.dbCAN.eCAMI/input/matches.csv'
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
    matchesDF = pd.DataFrame()

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
        matchesDF[sample] = matchList
    
    matchesDF = matchesDF.replace(r'\n', ' ', regex=True)
        # Remove new line characters
    outputPath = directoryOutput + cazyme + '.EC.match.csv'
    matchesDF.to_csv(outputPath, index=False)