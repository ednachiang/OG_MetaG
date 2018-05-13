fileName = 'idba/3734.idba.brite.clean.txt'
    # This saves the path to your brite output file as fileName
    # fileName is saved in binary so it's uninterpretable to the human eye
fileNameTest = 'idba/3734.idba.brite.use.txt'
    # This will be the path to your output
file = open(fileName, mode='r')
    # This opens up the file and loads it in

filedata = file.read()
    # Performs the function "read" on variable "file"
    # Makes file interpretable to the human eye (words instead of binary)
    # Creates an array
file.close()
    # Closes the datastream
    # We don't need the binary mumbo-jumbo anymore and will only be working with filedata form here on out

newdata = filedata.replace('\"', "")
    # backslash is an escape character --> this signifies that you're searching for 1 quote
    # You use the backslash to search for special characters
    # Quotes are usually reserved for specifying strings, so you need the backslash to let python know that you're searching for it and it's not missing the second quote
    # You could use quotes instead of apostrophes, but we use apostrophe here to make it easier to read
    # Quotes & apostrophes are roughly equivalent
    
file = open(fileNameTest, 'w')
file.write(newdata)
file.close()
