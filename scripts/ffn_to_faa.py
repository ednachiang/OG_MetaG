import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryFfn = 'test_ffn_to_faa/ffn/'
    # Path to .ffn you want to convert to .faa
directoryProdigal = 'test_ffn_to_faa/prodigal/'
    # Path to prodigal output.faa file
outputFaa = 'test_ffn_to_faa/'
    # Path to output faa file

def ffn_to_faa(ffn_input, prodigal_input, faa_output):
    # Open input ffn file
    ffnInput = open(ffn_input, mode = 'r')

    # Open output faa file
    output = open(faa_output, mode = 'a')

    for line1 in ffnInput.readlines():
        # Read input prodigal file line-by-line
        prodigal = open(prodigal_input, mode = 'r')
        flag = False

        for line2 in prodigal:
            if line1 == line2:
                flag = True
                output.write(line2)
                continue
            if '>' in line2 and flag == True:
                prodigal.close()
                break
            if flag == True:
                output.write(line2)
    return(output)


##### Run Code #####

for file in os.listdir(directoryFfn):
    # Iterate for all files in the directory

    ffnPath = directoryFfn + file
    print(ffnPath)

    sample = str(file[:4])
    fileSplit = file.split('.')
    enzyme = fileSplit[1]

    prodigalPath = directoryProdigal + sample + '.faa'
    print(prodigalPath)

    outputPath = outputFaa + sample + '.' + enzyme + '.faa'
    print(outputPath)
    
    ffn_to_faa(ffnPath, prodigalPath, outputPath)
        # Function will save the .faa file, so no need to set it to a variable

