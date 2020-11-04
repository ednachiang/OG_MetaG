import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryeCAMI = '../mucin/eCAMI/'
directorydbCAN = '../mucin/dbCAN/'
miscECpath = '../mucin/miscEC_counts.csv'
outputCount = '../mucin/mucinCount.csv'
outputTax = '../mucin/mucinClassification.csv'
    # Path to output count file of ECs w/o CAZymes

# Input = list of EC numbers with associated CAZymes. Use this list to pull create .faa input for dbCAN
EC = ["2.4.1.211:", "2.4.1.281:", "2.4.1.319:", "2.4.1.320:", "3.2.1.18:", "3.2.1.20:", "3.2.1.22:", "3.2.1.23:", "3.2.1.24:", "3.2.1.25:", "3.2.1.49:", "3.2.1.50:", "3.2.1.51:", "3.2.1.52:", "3.2.1.53:", "3.2.1.63:", "3.2.1.96:", "3.2.1.97:", "3.2.1.101:", "3.2.1.102:", "3.2.1.103:", "3.2.1.111:", "3.2.1.114:", "3.2.1.139:", "3.2.1.169:", "4.2.2.15:"]

# Input = list mucin-degrading CAZymes
CAZymes = ["GH2", "GH3", "GH4", "GH16", "GH18", "GH20", "GH27", "GH29", "GH31", "GH33", "GH35", "GH36", "GH38", "GH42", "GH67", "GH76", "GH84", "GH85", "GH89", "GH92", "GH95", "GH97", "GH98", "GH101", "GH109", "GH110", "GH112", "GH123", "GH125", "GH129", "GH130", "GH163"]


##### Define function: create enzyme count table
def makeCountTable(ECdirectory, dbCANdirectory):

    # Save paths for all eCAMI files
    eCAMIfiles = []
    for file1 in os.listdir(ECdirectory):
        eCAMIpath = ECdirectory + file1
        eCAMIfiles.append(eCAMIpath)
    
    # Save paths for all dbCAN files
    dbCANfiles = []
    for file2 in os.listdir(dbCANdirectory):
        dbCANpath = dbCANdirectory + file2
        dbCANfiles.append(dbCANpath)
    
    # Create empty dataframe for final count table
    finalCountTable = pd.DataFrame()

    # Create number list for 'for' loops to iterate through all eCAMI and dbCAN files
    fileNumber = range(0,len(eCAMIfiles))


    for file1 in fileNumber:
        # Go through eCAMI files one-by-one

        ##### eCAMI #####
        # Create empty dictionary for parsed EC ORFs
        eCAMI_ORFs = { }
        
        # Open input file
        eCAMIinput = open(eCAMIfiles[file1], mode = 'r')

        # Save sample ID (same for both eCAMI and dbCAN)
        sample = str(eCAMIfiles[file1][-8:-4])

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
                        # Remove '>' at start of OED name
                    eCAMI_ORFs[eCAMI_ORF_name] = entry1[:-1]
                        # Add ORF to dictionary of EC ORFs
        

        ##### dbCAN #####
        # Create empty dictionary for parsed dbCAN ORFs
        dbCAN_ORFs = { }

        # Open input file
        dbCANinput = open(dbCANfiles[file1], mode = 'r')

        # Pull out ORFs classified to mucin-degrading CAZymes
        for line2 in dbCANinput.readlines():
            # Read file line-by-line
               for entry2 in CAZymes:
                # Go entry-by-entry through CAZyme list
                if entry2 in line2:
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
        

        ##### Create count table for 1 sample #####
        # Create empty dictionary
        countDict = { }

        for ORF3, row in df1.iterrows():
            # Go row-by-row through ORF-CAZyme-EC-CAZyme_EC dataframe (created in previous for loop)

            if row['CAZyme_EC'] in countDict:
            # If CAZyme_EC is already in the dictionary
                countDict[row['CAZyme_EC']] += 1
                    # Increase count by 1
            else:
            # For CAZyme_EC that's not in the dictionary yet
                countDict[row['CAZyme_EC']] = 1
                    # Start counter

        # Convert count table dictionary to dataframe
        df2 = pd.DataFrame.from_dict(countDict, orient = 'index', columns = [sample])


        ##### Make final count table with all samples #####
        if finalCountTable.empty == True:
            # If final count table hasn't been populated yet; this is only used for the very first entry
            finalCountTable = df2
        else:
            finalCountTable = pd.concat([finalCountTable, df2], axis=1, sort=False)
                # Fills final count table after that first entry

    return(finalCountTable)


##### Run Code #####
output = makeCountTable(directoryeCAMI, directorydbCAN)

# Add non-CAZyme enzymes
miscEC = pd.read_csv(miscECpath, index_col=0)
miscEC = miscEC.rename(index = {'3.1.1.2:': '3.1.1.2',
        '3.1.6.3:': '3.1.6.3',
        '3.1.6.4:': '3.1.6.4',
        '3.1.6.8:': '3.1.6.8',
        '3.1.6.14:': '3.1.6.14',
        '4.1.3.3:': '4.1.3.3'})
finalCount = output.append(miscEC)

# Format count table
finalCount = finalCount.fillna(0)
    # Fill NA's with 0 (otherwise they get saved as blanks)

# Make "taxonomy" table
enzymeNames = finalCount.index.values
    # Pulls out all enzymeNames (CAZyme_EC)
enzymeNameList = enzymeNames.tolist()
    # Convert to list

# Create empty tax table dataframe
enzymeTax = pd.DataFrame(enzymeNames, index = enzymeNames, columns = ['Full'])

for name in enzymeNameList:
    # Go through enzymes one-by-one

    if 'G' in name:
        # For entries with CAZyme classification
        enzymeNamesSplit = name.split('_')
            # Split CAZyme and EC names
        CAZyme_name = str(enzymeNamesSplit[0])
        EC_name = enzymeNamesSplit[1]

        # Populate tax table
        enzymeTax.loc[name, 'GH_Class'] = CAZyme_name[:2]
        enzymeTax.loc[name, 'GH_Family'] = CAZyme_name
        enzymeTax.loc[name, 'EC1'] = EC_name[:1]
        enzymeTax.loc[name, 'EC2'] = EC_name[:4]
        enzymeTax.loc[name, 'EC3'] = EC_name[:6]
        enzymeTax.loc[name, 'EC4'] = EC_name
    
    else:
        # For entries w/o a CAZyme classification (miscEC entries)
        # Populate tax table
        enzymeTax.loc[name, 'GH_Class'] = "Unclassified"
        enzymeTax.loc[name, 'GH_Family'] = "Unclassified"
        enzymeTax.loc[name, 'EC1'] = name[:1]
        enzymeTax.loc[name, 'EC2'] = name[:4]
        enzymeTax.loc[name, 'EC3'] = name[:6]
        enzymeTax.loc[name, 'EC4'] = name

# Remove unnecessary column
enzymeTax = enzymeTax.drop(columns = 'Full')

# Save files!
finalCount.to_csv(outputCount)
enzymeTax.to_csv(outputTax)

        

