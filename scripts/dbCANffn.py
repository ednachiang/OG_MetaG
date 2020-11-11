import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directorydbCAN = 'test_dbCANffn/dbCAN/'
    # Directory of dbCAN.parsed.txt
directoryProdigal = 'test_dbCANffn/prodigal/'
    # Directory of prodigal .ffn output files
directoryOutput = 'test_dbCANffn/'
    # Path to output dbCAN .ffn files

# Input = list of CAZymes with counts < 3. These are removed in my R analysis.
drop = ["GH12", "GH17", "GH34", "GH52", "GH100", "GH107", "GH118", "GH149", "GH153", "GT29", "GT37", "GT42", "GT52", "GT58", "GT60", "GT67", "GT68", "GT77", "GT85", "GT93", "GT97", "CE5", "CE13", "PL2", "PL14", "PL16", "PL18", "PL28"]

##### Define function: Pull out dbCAN-classified ORFs to create ffn of dbCAN genes
def parse_dbCAN_ORFs(dbCAN_parsed_txt_path, prodigal_path, output_path):

    ##### Identify unwanted ORFs #####
    # Open input dbCAN file
    dbCANinput = open(dbCAN_parsed_txt_path, mode = 'r')

    # Create empty list for ORFs to remove
    remove = []

    for line1 in dbCANinput.readlines():
        # Read file line-by-line
        col = line1.split('\t')
            # Split row by tabs
        if 'hmm' in col[1]:
            family = col[1].split('.', 1)[0]
                # Pull out everything before the ".hmm"
            for CAZyme in drop:
                if family == CAZyme:
                    removeTrim = col[4]
                    removeTrim = removeTrim[:-1]
                        # Remove new line character at end of ORF name
                    remove.append(removeTrim)


    ##### Pull out ORF names #####
    # Open input dbCAN file
    dbCANinput = open(dbCAN_parsed_txt_path, mode = 'r')

    # Create empty list for ORFs
    ORFs = []

    # Pull out ORFs classified to CAZyme
    for line1 in dbCANinput.readlines():
        # Read file line-by-line
        col = line1.split('\t')
            # Split row by tabs
        if 'hmm' in col[1]:
            ORFtrim = col[4]
            ORFtrim = ORFtrim[:-1]
                # Remove new line character at end of ORF name
            ORFs.append(ORFtrim)
    

    ##### Remove unwanted ORFs #####
    for ORF0 in ORFs:
        for ORF_remove in remove:
            if ORF0 == ORF_remove:
                ORFs.remove(ORF0)


    ##### Create ffn file #####
    # Open output .ffn file
    output = open(output_path, mode = 'a')

    for ORF1 in ORFs:
        # Go ORF-by-ORF through ORF list
        prodigalInput = open(prodigal_path, mode = 'r')
        flag = False
        
        for line2 in prodigalInput.readlines():
            # Iterate line-by-line through prodigal file
            if ORF1 in line2:
                flag = True
                output.write(line2)
                continue
            if '>' in line2 and flag == True:
                prodigalInput.close()
                break
            if flag == True:
                output.write(line2)
    return(output)


##### Run Code #####
# Create .ffn of mucin-degrading enzyme genes
for file in os.listdir(directorydbCAN):
    # Iterate for all files in directory
    sample = str(file[:4])
    dbCANpath = directorydbCAN + str(file[:4]+'.parsed.txt')
    print(dbCANpath)
    prodigalPath = directoryProdigal + sample + '.ffn'
    print(prodigalPath)
    outputPath = directoryOutput + sample + '.ffn'
    print(outputPath)
    parse_dbCAN_ORFs(dbCANpath, prodigalPath, outputPath)
        # Function will save the .ffn file, so no need to set it to a variable