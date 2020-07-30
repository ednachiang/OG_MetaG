import csv
	# To convert dictionary into csv output
import sys
	# To format csv output
import pandas as pd
from pandas import DataFrame


dbcanOutput = 'test.txt'
dbcan = open(dbcanOutput, mode='r')
#outputFile = open('test.summary.csv', 'w')
#output = csv.writer(outputFile, sys.stdout, lineterminator="\n")
	# Creates csv file and ensures correct formatting (no extra new line character)
char1 = '.'
char2 = "_"
dbcanDict = { }


for line1 in dbcan.readlines():
# Read file line-by-line

	col = line1.split('\t')
	# Split the row by tabs

	if 'hmm' in col[1]:
	# Pull out only lines that specify dbCAN classification in col 2. The last 7 lines summarize each class and don't contain hmm, so we want to exclude them.
		print(col[1])
		split1 = col[1].split(char1, 1)[0]
			# Pull out everything before the ".hmm"
		print(split1)
		split2 = split1.split(char2, 1)[0]
			# Pull out everything before subfamily classification-- right now I only care about the family-level classification
		print(split2)

		if split2 in dbcanDict:
		# For CAZyme family that's already in the dictionary
			dbcanDict[split2] = dbcanDict[split2] + 1
			# Add one to the family counter
			print(dbcanDict[split2])
		else:
		# For CAZyme family that's not in the dictionary yet
			dbcanDict[split2] = 1
			# Add family to dictionary and start counter
			print(dbcanDict[split2])

print(dbcanDict)

df = DataFrame(list(dbcanDict.items()), columns=['Family', 'Count'])
	# Convert dictionary to dataframe so I can add a class-level classification column
df['Class'] = df['Family'].str[:2]
df = df.set_index('Family')
print(df)

#df.to_csv(r'test.csv')

# Convert dictionary into csv file
#for key, val in dbcanDict.items():
#	output.writerow([key,val])

#for line2 in output:
#	output["Class"] = line2[1:3]
#	print(line2)




dbcan.close()
#outputFile.close()