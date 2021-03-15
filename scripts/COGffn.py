import os
	# Import os to iterate over files in a directory
import pandas as pd
    # Import pandas to use dataframes

##### CHANGE THESE PARAMETERS ACCORDINGLY
directoryCOG = 'test_COGffn/cog/'
    # Directory of protein-id_cog.txt
directoryProdigal = 'test_COGffn/prodigal/'
    # Directory of prodigal .ffn output files
directoryOutput = 'test_COGffn/'
    # Path to output COG .ffn files

# Input = list of COGs that appear in only 1 sample. These are removed in my R analysis.
drop = ["COG1791", "COG1855", "COG3477", "COG4097", "COG4135", "COG4242", "COG4542", "COG5022", "COG5138", "COG5174", "COG5183", "COG5214", "COG5259", "COG1941", "COG3350", "COG3582", "COG3692", "COG3868", "COG3895", "COG5169", "COG5444", "COG5473", "COG5547", "COG5595", "COG0843", "COG1458", "COG3211", "COG3800", "COG3840", "COG4825", "COG0271", "COG1634", "COG2822", "COG3121", "COG3900", "COG4167", "COG4340", "COG4742", "COG5019", "COG5351", "COG5555", "COG1059", "COG1339", "COG1422", "COG1513", "COG1553", "COG1710", "COG1777", "COG2224", "COG2411", "COG2445", "COG2886", "COG3154", "COG3435", "COG3588", "COG3624", "COG3631", "COG3766", "COG3791", "COG4300", "COG4574", "COG4798", "COG4993", "COG5470", "COG3465", "COG4307", "COG4521", "COG4778", "COG0278", "COG0672", "COG1382", "COG1495", "COG1981", "COG2248", "COG2260", "COG2443", "COG2811", "COG2847", "COG2879", "COG2993", "COG2999", "COG3146", "COG3403", "COG4529", "COG5003", "COG5074", "COG0387", "COG1369", "COG1571", "COG1584", "COG1588", "COG1631", "COG1644", "COG1965", "COG2018", "COG2023", "COG2118", "COG2403", "COG2516", "COG3105", "COG3371", "COG3462", "COG3510", "COG3890", "COG3932", "COG4317", "COG4357", "COG4707", "COG4792", "COG4888", "COG4941", "COG5052", "COG5062", "COG5081", "COG5085", "COG5086", "COG5094", "COG5100", "COG5102", "COG5111", "COG5113", "COG5120", "COG5131", "COG5157", "COG5197", "COG5238", "COG5290", "COG5391", "COG5415", "COG5448", "COG5541", "COG5576", "COG5600", "COG5601", "COG5604", "COG5627", "COG0856", "COG1356", "COG1423", "COG1552", "COG1973", "COG1996", "COG2167", "COG2802", "COG3251", "COG3357", "COG3398", "COG3443", "COG3888", "COG4136", "COG4689", "COG4867"]

##### Define function: Pull out dbCAN-classified ORFs to create ffn of dbCAN genes
def parse_COG_ORFs(COG_parsed_txt_path, prodigal_path, output_path):

    ##### Identify unwanted ORFs #####
    # Open input COG file
    COGinput = open(COG_parsed_txt_path, mode = 'r')

    # Create empty list for ORFs to remove
    remove = []

    for line1 in COGinput.readlines():
        # Read file line-by-line
        col = line1.split('\t')
            # Split row by tabs
        for COGid in drop:
            if COGid == col[1]:
                remove.append(col[0])


    ##### Pull out ORF names #####
    # Open input COG file
    COGinput = open(COG_parsed_txt_path, mode = 'r')

    # Create empty list for ORFs
    ORFs = []

    # Pull out ORFs classified to COG
    for line1 in COGinput.readlines():
        # Read file line-by-line
        col = line1.split('\t')
            # Split row by tabs      
        ORFs.append(col[0])
    

    ##### Remove unwanted ORFs #####
    for ORF0 in ORFs:
        for ORF_remove in remove:
            if ORF0 == ORF_remove:
                ORFs.remove(ORF0)


    ##### Create ffn file #####
    # Open output .ffn file
    output = open(output_path, mode = 'a')

    for ORF1 in ORFs:
        # Go ORF-by-ORF through ORF list
        prodigalInput = open(prodigal_path, mode = 'r')
        flag = False
        
        for line2 in prodigalInput.readlines():
            # Iterate line-by-line through prodigal file
            if ORF1 in line2:
                flag = True
                output.write(line2)
                continue
            if '>' in line2 and flag == True:
                prodigalInput.close()
                break
            if flag == True:
                output.write(line2)
    return(output)


##### Run Code #####
# Create .ffn of COGs
for file in os.listdir(directoryCOG):
    # Iterate for all files in directory
    sample = str(file[:4])
    COGpath = directoryCOG + str(file[:4]+'.protein-id_cog.txt')
    print(COGpath)
    prodigalPath = directoryProdigal + sample + '.ffn'
    print(prodigalPath)
    outputPath = directoryOutput + sample + '.ffn'
    print(outputPath)
    parse_COG_ORFs(COGpath, prodigalPath, outputPath)
        # Function will save the .ffn file, so no need to set it to a variable