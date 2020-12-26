import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryKEGG = 'test_formatKEGG/KEGG/'
    # Path to directory of kegg ko tab files
outputPath = 'test_formatKEGG/KEGG.table.tab'
    # Output path

def formatKEGG(directoryKEGG):
    # Save paths for all kegg.ko.tab files
    KEGGfiles = []
    for file1 in os.listdir(directoryKEGG):
        KEGGpath = directoryKEGG + file1
        KEGGfiles.append(KEGGpath)
    
    # Create empty dataframe for final table
    finalDF = pd.DataFrame()

    # Create number list for 'for' loops to iterate through all KEGG files
    fileNumber = range(0,len(KEGGfiles))

    for file2 in fileNumber:
        # Go through KEGG files one-by-one

        # Create empty dictionary for KOIDs
        KEGG_KOIDs = { }

        # Open input file
        KEGGinput = pd.read_csv(KEGGfiles[file2], sep = '\t', names = ['ORF', 'KOID'])
        KEGGinput = KEGGinput.drop(columns = ['ORF'])
        KEGGinput = KEGGinput.dropna()
        print(KEGGfiles[file2])
        # Save sample ID
        sample = str(KEGGfiles[file2][-11:-7])

        for KOID1 in KEGGinput['KOID']:
            # Go through KOIDs one-by-one to create dictionary of KOID counts

            if KOID1 in KEGG_KOIDs.keys():
                # If KOID is already in dictionary
                KEGG_KOIDs[KOID1] += 1
            else:
                # If KOID isn't in the dictionary yet
                KEGG_KOIDs[KOID1] = 1
        
        KEGG_df = pd.DataFrame.from_dict(KEGG_KOIDs, orient = 'index', columns = [sample])
        # Convert dictionary to dataframe
        # Keys = index (rows)
        #KEGG_df[sample] = KEGG_df[sample].apply(int)
        KEGG_df[sample] = KEGG_df[sample].round()

        ##### Make final KOID table #####
        if finalDF.empty == True:
            # If final table hasn't been populated yet; this is only used for the very first entry
            finalDF = KEGG_df
        else:
            finalDF = pd.concat([finalDF, KEGG_df], axis = 1, sort = False)
        
    finalDF.reset_index(inplace = True)
    finalDF = finalDF.rename(columns = {'index' : 'KOID'})
    return(finalDF)

##### Run Code #####
output = formatKEGG(directoryKEGG)

# Format KEGG dataframe
output = output.fillna(0)
    # Fill NA's with 0 (otherwise they get saved as blanks)
output = output.sort_values(by = ['KOID'])
#output = output.set_option('precision', 0)

# Save files!
output.to_csv(outputPath, sep = '\t', index = False)



