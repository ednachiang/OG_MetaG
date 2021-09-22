#import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
pathHtext = 'test_createKEGGclassification/kegg.classification.txt'
    # Path to KEGG classification htext
directoryOutput = 'test_createKEGGclassification/'
    # Path to output COG .ffn files

htext = open(pathHtext, mode = "r")

keggDict1 = { }
    # Empty dictionary for cat 1 + cat 2
keggDict2 = { }
    # Empty dictionary for cat 2 + pathway
keggDict3 = { }
    # Empty dictionary for pathway + KOID
keggDict4 = { }
    # Empty dictionary for KOID + gene description

for line1 in htext.readlines():
        # Read file line-by-line

    if "A091" in line1:
        cat1 = line1[7:]
        #print(cat1)
        
    if "B  091" in line1:
        splitLine = line1.split('  ')
        #print(splitLine)

        if len(splitLine) > 1:
            cat2 = splitLine[1]
            cat2name = cat2[6:]
            #print(cat2name)
            
            keggDict1[cat1] = cat2name
        
    if "C    0" in line1:
        splitLine = line1.split('    ')
        #print(splitLine)

        path = splitLine[1]
        pathTrim = path[6:]
        pathTrim2 = pathTrim.split('[')
        pathName = pathTrim2[0]
        #print(pathName)

        keggDict2[cat2name] = pathName

        
    if "D      " in line1:
        splitLine = line1.split('      ')
        keep = splitLine[1]
        koid = keep[:6]
        #print(koid)

        keggDict3[pathName] = koid

        gene = keep[7:]
        geneTrim = gene.split('[')
        geneName = geneTrim[0]
        #print(geneName)

        keggDict4[koid] = geneName

#df1 = pd.DataFrame.from_dict(keggDict1, orient = 'index', columns = ['Cat2'])
#print(df1)
#df2 = pd.DataFrame.from_dict(keggDict2, orient = 'index', columns = ['Pathway'])
#print(df2)
#df3 = pd.DataFrame.from_dict(keggDict3, orient = 'index', columns = ['KOID'])
#print(df3)
df4 = pd.DataFrame.from_dict(keggDict4, orient = 'index', columns = ['Description'])
#print(df4)
df4['Pathway'] = keggDict3
print(df4)
