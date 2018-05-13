fileNameTest = 'test.txt'
file = open(fileNameTest, mode='r')
counter = 0
t1C = 0
t2C = 0
countOfNodes = 0
data = {}
    # {} = dictionary
    # Saves an empty dictionary
currTierOneCategory = ""
currTierTwoCategory = ""
currTierThreeCategory = ""

def replaceStupidCharacters(line):
    # def defines a function
##    index = 0
####    for char in line:
####        line[index] = ""
####        index = index + 1
####        if(char != " "):
####            break;
##    line[0:10].replace(" ", "")
    line = line.lstrip()
        # lstrip = leading white strip
        # removes all white space characters at the beginning of the line
    line = line.replace('\t', "")
        # t = tab
    line = line.replace('\n', "")
        # n = new line character
        # you can remove the new line character because we've already read in the file. If you remove the new line character before you read in the file, you get a giant unhelpful glob
    return line
        # Output the fixed line
        

for line in file:
    if line[0:2] == "  " and line[3] != " ":
            # Finds lines where the first 2 characters are spaces, and the third character is NOT a space
        line = replaceStupidCharacters(line)
        currTierOneCategory = line
        #print(currTierOneCategory)
        data[currTierOneCategory] = dict()
    elif line[0:4] == "    " and line[5] != " ":
        line = replaceStupidCharacters(line)
        currTierTwoCategory = line
        data[currTierOneCategory][currTierTwoCategory] = dict()
    elif line[0:6] == "      " and line[7] != " ":
        line = replaceStupidCharacters(line)
        currTierThreeCategory = line
        data[currTierOneCategory][currTierTwoCategory][currTierThreeCategory] = list()
    elif line[0:8] == "        " and line[9] != " ":
        line = replaceStupidCharacters(line)
        data[currTierOneCategory][currTierTwoCategory][currTierThreeCategory].append(line)

def countContigsForLevelOneHeader(lvlOneHeader):
    count = 0; 
    for header2 in data[lvlOneHeader]:
        for header3 in data[lvlOneHeader][header2]:
            count = count + len(data[lvlOneHeader][header2][header3])
    return count;

def countContigsForLevelTwoHeader(lvlOneHeader, lvlTwoHeader):
    count = 0; 
    for entry in data[lvlOneHeader][lvlTwoHeader]:
        count = count + len(data[lvlOneHeader][lvlTwoHeader][entry])
    return count;

#print(countContigsForLevelOneHeader("Metabolism"))
#print(countContigsForLevelTwoHeader("Metabolism", "Carbohydrate metabolism"))
        #data[currTierOneCategory][currTierTwoCategory][currTierThreeCategory].append(line)

##    if counter > 50:
##        break
##    
##    counter = counter + 1
    



##      
   
##    else:
##        if "NODE_" in line: 
##            countOfNodes = countOfNodes + 1
##        counter = counter + 1

#print(data[currTierOneCategory][currTierTwoCategory][currTierThreeCategory][1])
#print(len(data["Metabolism"]["Carbohydrate metabolism"]["00010 Glycolysis / Gluconeogenesis [PATH:ko00010]"]))
    # len = length

##
##celproc = countContigsForLevelOneHeader("Cellular Processes")
##orgsys = countContigsForLevelOneHeader("Organismal Systems")
##humdis = countContigsForLevelOneHeader("Human Diseases")
##other = celproc + orgsys + humdis

f = open('test.output.csv', "w")

f.write("Metabolism" + "," + str(countContigsForLevelOneHeader("Metabolism")) + '\n');
f.write("Metabolism: Carbohydrate metabolism" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Carbohydrate metabolism"))+ '\n');
f.write("Metabolism: NRG metabolism" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Energy metabolism"))+ '\n');
##f.write("Metabolism: Lipid metabolism" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Lipid metabolism"))+ '\n');
##f.write("Metabolism: Nucleotide metabolism" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Nucleotide metabolism"))+ '\n');
##f.write("Metabolism: AA metabolism" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Amino acid metabolism"))+ '\n');
##f.write("Metabolism: Other AA metabolism" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Metabolism of other amino acids"))+ '\n');
##f.write("Metabolism: Glycan" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Glycan biosynthesis and metabolism"))+ '\n');
##f.write("Metabolism: Cofactors and vitamins" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Metabolism of cofactors and vitamins"))+ '\n');
##f.write("Metabolism: Terpenoids and polyketides" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Metabolism of terpenoids and polyketides"))+ '\n');
##f.write("Metabolism: 2dary metabolites" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Biosynthesis of other secondary metabolites"))+ '\n');
##f.write("Metabolism: Xenobiotics" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Xenobiotics biodegradation and metabolism"))+ '\n');
##f.write("Metabolism: Enzyme families" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Enzyme families"))+ '\n');
##f.write("Genetic Information Processing" + "," + str(countContigsForLevelOneHeader("Genetic Information Processing"))+ '\n');
#f.write("Genetic Information Processing: Transcription" + "," + str(countContigsForLevelTwoHeader("Genetic Information Processing", "Transcription"))+ '\n');
#f.write("Genetic Information Processing: Tranlation" + "," + str(countContigsForLevelTwoHeader("Genetic Information Processing", "Translation"))+ '\n');
#f.write("Genetic Information Processing: Fold sort degr" + "," + str(countContigsForLevelTwoHeader("Genetic Information Processing", "Folding, sorting and degradation"))+ '\n');
#f.write("Genetic Information Processing: Replication and repair" + "," + str(countContigsForLevelTwoHeader("Genetic Information Processing", "Replication and repair"))+ '\n');
#f.write("Genetic Information Processing: RNA family" + "," + str(countContigsForLevelTwoHeader("Genetic information processing", "RNA family")+ '\n'));
#f.write("Environ Info Process" + "," + str(countContigsForLevelOneHeader("Environmental Information Processing"))+ '\n');
#f.write("Environ Info Process: Membrane transport" + "," + str(countContigsForLevelTwoHeader("Environmental Information Processing", "Membrane transport"))+ '\n');
#f.write("Environ Info Process: Signal transduction" + "," + str(countContigsForLevelTwoHeader("Environmental Information Processing", "Signal transduction"))+ '\n');
#f.write("Environ Info Process: Signal molec and interact" + "," + str(countContigsForLevelTwoHeader("Environmental Information Processing", "Signaling molecules and interaction"))+ '\n');
#f.write("Other" + "," + str(other)+ '\n')
f.close()






##print("done")
##print("Metabolism")
##print(len(data["Metabolism"]))
##print("Metabolism: Carbohydrate metabolism")
##print(len(data["Metabolism"]["Carbohydrate metabolism"]))
##print("Metabolism: Energy metabolism")
##print(len(data["Metabolism"]["Energy metabolism"]))
##print("Metabolism: Lipid metabolism")
##print(len(data["Metabolism"]["Lipid metabolism"]))
##print("Metabolism: Nucleotide metabolism")
##print(len(data["Metabolism"]["Nucleotide metabolism"]))
##print("Metabolism: Amino acid metabolism")
##print(len(data["Metabolism"]["Amino acid metabolism"]))
##print("Metabolism: Other amino acids metabolism")
##print(len(data["Metabolism"]["Metabolism of other amino acids"]))
##print("Metabolism: Glycans")
##print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]))
##print("Metabolism: Cofactors and vitamins")
##print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]))
##print("Metabolism: Terpenoids and polyketides")
##print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]))
##print("Metabolism: 2dary metabolites")
##print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]))
##print("Metabolism: Xenobiotics")
##print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]))
##print("Metabolism: Enzyme families")
##print(len(data["Metabolism"]["Enzyme families"]))
##print("Genetic Information Processing")
##print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]))
