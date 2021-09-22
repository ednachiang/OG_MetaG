import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directorydbCAN = 'test_significantCAZymeFFN/dbCAN/'
    # Directory of dbCAN.parsed.txt
dbCANtax = 'test_significantCAZymeFFN/dbcan_tax_table.csv'
    # dbCAN "tax" table
directoryFFN = 'test_significantCAZymeFFN/ffn/'
    # Directory of dbCANffn.py .ffn output files
directoryOutput = 'test_significantCAZymeFFN/'
    # Path to output dbCAN .ffn files

# Input = list of significant CAZyme families
CAZymes = ["GT101", "PL1", "GH43", "GH115", "CE12", "GH10", "GH59", "GT41", "GH20", "GT4", "GT9", "CE11", "GT3", "GH84", "GH3", "GH32", "GH5", "GH78", "GH42", "GH106", "GH39"]

##### Define function: Pull out dbCAN-classified ORFs to create ffn of dbCAN genes
def parse_CAZyme_ORFs(dbCAN_parsed_txt_path, dbCAN_tax_table_path, dbCAN_ffn_path, output_path):

    # Save paths for all dbCAN.parsed.txt files
    dbCANfiles = []
    for file1 in os.listdir(dbCAN_parsed_txt_path):
        dbCANpath = dbCAN_parsed_txt_path + file1
        dbCANfiles.append(dbCANpath)
    
    # Create number list for 'for' loops to iterate through all dbCAN.parsed.txt and dbcanffn/ffn files files
    fileNumber = range(0,len(dbCANfiles))

    for file2 in fileNumber:
        # Save sample ID
        sample = str(dbCANfiles[file2][-15:-11])

        # Create empty dictionary for parsed dbCAN ORFs
        dbCAN_ORFs = { }

        # Open input file
        dbCANinput = open(dbCANfiles[file2])
        print(dbCANfiles[file2])

        # Pull out ORFs classified to sig CAZymes
        for line1 in dbCANinput.readlines():
            # Read file line-by-line

            col = line1.split('\t')
                # Split the row by tabs
            
            if 'hmm' in col[1]:
                # Pull out only lines that specify dbCAN classification in col 2.
                family = col[1].split('.', 1)[0]
                    # Pull out everything before the ".hmm"
                
                for entry1 in CAZymes:
                    # Go entry-by-entry through CAZyme list
                    if entry1 == family:
                        dbCAN_ORF = line1.split()
                        dbCAN_ORFs[dbCAN_ORF[4]] = entry1
                            # Add ORF to dictionary of dbCAN ORFs
        
        # Convert dictionary to dataframe
        df1 = pd.DataFrame.from_dict(dbCAN_ORFs, orient = 'index', columns = ['CAZyme'])

        for entry2 in CAZymes:
            # Go entry-by-entry through list of significant CAZymes
            outputPath = output_path + sample + '.' + entry2 + '.ffn'
                # Name output file
            outputFFN = open(outputPath, mode = 'a')
                # Open output file
            
            # Create list of ORFs classified to entry2
            sigORF = []

            for row in df1.index:
                # GO line-by-line through df1
                if entry2 == df1.at[row, 'CAZyme']:
                    sigORF.append(row)
                        # Create list of ORFs classified to a specific CAZyme
                
            for ORF1 in sigORF:
                inputPath = dbCAN_ffn_path + sample + '.ffn'
                ffn_input = open(inputPath, mode = 'r')
                flag = False

                for line2 in ffn_input.readlines():
                    # Iterate line-by-line through .ffn file
                    if ORF1 in line2:
                        flag = True
                        outputFFN.write(line2)
                        continue
                    if '>' in line2 and flag == True:
                        ffn_input.close()
                        break
                    if flag == True:
                        outputFFN.write(line2)
  

    
##### Run code #####
parse_CAZyme_ORFs(directorydbCAN, dbCANtax, directoryFFN, directoryOutput)
        # Function will save .ffn files, so no need to set it to a variable