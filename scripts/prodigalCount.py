prodigalOutput = '3715.ffn'
prodigal = open(prodigalOutput, mode="r")
counter = 0

for line in prodigal:
    if '>' in line:
        counter = counter+1

print(counter)

prodigal.close()