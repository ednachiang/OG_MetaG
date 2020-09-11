import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes



##### CHANGE THESE PARAMETERS ACCORDINGLY
directory = '../dbcan/spades/'
otuPath = '../dbcan/dbcan_OTU_table.csv'
    # Path to output "OTU table"
taxPath = '../dbcan/dbcan_tax_table.csv'
    # Path to output "taxonomy table"



char1 = '.'
char2 = "_"
dbcanDictFinal = { }

# Define function
def dbcanParse(inputFilePath):
    dbcanDict = { }
        # Create dictionary to be populated in this command
    
    input = open(inputFilePath, mode='r')
        # Open input file

    for line1 in input.readlines():
    # Read file line-by-line

        col = line1.split('\t')
            # Split the row by tabs

        if 'hmm' in col[1]:
        # Pull out only lines that specify dbCAN classification in col 2. The last 7 lines summarize each class and don't contain hmm, so we want to exclude them.
            split1 = col[1].split(char1, 1)[0]
                # Pull out everything before the ".hmm"
            split2 = split1.split(char2, 1)[0]
                # Pull out everything before subfamily classification-- right now I only care about the family-level classification

            if split2 in dbcanDict:
            # For CAZyme family that's already in the dictionary
                dbcanDict[split2] = dbcanDict[split2] + 1
                    # Add one to the family counter
            else:
            # For CAZyme family that's not in the dictionary yet
                dbcanDict[split2] = 1
                    # Add familly to dictionary and start counter
    return(dbcanDict)



# Create dictionary
for file in os.listdir(directory):
# Iterate for all files in the directory
    filePath = directory + file
    sample = str(file[:4])
        # Pulls out sample ID #
    dbcanDictFinal[sample] = dbcanParse(filePath)



# Create dbcan "OTU table"
dbcanOTU = pd.DataFrame.from_dict(dbcanDictFinal)

# Format "OTU table"
dbcanOTU = dbcanOTU.fillna(0)
    # Fill NA's with 0 (otherwise they get saved as blanks)
dbcanOTU = dbcanOTU.drop(['cohesin', 'dockerin', 'SLH'])
    # Remove cohesin, dockerin, and SLH-- these are a domain modules added by dbCAN that's not in the CAZy database
for row in dbcanOTU.index:
    if 'AA' in row:
        dbcanOTU = dbcanOTU.drop(index=row)
            # Remove AA because they aren't relevant for me-- they're mostly lignose-degrading enzymes
    if 'CBM' in row:
        dbcanOTU = dbcanOTU.drop(index=row)
            # Remove CBM because they aren't enzymes


# Create dbcan "taxonomy table"
dbcanNames = dbcanOTU.index.values
dbcanTax = pd.DataFrame(dbcanNames, index = dbcanNames, columns = ['Family'])
dbcanTax['Class'] = dbcanTax['Family'].str[:2]
cols = dbcanTax.columns.tolist()
    # Convert column names to list because I want to reorder the columns so Class is first and Family is second
cols = cols[-1:] + cols[:-1]
    # Moves last col (Class) to the first position and moves first col (Family) to the second position
dbcanTax = dbcanTax[cols]
    # Reorder dataframe according to the new col positions



# Save dbcan OTU table and taxonomy table as .csv files
dbcanOTU.to_csv(otuPath)
dbcanTax.to_csv(taxPath)