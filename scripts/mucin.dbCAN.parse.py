import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directory = '../dbcan/mucin/'
miscECdir = '../dbcan/miscEC_counts.csv'
    # Count file for non-CAZyme EC #'s that participate in mucin degradation
otuPath = '../dbcan/mucin/mucin_OTU_table.csv'
    # Path to output "OTU table"
taxPath = '../dbcan/mucin/mucin_tax_table.csv'
    # Path to output "taxonomy table"

# Input = list mucin-degrading CAZymes
CAZymes = ["GH2", "GH3", "GH4", "GH16", "GH18", "GH20", "GH27", "GH29", "GH31", "GH33", "GH35", "GH36", "GH38", "GH42", "GH67", "GH76", "GH84", "GH85", "GH89", "GH92", "GH95", "GH97", "GH98", "GH101", "GH109", "GH110", "GH112", "GH123", "GH125", "GH129", "GH130", "GH163"]

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

            if split2 in CAZymes:
            # For mucin-degrading CAZymes
                if split2 in dbcanDict:
                    dbcanDict[split2] += 1
                        # Add one to the family counter
                else:
                # For CAZyme family that's not in the dictionary  yet
                    dbcanDict[split2] = 1
                        # Add family to dictionary and start counter
    return(dbcanDict)



# Create dictionary
for file in os.listdir(directory):
# Iterate for all files in the directory
    filePath = directory + file
    print(filePath)
    sample = str(file[:4])
        # Pulls out sample ID #
    dbcanDictFinal[sample] = dbcanParse(filePath)


# Create dbcan "OTU table"
dbcanOTU = pd.DataFrame.from_dict(dbcanDictFinal)

# Add non-CAZyme enzymes
miscEC = pd.read_csv(miscECdir, index_col=0)
finalEnzymes = dbcanOTU.append(miscEC)

# Format "OTU table"
finalEnzymes = finalEnzymes.fillna(0)
    # Fill NA's with 0 (otherwise they get saved as blanks)
for row in finalEnzymes.index:
    if 'AA' in row:
        finalEnzymes = finalEnzymes.drop(index=row)
            # Remove AA because they aren't relevant for me-- they're mostly lignose-degrading enzymes
    if 'CBM' in row:
        finalEnzymes = finalEnzymes.drop(index=row)
            # Remove CBM because they aren't enzymes

# Create dbcan "taxonomy table"
enzymeNames = finalEnzymes.index.values
enzymeTax = pd.DataFrame(enzymeNames, index = enzymeNames, columns = ['Family'])
enzymeTax['Class'] = enzymeTax['Family'].str[:2]
cols = enzymeTax.columns.tolist()
    # Convert column names to list because I want to reorder the columns so Class is first and Family is second
cols = cols[-1:] + cols[:-1]
    # Moves last col (Class) to the first position and moves first col (Family) to the second position
enzymeTax = enzymeTax[cols]
    # Reorder dataframe according to the new col positions



# Save dbcan OTU table and taxonomy table as .csv files
finalEnzymes.to_csv(otuPath)
enzymeTax.to_csv(taxPath)