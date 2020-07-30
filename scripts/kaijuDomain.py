kaiju = '3715.kaiju.output.names'
input = open(kaiju, mode='r')
counterArc = 0
counterBac = 0
counterEuk = 0
counterVir = 0
counterNA = 0
counterUnc = 0
output = open('3715.domain.count', mode='w')

for line in input:
	if 'Archaea' in line:
		counterArc = counterArc + 1
		continue
	elif 'Bacteria' in line:
		counterBac = counterBac + 1
		continue
	elif 'Eukaryota' in line:
		counterEuk = counterEuk + 1
		continue
	elif 'Virus' in line:
		counterVir = counterVir + 1
		continue
	elif 'NA' in line:
		counterNA = counterNA + 1
	else:
		counterUnc = counterUnc + 1
		continue

output.write('Archaea = ' + str(counterArc) + '\n')
output.write('Bacteria = ' + str(counterBac) + '\n')
output.write('Eukaryota = ' + str(counterEuk) + '\n')
output.write('Viruses = ' + str(counterVir) + '\n')
output.write('NA = ' + str(counterNA) + '\n')
output.write('Unclassified = ' + str(counterUnc) + '\n')
output.write('Total Unclassified = ' + str(counterNA + counterUnc) + '\n')
output.write('Total Classified = ' + str(counterArc + counterBac + counterEuk + counterVir) + '\n')
output.write('Total Sequences = ' + str(counterArc + counterBac + counterEuk + counterVir + counterNA + counterUnc))
#output.append("Bacteria = " % counterBac)
#output.append("Eukaryota = " % counterEuk)
#output.append("Viruses = " % counterVir)
#output.append("NA = " % counterNA)
#output.append("Unclassified = " % counterUnc)
input.close()
output.close()
