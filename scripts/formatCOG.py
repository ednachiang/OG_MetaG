import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryCOG = 'test_formatCOG/COG/'
    # Path to directory of cog_stats.txt
outputPath = 'test_formatCOG/COG.table.tab'
    # Output path

def formatCOG(directoryCOG_path):
    # Save paths for all cog_stats.txt files
    COGfiles = []
    for file1 in os.listdir(directoryCOG_path):
        COGpath = directoryCOG_path + file1
        COGfiles.append(COGpath)
    
    # Create empty dataframe for final table
    finalDF = pd.DataFrame()

    # Create number list for 'for' loops to iterate through all eCAMI and dbCAN files
    fileNumber = range(0,len(COGfiles))

    for file2 in fileNumber:
        # Go through COG files one-by-one

        # Create empty dictionary for COGs
        COG_ORFs = { }

        # Open input file
        COGinput = pd.read_csv(COGfiles[file2], sep = '\t', index_col = 0, names = ['Function', 'Count'])
        print(COGfiles[file2])

        # Save sample ID
        sample = str(COGfiles[file2][-18:-14])

        for COG1 in COGinput.index:
            COG_ORFs[COG1] = COGinput.at[COG1, 'Count']
                # Add COG + Count to dictionary

        COG_df = pd.DataFrame.from_dict(COG_ORFs, orient = 'index', columns = [sample])
            # Convert dictionary to dataframe
            # Keys = index (rows)

        ##### Make final COG table #####
        if finalDF.empty == True:
            # If final table hasn't been populated yet; this is only used for the very first entry
            finalDF = COG_df
        else:
            finalDF = pd.concat([finalDF, COG_df], axis = 1, sort = False)
    
    finalDF.reset_index(inplace = True)
    finalDF = finalDF.rename(columns = {'index': 'COG'})
    return(finalDF)

##### Run Code #####
output = formatCOG(directoryCOG)

# Format COG dataframe
output = output.fillna(0)
    # Fill NA's with 0 (otherwise they get saved as blanks)

# Save files!
output.to_csv(outputPath, sep = '\t', index = False)


