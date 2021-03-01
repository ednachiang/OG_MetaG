import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryFaa = 'test_createAnvioProdigal/faa/'
directoryOutput = 'test_createAnvioProdigal/output/'


def convert_list_to_string(org_list, seperator=' '):
    #""" Convert list to string, by joining all item in list with given separator.
    #    Returns the concatenated string """
    return seperator.join(org_list)


def findInfo(faaPath):

    faaInput = open(faaPath, mode = 'r')
    counter = 0
    df = pd.DataFrame(columns = ['gene_callers_id', 'contig', 'start', 'stop', 'direction', 'partial', 'call_type', 'source', 'version', 'aa_sequence'])
    print(df)

    for line1 in faaInput.readlines():
        
        if '>' in line1:
            counter += 1
            
            if counter % 10000 == 0:
                print("Still running. On ORF" + str(counter))

            df.at[counter, 'gene_callers_id'] = counter
            line1Split = line1.split('#')

            nodeName = line1Split[0]
            nodeCutoff = nodeName.find('.', 1, len(nodeName))
            nodeName = nodeName[1:(int(nodeCutoff)+7)]
            df.at[counter, 'contig'] = nodeName

            start = line1Split[1]
            startFix = int(start) -+ 1
                # Account for python indices so anvio start position is correct
            df.at[counter, 'start'] = startFix

            stop = line1Split[2]
            df.at[counter, 'stop'] = stop

            direction = line1Split[3]
            direction = direction.replace(' ','')
            if direction == '1':
                df.at[counter, 'direction'] = 'f'
            elif direction == '-1':
                df.at[counter, 'direction'] = 'r'

            info = line1Split[4]
            infoSplit = info.split(";")

            partial = infoSplit[1]
            partial = partial.replace('partial=', '')
            df.at[counter, 'partial'] = partial

            aaSeq = ""
            continue

        else:
            seq = line1.replace('\n', '')
            aaSeq += seq
            df.at[counter, 'aa_sequence'] = aaSeq
            continue
    
    df['call_type'] = '1'
    df['source'] = 'prodigal'
    df['version'] = '2.6.3'
    print(df)
    return(df)


### Run Code ###

for file in os.listdir(directoryFaa):
    # Iterate for all files in the directory

    faaPath = directoryFaa + file
    sample = str(file[:4])
    
    print(sample + ' start')
    print(faaPath)

    output = findInfo(faaPath)
    
    outputPath = directoryOutput + sample + '.anvio.format.txt'

    output.to_csv(outputPath, sep = '\t', index = False)
    print(sample + ' end')
print('Completed!')