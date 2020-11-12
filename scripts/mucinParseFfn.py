import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryeCAMI = 'test_mucinParseFfn/eCAMI/'
    # Directory of eCAMI output files
directorydbCAN = 'test_mucinParseFfn/dbCAN/'
    # Directory of dbCAN.parsed.txt (eCAMI --> dbCAN --> parsed text)
directoryProdigal = 'test_mucinParseFfn/prodigal/'
    # Directory of prodigal .ffn files
directoryOutput = 'test_mucinParseFfn/'
    # Path to output mucin .ffn files

# Input = list of EC numbers with associated CAZymes. Use this list to pull create .faa input for dbCAN
EC = ["2.4.1.211:", "2.4.1.281:", "2.4.1.319:", "2.4.1.320:", "3.2.1.18:", "3.2.1.20:", "3.2.1.22:", "3.2.1.23:", "3.2.1.24:", "3.2.1.25:", "3.2.1.49:", "3.2.1.50:", "3.2.1.51:", "3.2.1.52:", "3.2.1.53:", "3.2.1.63:", "3.2.1.96:", "3.2.1.97:", "3.2.1.101:", "3.2.1.102:", "3.2.1.103:", "3.2.1.111:", "3.2.1.114:", "3.2.1.139:", "3.2.1.169:", "4.2.2.15:"]

# Input = list mucin-degrading CAZymes
CAZymes = ["GH2", "GH3", "GH4", "GH16", "GH18", "GH20", "GH27", "GH29", "GH31", "GH33", "GH35", "GH36", "GH38", "GH42", "GH67", "GH76", "GH84", "GH85", "GH89", "GH92", "GH95", "GH97", "GH98", "GH101", "GH109", "GH110", "GH112", "GH123", "GH125", "GH129", "GH130", "GH163"]

# Input = list of EC numbers without associated CAZymes.
onlyEC = ["3.1.1.2:", "3.1.6.3:", "3.1.6.4:", "3.1.6.8:", "3.1.6.14:", "4.1.3.3:"]

# Input = list of enzymes with counts < 4. These are removed in my R analysis.
# "GH16_3.2.1.23", "GH16_3.2.1.103", "GH4_3.2.1.24", "3.1.1.2", "3.1.6.3", "3.1.6.4", "3.1.6.8", "3.1.6.14"
dropGH = ["GH16", "GH4"]
dropEC_withCAZyme = ["3.2.1.23:", "3.2.1.103:", "3.2.1.24:"]
dropEC_onlyEC = ["3.1.1.2:", "3.1.6.3:", "3.1.6.4:", "3.1.6.8:", "3.1.6.14:"]

##### Define function: create enzyme count table
def parseMucinORFs(eCAMI_path, dbCAN_path, prodigal_path, output_path):

    ##### eCAMI #####
    # Create empty list for parsed EC ORFs
    eCAMI_ORFs = []
        
    # Open input file
    eCAMIinput = open(eCAMI_path, mode = 'r')
    print(eCAMI_path)

    # Pull out ORFs classified to mucin-degrading ECs
    for line1 in eCAMIinput.readlines():
        # Read file line-by-line
        for entry1 in EC:
            # Go entry-by-entry through EC list
            if entry1 in line1:
                eCAMI_ORF = line1.split()
                eCAMI_ORF_name = eCAMI_ORF[0]
                    # Pull out ORF name
                eCAMI_ORF_name = eCAMI_ORF_name[1:]
                    # Remove '>' at start of ORF name
                
                if eCAMI_ORF_name in eCAMI_ORFs:
                    # Ignore ORF if it already matched to an EC number so you don't get duplicate ORFs
                    break
                else:
                    eCAMI_ORFs.append(eCAMI_ORF_name)

    ##### dbCAN #####
    # Create empty list for parsed dbCAN ORFs
    dbCAN_ORFs = []

    # Open input file
    dbCANinput = open(dbCAN_path, mode = 'r')
    print(dbCAN_path)

    # Pull out ORFs classified to mucin-degrading CAZymes
    for line2 in dbCANinput.readlines():
        # Read file line-by-line

        col = line2.split('\t')
            # Split the row by tabs
        
        if 'hmm' in col[1]:
        # Pull out only lines that specify dbCAN classification in col 2. The last 7 lines summarize each class and don't contain hmm, so we want to exclude them.
            family = col[1].split('.', 1)[0]
                # Pull out everything before the ".hmm"

            for entry2 in CAZymes:
                # Go entry-by-entry through CAZyme list
                if entry2 == family:
                    dbCAN_ORF = line2.split()
                    dbCAN_ORFs.append(dbCAN_ORF[4])
 

    ##### Create list of matching ORFs #####
    # Create empty list
    mucinContigs = []

    for ORF1 in dbCAN_ORFs:
        # Iterate ORF-by-ORF through list of dbCAN ORFs
        for ORF2 in eCAMI_ORFs:
            # Iterate ORF-by-ORF through list of eCAMI ORFs
            if ORF1 == ORF2:
                # If dbCAN-classified ORF is also an eCAMI-classified ORF
                mucinContigs.append(ORF1)


    ##### Add ECs w/o an associated CAZyme #####
    # Open input file
    eCAMIinput = open(eCAMI_path, mode = 'r')

    # Pull out ORFs classified to mucin-degrading ECs
    for line3 in eCAMIinput.readlines():
        # Read file line-by-line
        for entry3 in onlyEC:
                # Go entry-by-entry through EC list
            if entry3 in line3:
                EC_ORF = line3.split()
                EC_ORF_name = EC_ORF[0]
                    # Pull out ORF name
                EC_ORF_name = EC_ORF_name[1:]
                    # Remove '>' at start of ORF name
                mucinContigs.append(EC_ORF_name)
                    # Add ORF to list of mucin-degrading enzyme genes
    

    ##### Create list of ORFs to remove - enzymes with counts < 4. These are removed in my R analysis #####
    
    # Create list of EC ORFs to remove
    dropORF_EC_withCAZyme = []

    # Open input file - eCAMI
    eCAMIinput = open(eCAMI_path, mode = 'r')

    ### Parse through eCAMI
    for line4 in eCAMIinput.readlines():
        # Read file line-by-line
        for drop1 in dropEC_withCAZyme:
            # Go entry-by-entry through EC list
            if drop1 in line4:
                drop_ORF1 = line4.split()
                drop_ORF1_name = drop_ORF1[0]
                    # Pull out ORF name
                drop_ORF1_name = drop_ORF1_name[1:]
                    # Remove '>' at start of ORF name
                
                if drop_ORF1_name in dropORF_EC_withCAZyme:
                    # Ignore ORF if it already matched to an EC number so you don't get duplicate ORFs
                    break
                else:
                    dropORF_EC_withCAZyme.append(drop_ORF1_name)


    # Create list of CAZyme ORFs to remove
    dropORF_CAZyme = []

    # Open input file - dbCAN
    dbCANinput = open(dbCAN_path, mode = 'r')

    ### Parse through dbCAN 
    for line5 in dbCANinput.readlines():
        # Read file line-by-line
        col2 = line5.split('\t')

        if 'hmm' in col2[1]:
        # Pull out only lines that specify dbCAN classification in col 2. The last 7 lines summarize each class and don't contain hmm, so we want to exclude them.
            family = col2[1].split('.', 1)[0]
                # Pull out everything before the ".hmm"
            for drop2 in dropGH:
                if family == drop2:
                    drop_ORF2 = line5.split()
                    dropORF_CAZyme.append(drop_ORF2[4])


    # Create list of ORFs to remove (EC & CAZyme combined)
    dropORF = []

    ### Pull out shared ORFs between drop EC & CAZyme
    for drop3 in dropORF_EC_withCAZyme:
        for drop4 in dropORF_CAZyme:
            if drop3 == drop4:
                dropORF.append(drop3)

    
    ### Pull out ORFs for dropped ECs w/o associated CAZyme
    dropORF_EC_onlyEC = []

    # Open input file - eCAMI
    eCAMIinput = open(eCAMI_path, mode = 'r')

    # Parse through eCAMI
    for line6 in eCAMIinput.readlines():
        # Read file line-by-line
        for drop5 in dropEC_onlyEC:
            if drop5 in line6:
                drop_ORF3 = line6.split()
                drop_ORF3_name = drop_ORF3[0]
                    # Pull out ORF name
                drop_ORF3_name = drop_ORF3_name[1:]
                    # Remove '>' at start of ORF name
                
                if drop_ORF3_name in dropORF_EC_onlyEC:
                    # Ignore ORF if it already matched to an EC number so you don't get duplicate ORFs
                    break
                else:
                    dropORF_EC_onlyEC.append(drop_ORF3_name)


    ### Add only-EC ORFs to list of ORFs to drop
    for drop5 in dropORF_EC_onlyEC:
        dropORF.append(drop5)
    

    ### Remove unwanted ORFs
    for ORF3 in mucinContigs:
        for drop5 in dropORF:
            if ORF3 == drop5:
                mucinContigs.remove(ORF3)

    
    ##### Pull out contigs that match mucin ORF #####
    output = open(outputPath, mode = 'a')

    for contig in mucinContigs:
        prodigalInput = open(prodigal_path, mode = 'r')
        flag = False

        for line4 in prodigalInput.readlines():
            # Iterate line-by-line through prodigal file
            if contig in line4:
                flag = True
                output.write(line4)
                continue
            if '>' in line4 and flag == True:
                prodigalInput.close()
                break
            if flag == True:
                output.write(line4)
    return(output)


##### Run Code #####

##### Create .ffn of mucin-degrading enzyme genes
for file in os.listdir(directoryeCAMI):
    # Iterate for all files in directory

    eCAMIpath = directoryeCAMI + file
    sample = str(file[:4]+'.ffn')
    dbCANpath = directorydbCAN + str(file[:4]+'.parsed.txt')
    prodigalPath = directoryProdigal + sample
    outputPath = directoryOutput + sample
    parseMucinORFs(eCAMIpath, dbCANpath, prodigalPath, outputPath)
        # Function will save the .ffn file, so no need to set it to a variable
