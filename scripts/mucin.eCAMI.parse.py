import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryeCAMI = 'test_mucin.eCAMI.parse/eCAMI/'
directoryProdigal = 'test_mucin.eCAMI.parse/prodigal/'
outputFaa = 'test_mucin.eCAMI.parse/eCAMI/'
    # Path to output faa file (for dbCAN input)
outputCount = 'test_mucin.eCAMI.parse/count.csv'
    # Path to output count file of ECs w/o CAZymes

# Input = list of EC numbers with associated CAZymes. Use this list to pull create .faa input for dbCAN
CAZymes = ["2.4.1.211:", "2.4.1.281:", "2.4.1.319:", "2.4.1.320:", "3.2.1.18:", "3.2.1.20:", "3.2.1.22:", "3.2.1.23:", "3.2.1.24:", "3.2.1.25:", "3.2.1.49:", "3.2.1.50:", "3.2.1.51:", "3.2.1.52:", "3.2.1.53:", "3.2.1.63:", "3.2.1.96:", "3.2.1.97:", "3.2.1.101:", "3.2.1.102:", "3.2.1.103:", "3.2.1.111:", "3.2.1.114:", "3.2.1.139:", "3.2.1.169:", "4.2.2.15:"]

# Create dictionary for EC's w/o associated CAZymes
outputEC = { }



##### Define function: Count ECs w/o an associated CAZyme
def countEC(inputFilePath, outputFilePath):
    # Input and Output = dictionary of EC numbers without an associated CAZyme.
    noCAZymes = {
        "3.1.1.2:": 0,
        "3.1.6.3:": 0,
        "3.1.6.4:": 0,
        "3.1.6.8:": 0,
        "3.1.6.14:": 0,
        "4.1.3.3:": 0
        }
    # Open input file
    input = open(inputFilePath, mode = 'r')
    # Open output file
    output = open(outputFilePath, mode = 'w')

    for line in input.readlines():
        # Read file line-by-line
        for entry in noCAZymes:
            # Go entry-by-entry through EC list
            if entry in line:
                noCAZymes[entry] += 1
    return(noCAZymes)



##### Define function: Create .faa of ECs of interest
def parseEC(eCAMIFilePath, prodigalFilePath, outputFilePath):
    # Open input eCAMI file
    eCAMI = open(eCAMIFilePath, mode = 'r')
    # Open input prodigal file
    prodigal = open(prodigalFilePath, mode = 'r')
    # Open output file
    output = open(outputFilePath, mode = 'a')
    # Create list for contigs that match an EC of interest
    contig = []

    for line1 in eCAMI.readlines():
        # Read eCAMI file line-by-line
        if '>' in line1:
            # For lines with contig name
            for entry in CAZymes:
                if entry in line1:
                    string = line1.split('\t')
                    name = string[0]

                    if name in contig:
                        # Ignore ORF if it already matched to an EC number so you don't get duplicate ORFs
                        break
                    else:
                        contig.append(name)

    for contigName in contig:
        prodigal = open(prodigalFilePath, mode = 'r')
        flag = False
        
        for line2 in prodigal:
            if contigName in line2:
                flag = True
                output.write(line2)
                continue
            if '>' in line2 and flag == True:
                prodigal.close()
                break
            if flag == True:
                output.write(line2)
    return(output)



##### Create EC count output
for file1 in os.listdir(directoryeCAMI):
# Iterate for all files in the directory
    
    filePath = directoryeCAMI + file1
    sample = str(file1[:4])
        # Pulls out sample ID #
    outputEC[sample] = countEC(filePath, outputCount)

ECdf = pd.DataFrame.from_dict(outputEC)
ECdf.to_csv(outputCount)



##### Create .faa of ECs of interest for dbCAN
for file2 in os.listdir(directoryeCAMI):
    # Iterate for all files in the directory
    
    eCAMIpath = directoryeCAMI + file2
    sample = str(file2[:4]+'.faa')
        # Pulls out sample ID #
    print(str(file2[:4]))
    prodigalPath = directoryProdigal + sample
    outputPath = outputFaa + sample
    parseEC(eCAMIpath, prodigalPath, outputPath)
        # Function will save the .faa file, so no need to set it to a variable