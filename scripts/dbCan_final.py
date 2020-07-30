import os
import sys
import pandas as pd

#input files parsed by hmmscan-parser.sh
for arg in sys.argv[1:]:
	file=pd.read_table(arg, header=None)
	column_withCAZY=file[0]

#prime counters

	AA=0
	CBM=0
	GT=0
	CE=0
	GH=0
	PL=0
	SLH=0

#loop through each row of file and count CAZYs
	for item in column_withCAZY:
		if 'AA' in item:
			AA+=1
		if 'CBM' in item:
			CBM+=1
		if 'GH' in item:
			GH+=1
		if 'CE' in item:
			CE+=1
		if 'GH' in item:
			GH+=1
		if 'PL' in item:
			PL+=1
		if 'SLH' in item:
			SLH+=1
#add total counts to a dictionary
	dictionary={'AA': AA, 'CBM': CBM, 'GH': GH, 'PL': PL, 'SLH':SLH, 'CE':CE}
	#print(dictionary)

#write to file
	with open('summary.txt', 'a') as f:
		f.write(arg + ' ')
		for key, value in dictionary.items():
			f.write(str(value)+' ')
		f.write('\n')
#with this text file you can copy and paste results to an excel file
#then use the "text to columns" feature (under Data) and use space as your delimiter

