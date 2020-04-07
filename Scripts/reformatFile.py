fileName = '3715_brite.txt'
fileNameTest = 'random.txt'
file = open(fileNameTest, mode='r')
counter = 0
t1C = 0
t2C = 0
countOfNodes = 0

filedata = file.read()
file.close()

newdata = filedata.replace('\"', "")

file = open (fileNameTest, 'w')
file.write(newdata)
file.close()
