import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes



##### CHANGE THESE PARAMETERS ACCORDINGLY
directory = '../dbcan/spades/'
otuPath = '../dbcan/dbcan_mucinCBM_table.csv'
    # Path to output "OTU table"
#taxPath = '../dbcan/dbcan_tax_table.csv'
    # Path to output "taxonomy table"

CBM = ["CBM32", "CBM40", "CBM47", "CBM51", "CBM71"]

char1 = '.'
char2 = "_"
CBMdictFinal = { }

# Define function
def CBMparse(inputFilePath):
    CBMdict = { }
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

            if split2 in CBM:
            # For CBMs of interest
                if split2 in CBMdict:
                    CBMdict[split2] += 1
                        # Add one to the CBM counter
                else:
                # For CBM that's not in dictionary yet
                    CBMdict[split2] = 1
    return(CBMdict)



# Create dictionary
for file in os.listdir(directory):
# Iterate for all files in the directory
    filePath = directory + file
    sample = str(file[:4])
        # Pulls out sample ID #
    CBMdictFinal[sample] = CBMparse(filePath)



# Create dbcan "OTU table"
CBMotu = pd.DataFrame.from_dict(CBMdictFinal)

# Format "OTU table"
CBMotu = CBMotu.fillna(0)
    # Fill NA's with 0 (otherwise they get saved as blanks)

# Save CBM OTU table as .csv files
CBMotu.to_csv(otuPath)