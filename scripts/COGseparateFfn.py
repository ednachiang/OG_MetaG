import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes


##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryCOG = 'test_COGseparateFfn/cog/'
    # Directory of COG protein-id_cog.txt
directoryFfn = 'test_COGseparateFfn/ffn/'
    # Directory of .ffn files from prodigal
directoryOutput = 'test_COGseparateFfn/output/'
    # Output directory


# Input = list of significant COGs
COGs = ["COG0004", "COG0243", "COG0246", "COG0395", "COG0437", "COG0457", "COG0561", "COG0760", "COG0774", "COG1026", "COG1061", "COG1070", "COG1105", "COG1131", "COG1132", "COG1136", "COG1175", "COG1240", "COG1452", "COG1463", "COG1472", "COG1511", "COG1609", "COG1629", "COG1653", "COG1874", "COG1925", "COG2182", "COG2190", "COG2207", "COG2730", "COG2825", "COG2885", "COG2972", "COG3044", "COG3246", "COG3345", "COG3507", "COG3637", "COG3757", "COG3664", "COG3693", "COG3866", "COG3940", "COG3973", "COG4284", "COG4485", "COG4709", "COG4753", "COG4775", "COG5578"]




##### Define function: Create separate .ffn file for each enzyme of interest (CAZyme_EC)
def parseCOGs(COG_path, ffn_path, output_path):

    # Save paths for all protein-id_cog.txt files
    COGfiles = []
    for file1 in os.listdir(COG_path):
        COGpath = COG_path + file1
        COGfiles.append(COGpath)

    # Save paths for all prodigal .ffn files
    ffnFiles = []
    for file2 in os.listdir(ffn_path):
        ffnPath = ffn_path + file2
        ffnFiles.append(ffnPath)

    for file3 in COGfiles:
        # Go through COG files one-by-one

        sample = str(file3[-23:-19])
            # Save sample ID
        print(sample)
        print(file3)
        COG_ORFs = { }
            # Create empty dictionary for parsed COG ORFs
        
        # Open input file
        COGinput = open(file3, mode = 'r')

        # Pull out ORFs classified to sig COG
        for line1 in COGinput.readlines():
            # Read file line-by line

            col = line1.split('\t')
                # Split row by tabs
            
            for COGid in COGs:
                    # Go entry-by-entry through COG list
                if COGid == col[1]:
                    COG_ORFs[col[0]] = col[1]
                        # Add ORF to dictionary of COG ORFs
    
        # Convert dictionary to dataframe
        df1 = pd.DataFrame.from_dict(COG_ORFs, orient = 'index', columns = ['COG'])

        for COGid2 in COGs:
            # Go entry-by-entry through list of significant COGs
            outputPath = output_path + sample + '.' + COGid2 + '.ffn'
                # Name output file
            outputFFN = open(outputPath, mode = 'a')
                # Open output file
            print(outputPath)
        
            # Create list of ORFs classified to COGid2
            sigCOGs = []

            for row in df1.index:
                # Go line-by-line through df1
                if COGid2 == df1.at[row, 'COG']:
                    sigCOGs.append(row)
                        # Create list of ORFs classified to a specific COG
        
        
            for ORF1 in sigCOGs:
                inputPath = ffn_path + sample + '.ffn'
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

parseCOGs(directoryCOG, directoryFfn, directoryOutput)