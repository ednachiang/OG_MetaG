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


##### Define function: Pull out dbCAN-classified ORFs to create ffn of dbCAN genes
def parse_dbCAN_ORFs(dbCAN_parsed_txt_path, prodigal_path, output_path):

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
            # Pull out only lines with dbCAN classification
            ORFtrim = col[4]
            ORFtrim = ORFtrim[:-1]
                # Remove new line character at end of ORF name
            ORFs.append(ORFtrim)
    

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
    print(sample)
    dbCANpath = directorydbCAN + str(file[:4]+'.parsed.txt')
    prodigalPath = directoryProdigal + sample + '.ffn'
    outputPath = directoryOutput + sample + '.ffn'
    parse_dbCAN_ORFs(dbCANpath, prodigalPath, outputPath)
        # Function will save the .ffn file, so no need to set it to a variable