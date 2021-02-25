import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryFaa = 'test_createAnvioProdigal/faa/'
directoryProdigalTxt = 'test_createAnvioProdigal/prodigal/'
directoryOutput = 'test_createAnvioProdigal/output/'




def convert_list_to_string(org_list, seperator=' '):
    #""" Convert list to string, by joining all item in list with given separator.
    #    Returns the concatenated string """
    return seperator.join(org_list)

def findContigName(line):
    lineSplit = line.split()
    info = lineSplit[1]
    infoSplit = info.split(';')
    name = infoSplit[2]
    name = name.replace('seqhdr="', '')
    name = name.replace('"', '')
    return(name)



def findStartStop(line):
    lineSplit = line.split('CDS')
    lineSplit.pop(0)
    lineChar = convert_list_to_string(lineSplit)
    lineClean = lineChar.split()
    lineClean = convert_list_to_string(lineClean)
    lineClean = lineClean.replace('complement(', '')
    lineClean = lineClean.replace(')', '')
    lineClean = lineClean.replace('<','')

    startStop = lineClean.split('..')
    start = startStop[0]
    stop = startStop[1]
   
    return start, stop
    
 
def findInfo(line):
    lineSplit = line.split(";")
    ID = lineSplit[0]
    ID = ID.replace('/note="ID=', '')
    ID = ID.replace(' ', '')
    
    lineChar = convert_list_to_string(lineSplit)
    lineCharSplit = lineChar.split()

    partial = lineCharSplit[1]
    partialUse = partial.replace('partial=', '')
    return ID, partialUse



def findInfoFinal(prodigalPath, faaPath):

    prodigalInput = open(prodigalPath, mode = 'r')
    #faaInput = open(faaPath, mode = 'r')
    counter = 0
    df1 = pd.DataFrame()
    df = pd.DataFrame(columns = ['gene_callers_id', 'contig', 'start', 'stop', 'direction', 'partial', 'call_type', 'source', 'version', 'aa_sequence'])

    for line1 in prodigalInput.readlines():
        
        if '//' in line1:
            continue

        if 'DEFINITION' in line1:
            contigName = findContigName(line1)
            continue

        if 'FEATURES' in line1:
            continue

        if 'CDS' in line1:
            start, stop = findStartStop(line1)
            counter += 1
            df.at[counter,'start'] = start
            df.at[counter,'stop'] = stop
            df.at[counter,'contig'] = contigName
            #print(df)
            #continue
        if '/' in line1:
            ID, partial = findInfo(line1)
            df.at[counter, 'gene_callers_id'] = ID
            df.at[counter, 'partial'] = partial
            #print(df)
            #continue

    print('First part done')
    faaInput = open(faaPath, mode = 'r')

    for line2 in faaInput.readlines():
        #print(line2)
        if '>' in line2:
            line2Split = line2.split('#')
            direction = line2Split[3]

            info = line2Split[4]
            infoSplit = info.split(";")
            ID2 = infoSplit[0].replace('ID=', '')
            ID2 = ID2.replace(' ', '')

            flag = True
            aaSeq = ""

        else:
            for line3 in df.iterrows():
                row = line3[0]
                dfID = df.at[row, 'gene_callers_id']

                if dfID == ID2:
                    df.at[row, 'direction'] = direction

                    if flag == True:
                        seq = line2.replace('\n', '')
                        aaSeq += seq
                    
                        if '*' in line2:
                            df.at[row, 'aa_sequence'] = aaSeq
                            flag = False
                            continue
    
    df['call_type'] = '1'
    df['source'] = 'prodigal'
    df['version'] = '2.6.3'
    print(df)
    return(df)




### Run Code

for file in os.listdir(directoryProdigalTxt):
    # Iterate for all files in the directory

    prodigalPath = directoryProdigalTxt + file
    sample = str(file[:4])
    faaPath = directoryFaa + sample + '.faa'
    
    print(sample + ' start')
    print(prodigalPath)
    print(faaPath)

    output = findInfoFinal(prodigalPath, faaPath)
    
    outputPath = directoryOutput + sample + '.anvio.format.txt'
    output.to_csv(outputPath, sep = '\t', index = False)
    print(sample + ' end')
print('Completed!')