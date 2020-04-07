fileName = '3715_brite.txt'
fileNameTest = 'random.txt'
file = open(fileNameTest, mode='r')
counter = 0
t1C = 0
t2C = 0
countOfNodes = 0
data = {}
currTierOneCategory = ""
currTierTwoCategory = ""
currTierThreeCategory = ""

def replaceStupidCharacters(line):
##    index = 0
####    for char in line:
####        line[index] = ""
####        index = index + 1
####        if(char != " "):
####            break;
##    line[0:10].replace(" ", "")
    line = line.lstrip()
    line = line.replace('\t', "")
    line = line.replace('\n', "")
    return line
        

for line in file:
    if line[0:2] == "  " and line[3] != " ":
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

    if counter > 50:
        break
    
    counter = counter + 1
    



##    
   
##    else:
##        if "NODE_" in line: 
##            countOfNodes = countOfNodes + 1
##        counter = counter + 1

#print(data[currTierOneCategory][currTierTwoCategory][currTierThreeCategory][1])

print("done")
print(len(data["Metabolism"]["Carbohydrate metabolism"]))
print(data["Metabolism"]["Carbohydrate metabolism"]["00010 Glycolysis / Gluconeogenesis [PATH:ko00010]"])
