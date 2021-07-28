import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryKaiju = '../kaiju/mucin_sep/'
    # Directory of kaiju outputs
    # directoryKaiju/directorySpecificPredictedProtein/taxon
    # CHANGE FUNCTION makeDF ACCORDING TO DIRECTORY

proteins = os.listdir(directoryKaiju)
    # Save all predicted proteins
samples = ['3715', '3717', '3723', '3733', '3734', '3744', '3772', '3773', '3775']
sampDict = {0:"3715", 1:"3717", 2:"3723", 3:"3733", 4:"3734", 5:"3744", 6:"3772", 7:"3773", 8:"3775"}
taxon = ["phylum", "class", "order", "family", "genus", "species"]
    # Save all taxa levels
dict1 = {"3715":"Summer", "3717":"Summer", "3723":"Winter", "3733":"Winter", "3734":"Spring", "3744":"Summer", "3772":"Winter", "3773":"Spring", "3775":"Spring"}
    # Dictionary of sample-season
dict2 = {"Summer":"3715,3717,3744", "Winter":"3723,3733,3772", "Spring":"3734,3773,3775"}
    # Dictionary of season-taxa
dict3 = {}
    # Dictionary of taxa-rel abund




##### Define function: XXXXXXXXXXXXXXXX
def makeDF(taxaList, dataFrame, inputFile, taxaDict):
    
    input = open(inputFile, mode = "r")
    output = dataFrame
    #print(dataFrame)

    for line1 in input.readlines()[1:]:
        line1Split = line1.split('	')
        taxonName = line1Split[4]
        taxonName = taxonName[:-1]
        #print(taxonName)
        taxaDict[taxonName] = (line1Split[1])
        currentSamp = line1Split[0]

        ## FOR SEP SIG COGS ##
        #currentSamp = currentSamp[:-21]


        ## FOR SEP SIG CAZYMES   or   SEP MUCIN ##
        currentSamp = currentSamp[:-13]
        length = len(currentSamp)



        currentSamp = currentSamp[length-4 : length]
    
    #print(taxaDict)

    for taxon1 in taxaDict:
        output.loc[taxon1, currentSamp] = taxaDict[taxon1]
    
    return(output)







##### Define function: XXXXXXXXXXXXXXXX
def summarizeKaiju(input_Path, protein, output_Path, protein_path):

    for taxa in taxon:
        # Working taxon-by-taxon

        # Save output path
        outputPath = protein_path + protein + '.' + taxa + '.csv'

        # Empty list of taxa
        taxaList = []
        
        # Save paths for all kaiju files
        kaijuFiles = []
        for file1 in os.listdir(protein_path+taxa+'/'):
            #print(file1)
            kaijuPath = protein_path + taxa + '/' + file1
            kaijuFiles.append(kaijuPath)

        for file2 in kaijuFiles:
            kaijuInput = pd.read_table(file2)
            taxaCol = kaijuInput["taxon_name"].values.tolist()
                # Same taxon name column and convert that dataframe column into a list

            for taxa1 in taxaCol:
                if taxa1 in taxaList:
                    continue
                else:
                    taxaList.append(taxa1)
        
        #print(taxaList)
            
        df1 = pd.DataFrame(index = taxaList, columns = samples)        


        for file3 in kaijuFiles:
            taxaDict = {}
            df2 = makeDF(taxaList, df1, file3, taxaDict)
        
        df2 = df2.fillna(0)
        df2.to_csv(outputPath)






##### Run Code #####
for file in os.listdir(directoryKaiju):
    # Iterate for all files in directory
    protein = str(file)
    proteinPath = directoryKaiju + protein + '/'
    print(protein)
    summarizeKaiju(directoryKaiju, protein, directoryKaiju, proteinPath)
