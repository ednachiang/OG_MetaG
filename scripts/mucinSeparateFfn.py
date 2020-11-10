import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes


##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryeCAMI = 'test_mucinSeparateFfn/eCAMI/'
    # Directory of eCAMI output files
directorydbCAN = 'test_mucinSeparateFfn/dbCAN/'
    # Directory of dbCAN.parsed.txt (eCAMI --> dbCAN --> parsed text)
directoryFfn = 'test_mucinSeparateFfn/ffn/'
    # Directory of mucinParseFfn output .ffn files
directoryOutput = 'test_mucinSeparateFfn/'
    # Path to output mucin .ffn files


# Input = list of EC numbers with associated CAZymes. Use this list to pull create .faa input for dbCAN
EC = ["2.4.1.211:", "2.4.1.281:", "2.4.1.319:", "2.4.1.320:", "3.2.1.18:", "3.2.1.20:", "3.2.1.22:", "3.2.1.23:", "3.2.1.24:", "3.2.1.25:", "3.2.1.49:", "3.2.1.50:", "3.2.1.51:", "3.2.1.52:", "3.2.1.53:", "3.2.1.63:", "3.2.1.96:", "3.2.1.97:", "3.2.1.101:", "3.2.1.102:", "3.2.1.103:", "3.2.1.111:", "3.2.1.114:", "3.2.1.139:", "3.2.1.169:", "4.2.2.15:"]

# Input = list mucin-degrading CAZymes
CAZymes = ["GH2", "GH3", "GH4", "GH16", "GH18", "GH20", "GH27", "GH29", "GH31", "GH33", "GH35", "GH36", "GH38", "GH42", "GH67", "GH76", "GH84", "GH85", "GH89", "GH92", "GH95", "GH97", "GH98", "GH101", "GH109", "GH110", "GH112", "GH123", "GH125", "GH129", "GH130", "GH163"]

# Input = list of EC numbers that don't have associated CAZymes
onlyEC = ["3.1.1.2:", "3.1.6.3:", "3.1.6.4:", "3.1.6.8:", "3.1.6.14:", "4.1.3.3:"]


##### Define function: create enzyme count table
def parseEnzymes(eCAMI_path, dbCAN_path, ffn_path, output_path):

    # Save paths for all eCAMI files
    eCAMIfiles = []
    for file1 in os.listdir(eCAMI_path):
        eCAMIpath = eCAMI_path + file1
        eCAMIfiles.append(eCAMIpath)

    # Save paths for all dbCAN files
    dbCANfiles = []
    for file2 in os.listdir(dbCAN_path):
        dbCANpath = dbCAN_path + file2
        dbCANfiles.append(dbCANpath)

    # Create number list for 'for' loops to iterate through all eCAMI and dbCAN files
    fileNumber = range(0,len(eCAMIfiles))

    for file3 in fileNumber:
        # Go through eCAMI files one-by-one

        ##### eCAMI #####
        # Create empty dictionary for parsed EC ORFs
        eCAMI_ORFs = { }
        
        # Open input file
        eCAMIinput = open(eCAMIfiles[file3], mode = 'r')
        print(eCAMIfiles[file3])

        # Save sample ID (same for both eCAMI and dbCAN)
        sample = str(eCAMIfiles[file3][-8:-4])

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
                    eCAMI_ORFs[eCAMI_ORF_name] = entry1[:-1]
                        # Add ORF to dictionary of EC ORFs
        

        ##### dbCAN #####
        # Create empty dictionary for parsed dbCAN ORFs
        dbCAN_ORFs = { }

        # Open input file
        dbCANinput = open(dbCANfiles[file3], mode = 'r')
        print(dbCANfiles[file3])

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
                        dbCAN_ORFs[dbCAN_ORF[4]] = entry2
                            # Add ORF to dictionary of dbCAN ORFs


        ##### Create dataframe of matching ORFs, CAZymes, and ECs #####
        # Covert ORF names to list
        eCAMI_ORF_list = list(eCAMI_ORFs.keys())
        dbCAN_ORF_list = list(dbCAN_ORFs.keys())

        # Create empty dataframe
        df1 = pd.DataFrame(columns = ['ORF', 'CAZyme', 'EC', 'CAZyme_EC'])

        for ORF1 in dbCAN_ORF_list:
            # Iterate ORF-by-ORF through list of dbCAN ORFs

            for ORF2 in eCAMI_ORF_list:
                # Iterate ORF-by-ORF through list of eCAMI ORFs

                if ORF1 == ORF2:
                    # If dbCAN-classified ORF is also an eCAMI-classified ORF
                    combined = str(ORF1+'_'+ORF2)
                        # Create enzyme name: dbCAN_EC
                    df1 = df1.append({'ORF': ORF1, 'CAZyme': dbCAN_ORFs[ORF2], 'EC': eCAMI_ORFs[ORF2], 'CAZyme_EC': str(dbCAN_ORFs[ORF1]+'_'+eCAMI_ORFs[ORF2])}, ignore_index = True)
                        # Add ORF and enzyme name info to dataframe
        df1.index = df1['ORF']
            # Row names = ORF names

        ##### Pull out ORFs by dbCAN_EC #####
        enzymes = df1.CAZyme_EC.unique()
            # Pull out unique CAZyme_EC entries

        for enzyme1 in enzymes:
            # Go enzyme-by-enzyme through list of unique enzymes
            outputPath = output_path + sample + '.' + enzyme1 + '.ffn'
                # Name output files
            outputFFN = open(outputPath, mode = 'a')

            # Create list of ORFs classified to enzyme1
            ORFlist = []

            for row1 in df1.index:
                # Go line-by-line through df1
                if enzyme1 == df1.at[row1, 'CAZyme_EC']:
                    ORFlist.append(row1)
                        # Create list of ORFs classified to a specific enzyme
            
            for ORF3 in ORFlist:
                inputPath = ffn_path + sample + '.ffn'
                ffn_input = open(inputPath, mode = 'r')
                flag = False

                for line3 in ffn_input.readlines():
                    # Iterate line-by-line through input ffn file

                    if ORF3 in line3:
                        flag = True
                        outputFFN.write(line3)
                        continue
                    if '>' in line3 and flag == True:
                        ffn_input.close()
                        break
                    if flag == True:
                        outputFFN.write(line3)


        ##### ECs w/o associated CAZyme #####
        # Create empty directory of parsed EC ORFs
        df3 = pd.DataFrame(columns = ['ORF', 'EC'])

        # Open input file
        eCAMIinput = open(eCAMIfiles[file3], mode = 'r')

        # Pull out ORFs classified to ECs
        for line4 in eCAMIinput.readlines():
            # Read file line-by-line
            for entry3 in onlyEC:
                # Go entry-by-entry through EC list
                if entry3 in line4:
                    ORF4 = line4.split()
                    ORF4_name = ORF4[0]
                        # Pull out ORF name
                    ORF4_name = ORF4_name[1:]
                        # Remove '>' at start of ORF name
                    df3 = df3.append({'ORF':ORF4_name, 'EC':entry3[:-1]}, ignore_index = True)
                        # Add ORF to dictionary of EC-only ORFs
        df3.index = df3['ORF']
            # Row names = ORF names

        ##### Pull out EC-only ORFs #####
        for entry5 in onlyEC:
            # Go entry-by-entry through list of ECs w/o associated CAZyme
            outputPath = output_path + sample + '.' + entry5[:-1] + '.ffn'
                # Name output file
            outputFFN = open(outputPath, mode = 'a')
            entryRename = entry5[:-1]
                # Remove ':' at end of EC number

            # Create of ORFs classified to entry5
            EConly_ORF = []

            for row2 in df3.index:
                # Go line-by-line through df3

                if entryRename == df3.at[row2, 'EC']:
                    EConly_ORF.append(row2)

            for ORF5 in EConly_ORF:
                inputPath = ffn_path + sample + '.ffn'
                ffn_input = open(inputPath, mode = 'r')
                flag = False

                for line5 in ffn_input.readlines():
                    # Iterate line-by-line through input ffn file
                    if ORF5 in line5:
                        flag = True
                        outputFFN.write(line5)
                        continue
                    if '>' in line5 and flag == True:
                        ffn_input.close()
                    if flag == True:
                        outputFFN.write(line5)

        

##### Run code #####
parseEnzymes(directoryeCAMI, directorydbCAN, directoryFfn, directoryOutput)
        # Function will save .ffn files, so no need to set it to a variable
    