import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryFaa = 'test_format_for_eCAMI/'
    # Path to .ffn you want to convert to .faa
outputFaa = 'test_format_for_eCAMI/'
    # Path to output faa file

def ffn_to_faa(faa_input, faa_output):
    faaInput = open(faa_input, mode = 'r')

    # Open output faa file
    output = open(faa_output, mode = 'a')

    for line1 in faaInput.readlines():
        # Read input prodigal file line-by-line
        prodigal = open(faa_input, mode = 'r')
        flag = False

        for line2 in prodigal:
            if line1 == line2:
                flag = True
                output.write(line2 + '|')
                continue
            if '>' in line2 and flag == True:
                prodigal.close()
                break
            if flag == True:
                output.write(line2)
    return(output)


##### Run Code #####

for file in os.listdir(directoryFaa):
    # Iterate for all files in the directory

    faaPath = directoryFaa + file
    print(faaPath)

    sample = str(file[:4])

    outputPath = outputFaa + sample + '.formatted.faa'
    print(outputPath)
    
    ffn_to_faa(faaPath, outputPath)
        # Function will save the .faa file, so no need to set it to a variable

