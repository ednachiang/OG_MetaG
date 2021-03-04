import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryGeneID = 'test_renameKeggORFs/geneID/'
directoryKOTab = 'test_renameKeggORFs/ko.tab/'
directoryOutput = 'test_renameKeggORFs/output/'


def convert_list_to_string(org_list, seperator=' '):
    #""" Convert list to string, by joining all item in list with given separator.
    #    Returns the concatenated string """
    return seperator.join(org_list)


def renameKeggORFs(geneID_path, KOTab_path):

    input_geneID = open(geneID_path, mode = 'r')
    input_koTab = open(KOTab_path, mode = 'r')

    geneID_dict = {}
    koTab_dict = {}
    output_dict = {}

    for line1 in input_geneID.readlines()[1:]:
        line1Split = line1.split()
        geneID_dict[line1Split[0]] = line1Split[1]
    
    for line2 in input_koTab.readlines():
        line2Split = line2.split('\t')

        if len(line2Split) == 1:
            line2str = convert_list_to_string(line2Split)
            line2str = line2str.replace('\n', '')
            entry = geneID_dict[line2str]
            entry = entry.replace('\n', '')
            output_dict[entry] = ''
            continue
        if len(line2Split) == 2:
            contigName = line2Split[0]
            contigName = contigName.replace('\n', '')
            newID = geneID_dict[contigName]
            koid = line2Split[1].replace('\n', '')

        output_dict[newID] = koid

    return(output_dict)



### Run Code ###

for file in os.listdir(directoryGeneID):
    # Iterate for all files in the directory

    GeneIDpath = directoryGeneID + file
    sample = str(file[:4])
    KOtabPath = directoryKOTab + sample + '.ko.tab'
    
    print(sample + ' start')
    print(GeneIDpath)
    print(KOtabPath)

    output = renameKeggORFs(GeneIDpath, KOtabPath)

    outputPath = directoryOutput + sample + '.ko.geneID.txt'

    outputdf = pd.DataFrame.from_dict(output, orient = 'index')
    print(outputdf)


    outputdf.to_csv(outputPath, sep = '\t', index = True, header = False)
    print(sample + ' end')
print('Completed!')