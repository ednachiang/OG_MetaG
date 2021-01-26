##### CHANGE THESE PARAMETERS ACCORDINGLY
pathWhog = '../cog/whog'
    # Path to whog file
pathOutput = '../cog/cog.classifications.tab'
    # Path to output file

whog = open(pathWhog, mode="r")
output = open(pathOutput, 'w')


for line in whog:
    if '[' in line:
        # Pull out lines with COG annotation
        row = line.split(' ')
            # Split line by space
        annotation = line.split(' ')
            # Split line by space; this will be used to pull out annotation name
        annotation.pop(0)
            # Remove first item (category)
        annotation.pop(0)
            # Remove first item (originally 2nd item in line) (COG)
        output.write(row[1] + '\t' + row[0] + '\t' + str(annotation) + '\n')
            # Save to output. Column order = COG, Category, Annotation

whog.close()
output.close()
