fileNameTest = 'idba/3775.idba.brite.use.txt'
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
currTierFourCategory = ""

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
        data[currTierOneCategory][currTierTwoCategory][currTierThreeCategory] = dict()
    elif line[0:8] == "        " and line[9] != " ":
        line = replaceStupidCharacters(line)
        currTierFourCategory = line
        data[currTierOneCategory][currTierTwoCategory][currTierThreeCategory][currTierFourCategory] = list()
        #data[currTierOneCategory][currTierTwoCategory][currTierThreeCategory].append(line)

        

def countContigsForLevelOneHeader(lvlOneHeader):
    count = 0; 
    for header2 in data[lvlOneHeader]:
        for header3 in data[lvlOneHeader][header2]:
            count = count + len(data[lvlOneHeader][header2][header3])
    return count;

def countContigsForLevelTwoHeader(lvlOneHeader, lvlTwoHeader):
    count = 0; 
    for entry in data[lvlOneHeader][lvlTwoHeader]:
        print(entry)
        count = count + len(data[lvlOneHeader][lvlTwoHeader][entry])
        print(count)
    return count;


def countContigsForLevelThreeHeader(lvlOneHeader, lvlTwoHeader, lvlThreeHeader):
    count = 0; 
    for lines in data[lvlOneHeader][lvlTwoHeader][lvlThreeHeader]:
        print(lines)
        count = count + len(data[lvlOneHeader][lvlTwoHeader][lvlThreeHeader][lines])
        print(count)
    return count;






print(len(data["Metabolism"]["Carbohydrate metabolism"]["00010 Glycolysis / Gluconeogenesis [PATH:ko00010]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00020 Citrate cycle (TCA cycle) [PATH:ko00020]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00030 Pentose phosphate pathway [PATH:ko00030]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00040 Pentose and glucuronate interconversions [PATH:ko00040]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00051 Fructose and mannose metabolism [PATH:ko00051]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00052 Galactose metabolism [PATH:ko00052]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00053 Ascorbate and aldarate metabolism [PATH:ko00053]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00500 Starch and sucrose metabolism [PATH:ko00500]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00520 Amino sugar and nucleotide sugar metabolism [PATH:ko00520]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00620 Pyruvate metabolism [PATH:ko00620]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00630 Glyoxylate and dicarboxylate metabolism [PATH:ko00630]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00640 Propanoate metabolism [PATH:ko00640]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00650 Butanoate metabolism [PATH:ko00650]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00660 C5-Branched dibasic acid metabolism [PATH:ko00660]"]))
print(len(data["Metabolism"]["Carbohydrate metabolism"]["00562 Inositol phosphate metabolism [PATH:ko00562]"]))

print(len(data["Metabolism"]["Energy metabolism"]["00190 Oxidative phosphorylation [PATH:ko00190]"]))
print(len(data["Metabolism"]["Energy metabolism"]["00195 Photosynthesis [PATH:ko00195]"]))
#print(len(data["Metabolism"]["Energy metabolism"]["00196 Photosynthesis - antenna proteins [PATH:ko00196]"]))
#print(len(data["Metabolism"]["Energy metabolism"]["00194 Photosynthesis proteins [BR:ko00194]"]))
print(len(data["Metabolism"]["Energy metabolism"]["00710 Carbon fixation in photosynthetic organisms [PATH:ko00710]"]))
print(len(data["Metabolism"]["Energy metabolism"]["00720 Carbon fixation pathways in prokaryotes [PATH:ko00720]"]))
print(len(data["Metabolism"]["Energy metabolism"]["00680 Methane metabolism [PATH:ko00680]"]))
print(len(data["Metabolism"]["Energy metabolism"]["00910 Nitrogen metabolism [PATH:ko00910]"]))
print(len(data["Metabolism"]["Energy metabolism"]["00920 Sulfur metabolism [PATH:ko00920]"]))

print(len(data["Metabolism"]["Lipid metabolism"]["00061 Fatty acid biosynthesis [PATH:ko00061]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00062 Fatty acid elongation [PATH:ko00062]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00071 Fatty acid degradation [PATH:ko00071]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00072 Synthesis and degradation of ketone bodies [PATH:ko00072]"]))
#print(len(data["Metabolism"]["Lipid metabolism"]["00073 Cutin, suberine and wax biosynthesis [PATH:ko00073]"]))
#print(len(data["Metabolism"]["Lipid metabolism"]["00100 Steroid biosynthesis [PATH:ko00100]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00120 Primary bile acid biosynthesis [PATH:ko00120]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00121 Secondary bile acid biosynthesis [PATH:ko00121]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00140 Steroid hormone biosynthesis [PATH:ko00140]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00561 Glycerolipid metabolism [PATH:ko00561]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00564 Glycerophospholipid metabolism [PATH:ko00564]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00565 Ether lipid metabolism [PATH:ko00565]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00600 Sphingolipid metabolism [PATH:ko00600]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00590 Arachidonic acid metabolism [PATH:ko00590]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00591 Linoleic acid metabolism [PATH:ko00591]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["00592 alpha-Linolenic acid metabolism [PATH:ko00592]"]))
print(len(data["Metabolism"]["Lipid metabolism"]["01040 Biosynthesis of unsaturated fatty acids [PATH:ko01040]"]))
#print(len(data["Metabolism"]["Lipid metabolism"]["01004 Lipid biosynthesis proteins [BR:ko01004]"]))

print(len(data["Metabolism"]["Nucleotide metabolism"]["00230 Purine metabolism [PATH:ko00230]"]))
print(len(data["Metabolism"]["Nucleotide metabolism"]["00240 Pyrimidine metabolism [PATH:ko00240]"]))

print(len(data["Metabolism"]["Amino acid metabolism"]["00250 Alanine, aspartate and glutamate metabolism [PATH:ko00250]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00260 Glycine, serine and threonine metabolism [PATH:ko00260]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00270 Cysteine and methionine metabolism [PATH:ko00270]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00280 Valine, leucine and isoleucine degradation [PATH:ko00280]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00290 Valine, leucine and isoleucine biosynthesis [PATH:ko00290]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00300 Lysine biosynthesis [PATH:ko00300]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00310 Lysine degradation [PATH:ko00310]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00220 Arginine biosynthesis [PATH:ko00220]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00330 Arginine and proline metabolism [PATH:ko00330]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00340 Histidine metabolism [PATH:ko00340]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00350 Tyrosine metabolism [PATH:ko00350]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00360 Phenylalanine metabolism [PATH:ko00360]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00380 Tryptophan metabolism [PATH:ko00380]"]))
print(len(data["Metabolism"]["Amino acid metabolism"]["00400 Phenylalanine, tyrosine and tryptophan biosynthesis [PATH:ko00400]"]))
#print(len(data["Metabolism"]["Amino acid metabolism"]["01007 Amino acid related enzymes [BR:ko01007]"]))
      
print(len(data["Metabolism"]["Metabolism of other amino acids"]["00410 beta-Alanine metabolism [PATH:ko00410]"]))
print(len(data["Metabolism"]["Metabolism of other amino acids"]["00430 Taurine and hypotaurine metabolism [PATH:ko00430]"]))
print(len(data["Metabolism"]["Metabolism of other amino acids"]["00440 Phosphonate and phosphinate metabolism [PATH:ko00440]"]))
print(len(data["Metabolism"]["Metabolism of other amino acids"]["00450 Selenocompound metabolism [PATH:ko00450]"]))
print(len(data["Metabolism"]["Metabolism of other amino acids"]["00460 Cyanoamino acid metabolism [PATH:ko00460]"]))
print(len(data["Metabolism"]["Metabolism of other amino acids"]["00471 D-Glutamine and D-glutamate metabolism [PATH:ko00471]"]))
print(len(data["Metabolism"]["Metabolism of other amino acids"]["00472 D-Arginine and D-ornithine metabolism [PATH:ko00472]"]))
print(len(data["Metabolism"]["Metabolism of other amino acids"]["00473 D-Alanine metabolism [PATH:ko00473]"]))
print(len(data["Metabolism"]["Metabolism of other amino acids"]["00480 Glutathione metabolism [PATH:ko00480]"]))

#print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["01003 Glycosyltransferases [BR:ko01003]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00510 N-Glycan biosynthesis [PATH:ko00510]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00513 Various types of N-glycan biosynthesis [PATH:ko00513]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00512 Mucin type O-glycan biosynthesis [PATH:ko00512]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00515 Mannose type O-glycan biosyntheis [PATH:ko00515]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00514 Other types of O-glycan biosynthesis [PATH:ko00514]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00532 Glycosaminoglycan biosynthesis - chondroitin sulfate / dermatan sulfate [PATH:ko00532]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00534 Glycosaminoglycan biosynthesis - heparan sulfate / heparin [PATH:ko00534]"]))
#print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00533 Glycosaminoglycan biosynthesis - keratan sulfate [PATH:ko00533]"]))
#print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00535 Proteoglycans [BR:ko00535]"]))
#print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00536 Glycosaminoglycan binding proteins [BR:ko00536]"]))
#print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00537 Glycosylphosphatidylinositol (GPI)-anchored proteins [BR:ko00537]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00531 Glycosaminoglycan degradation [PATH:ko00531]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00563 Glycosylphosphatidylinositol(GPI)-anchor biosynthesis [PATH:ko00563]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00601 Glycosphingolipid biosynthesis - lacto and neolacto series [PATH:ko00601]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00603 Glycosphingolipid biosynthesis - globo and isoglobo series [PATH:ko00603]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00604 Glycosphingolipid biosynthesis - ganglio series [PATH:ko00604]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00540 Lipopolysaccharide biosynthesis [PATH:ko00540]"]))
#print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["01005 Lipopolysaccharide biosynthesis proteins [BR:ko01005]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00550 Peptidoglycan biosynthesis [PATH:ko00550]"]))
#print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["01011 Peptidoglycan biosynthesis and degradation proteins [BR:ko01011]"]))
print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00511 Other glycan degradation [PATH:ko00511]"]))
#print(len(data["Metabolism"]["Glycan biosynthesis and metabolism"]["00571 Lipoarabinomannan (LAM) biosynthesis [PATH:ko00571]"]))
      
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00730 Thiamine metabolism [PATH:ko00730]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00740 Riboflavin metabolism [PATH:ko00740]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00750 Vitamin B6 metabolism [PATH:ko00750]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00760 Nicotinate and nicotinamide metabolism [PATH:ko00760]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00770 Pantothenate and CoA biosynthesis [PATH:ko00770]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00780 Biotin metabolism [PATH:ko00780]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00785 Lipoic acid metabolism [PATH:ko00785]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00790 Folate biosynthesis [PATH:ko00790]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00670 One carbon pool by folate [PATH:ko00670]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00830 Retinol metabolism [PATH:ko00830]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00860 Porphyrin and chlorophyll metabolism [PATH:ko00860]"]))
print(len(data["Metabolism"]["Metabolism of cofactors and vitamins"]["00130 Ubiquinone and other terpenoid-quinone biosynthesis [PATH:ko00130]"]))
      
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["01006 Prenyltransferases [BR:ko01006]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00900 Terpenoid backbone biosynthesis [PATH:ko00900]"]))
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00902 Monoterpenoid biosynthesis [PATH:ko00902]"]))
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00909 Sesquiterpenoid and triterpenoid biosynthesis [PATH:ko00909]"]))
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00904 Diterpenoid biosynthesis [PATH:ko00904]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00906 Carotenoid biosynthesis [PATH:ko00906]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00905 Brassinosteroid biosynthesis [PATH:ko00905]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00981 Insect hormone biosynthesis [PATH:ko00981]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00908 Zeatin biosynthesis [PATH:ko00908]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00903 Limonene and pinene degradation [PATH:ko00903]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00281 Geraniol degradation [PATH:ko00281]"]))
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["01008 Polyketide biosynthesis proteins [BR:ko01008]"]))
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["01052 Type I polyketide structures [PATH:ko01052]"]))
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00522 Biosynthesis of 12-, 14- and 16-membered macrolides [PATH:ko00522]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["01051 Biosynthesis of ansamycins [PATH:ko01051]"]))
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["01059 Biosynthesis of enediyne antibiotics [PATH:ko01059]"]))
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["01056 Biosynthesis of type II polyketide backbone [PATH:ko01056]"]))
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["01057 Biosynthesis of type II polyketide products [PATH:ko01057]"]))
#print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00253 Tetracycline biosynthesis [PATH:ko00253]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["00523 Polyketide sugar unit biosynthesis [PATH:ko00523]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["01054 Nonribosomal peptide structures [PATH:ko01054]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["01053 Biosynthesis of siderophore group nonribosomal peptides [PATH:ko01053]"]))
print(len(data["Metabolism"]["Metabolism of terpenoids and polyketides"]["01055 Biosynthesis of vancomycin group antibiotics [PATH:ko01055]"]))
      
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00940 Phenylpropanoid biosynthesis [PATH:ko00940]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00945 Stilbenoid, diarylheptanoid and gingerol biosynthesis [PATH:ko00945]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00941 Flavonoid biosynthesis [PATH:ko00941]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00944 Flavone and flavonol biosynthesis [PATH:ko00944]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00942 Anthocyanin biosynthesis [PATH:ko00942]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00943 Isoflavonoid biosynthesis [PATH:ko00943]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00901 Indole alkaloid biosynthesis [PATH:ko00901]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00403 Indole diterpene alkaloid biosynthesis [PATH:ko00403]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00950 Isoquinoline alkaloid biosynthesis [PATH:ko00950]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00960 Tropane, piperidine and pyridine alkaloid biosynthesis [PATH:ko00960]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["01058 Acridone alkaloid biosynthesis [PATH:ko01058]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00232 Caffeine metabolism [PATH:ko00232]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00965 Betalain biosynthesis [PATH:ko00965]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00966 Glucosinolate biosynthesis [PATH:ko00966]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00402 Benzoxazinoid biosynthesis [PATH:ko00402]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00311 Penicillin and cephalosporin biosynthesis [PATH:ko00311]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00332 Carbapenem biosynthesis [PATH:ko00332]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00261 Monobactam biosynthesis [PATH:ko00261]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00331 Clavulanic acid biosynthesis [PATH:ko00331]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00521 Streptomycin biosynthesis [PATH:ko00521]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00524 Neomycin, kanamycin and gentamicin biosynthesis [PATH:ko00524]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00525 Acarbose and validamycin biosynthesis [PATH:ko00525]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00231 Puromycin biosynthesis [PATH:ko00231]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00401 Novobiocin biosynthesis [PATH:ko00401]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00404 Staurosporine biosynthesis [PATH:ko00404]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00405 Phenazine biosynthesis [PATH:ko00405]"]))
print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00333 Prodigiosin biosyntheses [PATH:ko00333]"]))
#print(len(data["Metabolism"]["Biosynthesis of other secondary metabolites"]["00254 Aflatoxin biosynthesis [PATH:ko00254]"]))
      
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00362 Benzoate degradation [PATH:ko00362]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00627 Aminobenzoate degradation [PATH:ko00627]"]))
#print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00364 Fluorobenzoate degradation [PATH:ko00364]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00625 Chloroalkane and chloroalkene degradation [PATH:ko00625]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00361 Chlorocyclohexane and chlorobenzene degradation [PATH:ko00361]"]))
#print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00623 Toluene degradation [PATH:ko00623]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00622 Xylene degradation [PATH:ko00622]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00633 Nitrotoluene degradation [PATH:ko00633]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00642 Ethylbenzene degradation [PATH:ko00642]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00643 Styrene degradation [PATH:ko00643]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00791 Atrazine degradation [PATH:ko00791]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00930 Caprolactam degradation [PATH:ko00930]"]))
#print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00363 Bisphenol degradation [PATH:ko00363]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00621 Dioxin degradation [PATH:ko00621]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00626 Naphthalene degradation [PATH:ko00626]"]))
#print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00624 Polycyclic aromatic hydrocarbon degradation [PATH:ko00624]"]))
#print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00365 Furfural degradation [PATH:ko00365]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00984 Steroid degradation [PATH:ko00984]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00980 Metabolism of xenobiotics by cytochrome P450 [PATH:ko00980]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00982 Drug metabolism - cytochrome P450 [PATH:ko00982]"]))
print(len(data["Metabolism"]["Xenobiotics biodegradation and metabolism"]["00983 Drug metabolism - other enzymes [PATH:ko00983]"]))

print(len(data["Genetic Information Processing"]["Transcription"]["03020 RNA polymerase [PATH:ko03020]"]))
print(len(data["Genetic Information Processing"]["Transcription"]["03022 Basal transcription factors [PATH:ko03022]"]))
#print(len(data["Genetic Information Processing"]["Transcription"]["03000 Transcription factors [BR:ko03000]"]))
#print(len(data["Genetic Information Processing"]["Transcription"]["03021 Transcription machinery [BR:ko03021]"]))
print(len(data["Genetic Information Processing"]["Transcription"]["03040 Spliceosome [PATH:ko03040]"]))
#print(len(data["Genetic Information Processing"]["Transcription"]["03041 Spliceosome [BR:ko03041]"]))
      
print(len(data["Genetic Information Processing"]["Translation"]["03010 Ribosome [PATH:ko03010]"]))
#print(len(data["Genetic Information Processing"]["Translation"]["03011 Ribosome [BR:ko03011]"]))
#print(len(data["Genetic Information Processing"]["Translation"]["03016 Transfer RNA biogenesis [BR:ko03016]"]))
print(len(data["Genetic Information Processing"]["Translation"]["00970 Aminoacyl-tRNA biosynthesis [PATH:ko00970]"]))
print(len(data["Genetic Information Processing"]["Translation"]["03013 RNA transport [PATH:ko03013]"]))
print(len(data["Genetic Information Processing"]["Translation"]["03015 mRNA surveillance pathway [PATH:ko03015]"]))
#print(len(data["Genetic Information Processing"]["Translation"]["03019 Messenger RNA Biogenesis [BR:ko03019]"]))
print(len(data["Genetic Information Processing"]["Translation"]["03008 Ribosome biogenesis in eukaryotes [PATH:ko03008]"]))
#print(len(data["Genetic Information Processing"]["Translation"]["03009 Ribosome biogenesis [BR:ko03009]"]))
#print(len(data["Genetic Information Processing"]["Translation"]["03029 Mitochondrial biogenesis [BR:ko03029]"]))
#print(len(data["Genetic Information Processing"]["Translation"]["03012 Translation factors [BR:ko03012]"]))
      
#print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["03110 Chaperones and folding catalysts [BR:ko03110]"]))
print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["03060 Protein export [PATH:ko03060]"]))
print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["04141 Protein processing in endoplasmic reticulum [PATH:ko04141]"]))
#print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["04130 SNARE interactions in vesicular transport [PATH:ko04130]"]))
#print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["04131 Membrane trafficking [BR:ko04131]"]))
print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["04120 Ubiquitin mediated proteolysis [PATH:ko04120]"]))
#print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["04121 Ubiquitin system [BR:ko04121]"]))
print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["04122 Sulfur relay system [PATH:ko04122]"]))
print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["03050 Proteasome [PATH:ko03050]"]))
#print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["03051 Proteasome [BR:ko03051]"]))
print(len(data["Genetic Information Processing"]["Folding, sorting and degradation"]["03018 RNA degradation [PATH:ko03018]"]))
      
print(len(data["Genetic Information Processing"]["Replication and repair"]["03030 DNA replication [PATH:ko03030]"]))
#print(len(data["Genetic Information Processing"]["Replication and repair"]["03032 DNA replication proteins [BR:ko03032]"]))
#print(len(data["Genetic Information Processing"]["Replication and repair"]["03036 Chromosome and associated proteins [BR:ko03036]"]))
print(len(data["Genetic Information Processing"]["Replication and repair"]["03410 Base excision repair [PATH:ko03410]"]))
print(len(data["Genetic Information Processing"]["Replication and repair"]["03420 Nucleotide excision repair [PATH:ko03420]"]))
print(len(data["Genetic Information Processing"]["Replication and repair"]["03430 Mismatch repair [PATH:ko03430]"]))
print(len(data["Genetic Information Processing"]["Replication and repair"]["03440 Homologous recombination [PATH:ko03440]"]))
print(len(data["Genetic Information Processing"]["Replication and repair"]["03450 Non-homologous end-joining [PATH:ko03450]"]))
print(len(data["Genetic Information Processing"]["Replication and repair"]["03460 Fanconi anemia pathway [PATH:ko03460]"]))
#print(len(data["Genetic Information Processing"]["Replication and repair"]["03400 DNA repair and recombination proteins [BR:ko03400]"]))

#print(len(data["Environmental Information Processing"]["Membrane transport"]["02000 Transporters [BR:ko02000]"]))
print(len(data["Environmental Information Processing"]["Membrane transport"]["02010 ABC transporters [PATH:ko02010]"]))
print(len(data["Environmental Information Processing"]["Membrane transport"]["02060 Phosphotransferase system (PTS) [PATH:ko02060]"]))
print(len(data["Environmental Information Processing"]["Membrane transport"]["03070 Bacterial secretion system [PATH:ko03070]"]))
#print(len(data["Environmental Information Processing"]["Membrane transport"]["02044 Secretion system [BR:ko02044]"]))
      
print(len(data["Environmental Information Processing"]["Signal transduction"]["02020 Two-component system [PATH:ko02020]"]))
#print(len(data["Environmental Information Processing"]["Signal transduction"]["02022 Two-component system [BR:ko02022]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04014 Ras signaling pathway [PATH:ko04014]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04015 Rap1 signaling pathway [PATH:ko04015]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04010 MAPK signaling pathway [PATH:ko04010]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04011 MAPK signaling pathway - yeast [PATH:ko04011]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04012 ErbB signaling pathway [PATH:ko04012]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04310 Wnt signaling pathway [PATH:ko04310]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04330 Notch signaling pathway [PATH:ko04330]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04340 Hedgehog signaling pathway [PATH:ko04340]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04350 TGF-beta signaling pathway [PATH:ko04350]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04390 Hippo signaling pathway [PATH:ko04390]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04392 Hippo signaling pathway - multiple species [PATH:ko04392]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04370 VEGF signaling pathway [PATH:ko04370]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04371 Apelin signaling pathway [PATH:ko04371]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04630 Jak-STAT signaling pathway [PATH:ko04630]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04064 NF-kappa B signaling pathway [PATH:ko04064]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04668 TNF signaling pathway [PATH:ko04668]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04066 HIF-1 signaling pathway [PATH:ko04066]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04068 FoxO signaling pathway [PATH:ko04068]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04020 Calcium signaling pathway [PATH:ko04020]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04070 Phosphatidylinositol signaling system [PATH:ko04070]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04072 Phospholipase D signaling pathway [PATH:ko04072]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04071 Sphingolipid signaling pathway [PATH:ko04071]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04024 cAMP signaling pathway [PATH:ko04024]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04022 cGMP - PKG signaling pathway [PATH:ko04022]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04151 PI3K-Akt signaling pathway [PATH:ko04151]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04152 AMPK signaling pathway [PATH:ko04152]"]))
print(len(data["Environmental Information Processing"]["Signal transduction"]["04150 mTOR signaling pathway [PATH:ko04150]"]))

#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04030 G protein-coupled receptors [BR:ko04030]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04050 Cytokine receptors [BR:ko04050]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["03310 Nuclear receptors [BR:ko03310]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04040 Ion channels [BR:ko04040]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04031 GTP-binding proteins [BR:ko04031]"]))
print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04080 Neuroactive ligand-receptor interaction [PATH:ko04080]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04060 Cytokine-cytokine receptor interaction [PATH:ko04060]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04052 Cytokines and growth factors [BR:ko04052]"]))
print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04512 ECM-receptor interaction [PATH:ko04512]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04514 Cell adhesion molecules (CAMs) [PATH:ko04514]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04515 Cell adhesion molecules [BR:ko04515]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04090 CD Molecules [BR:ko04090]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["04091 Lectins [BR:ko04091]"]))
#print(len(data["Environmental Information Processing"]["Signaling molecules and interaction"]["02042 Bacterial toxins [BR:ko02042] "]))
      
print(len(data["Cellular Processes"]["Transport and catabolism"]["04144 Endocytosis [PATH:ko04144]"]))
print(len(data["Cellular Processes"]["Transport and catabolism"]["04145 Phagosome [PATH:ko04145]"]))
print(len(data["Cellular Processes"]["Transport and catabolism"]["04142 Lysosome [PATH:ko04142]"]))
print(len(data["Cellular Processes"]["Transport and catabolism"]["04146 Peroxisome [PATH:ko04146]"]))
print(len(data["Cellular Processes"]["Transport and catabolism"]["04138 Autophagy - yeast [PATH:ko04138]"]))
print(len(data["Cellular Processes"]["Transport and catabolism"]["04136 Autophagy - other eukaryotes [PATH:ko04136]"]))
print(len(data["Cellular Processes"]["Transport and catabolism"]["04139 Mitophagy - yeast [PATH:ko04139]"]))
#print(len(data["Cellular Processes"]["Transport and catabolism"]["02048 Prokaryotic Defense System [BR:ko02048]"]))

print(len(data["Cellular Processes"]["Cell growth and death"]["04110 Cell cycle [PATH:ko04110]"]))
print(len(data["Cellular Processes"]["Cell growth and death"]["04111 Cell cycle - yeast [PATH:ko04111]"]))
print(len(data["Cellular Processes"]["Cell growth and death"]["04112 Cell cycle - Caulobacter [PATH:ko04112]"]))
print(len(data["Cellular Processes"]["Cell growth and death"]["04113 Meiosis - yeast [PATH:ko04113]"]))
print(len(data["Cellular Processes"]["Cell growth and death"]["04210 Apoptosis [PATH:ko04210]"]))
print(len(data["Cellular Processes"]["Cell growth and death"]["04216 Ferroptosis [PATH:ko04216]"]))

print(len(data["Cellular Processes"]["Cellular community - prokaryotes"]["02024 Quorum sensing [PATH:ko02024]"]))
print(len(data["Cellular Processes"]["Cellular community - prokaryotes"]["05111 Biofilm formation - Vibrio cholerae [PATH:ko05111]"]))
print(len(data["Cellular Processes"]["Cellular community - prokaryotes"]["02025 Biofilm formation - Pseudomonas aeruginosa [PATH:ko02025]"]))
print(len(data["Cellular Processes"]["Cellular community - prokaryotes"]["02026 Biofilm formation - Escherichia coli [PATH:ko02026]"]))

print(len(data["Cellular Processes"]["Cell motility"]["02030 Bacterial chemotaxis [PATH:ko02030]"]))
#print(len(data["Cellular Processes"]["Cell motility"]["02035 Bacterial motility proteins [BR:ko02035]"]))
print(len(data["Cellular Processes"]["Cell motility"]["02040 Flagellar assembly [PATH:ko02040]"]))
print(len(data["Cellular Processes"]["Cell motility"]["04810 Regulation of actin cytoskeleton [PATH:ko04810]"]))
#print(len(data["Cellular Processes"]["Cell motility"]["04812 Cytoskeleton proteins [BR:ko04812]"]))




#print(countContigsForLevelTwoHeader("Metabolism", "Carbohydrate metabolism"))
#print(countContigsForLevelThreeHeader("Metabolism", "Carbohydrate metabolism", "00010 Glycolysis / Gluconeogenesis [PATH:ko00010]"))

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


#celproc = countContigsForLevelOneHeader("Cellular Processes")
#orgsys = countContigsForLevelOneHeader("Organismal Systems")
#humdis = countContigsForLevelOneHeader("Human Diseases")
#other = celproc + orgsys + humdis
      
#f = open('3715.phylip.use.csv', "w")

##f.write("Metabolism" + "," + str(countContigsForLevelOneHeader("Metabolism")) + '\n');
##f.write("Metabolism: Carbohydrate metabolism" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Carbohydrate metabolism"))+ '\n');
##f.write("Metabolism: NRG metabolism" + "," + str(countContigsForLevelTwoHeader("Metabolism", "Energy metabolism"))+ '\n');
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
##f.write("Genetic Information Processing: Transcription" + "," + str(countContigsForLevelTwoHeader("Genetic Information Processing", "Transcription"))+ '\n');
##f.write("Genetic Information Processing: Tranlation" + "," + str(countContigsForLevelTwoHeader("Genetic Information Processing", "Translation"))+ '\n');
##f.write("Genetic Information Processing: Fold sort degr" + "," + str(countContigsForLevelTwoHeader("Genetic Information Processing", "Folding, sorting and degradation"))+ '\n');
##f.write("Genetic Information Processing: Replication and repair" + "," + str(countContigsForLevelTwoHeader("Genetic Information Processing", "Replication and repair"))+ '\n');
###f.write("Genetic Information Processing: RNA family" + "," + str(countContigsForLevelTwoHeader("Genetic information processing", "RNA family")+ '\n'));
##f.write("Environ Info Process" + "," + str(countContigsForLevelOneHeader("Environmental Information Processing"))+ '\n');
##f.write("Environ Info Process: Membrane transport" + "," + str(countContigsForLevelTwoHeader("Environmental Information Processing", "Membrane transport"))+ '\n');
##f.write("Environ Info Process: Signal transduction" + "," + str(countContigsForLevelTwoHeader("Environmental Information Processing", "Signal transduction"))+ '\n');
##f.write("Environ Info Process: Signal molec and interact" + "," + str(countContigsForLevelTwoHeader("Environmental Information Processing", "Signaling molecules and interaction"))+ '\n');
##f.write("Other" + "," + str(other)+ '\n')

#f.write("ko00010" + "," + str(countContigsF

#f.write(countContigsForLevelThreeHeader("Metabolism", "Carbohydrate metabolism", "00010 Glycolysis / Gluconeogenesis [PATH:ko00010]"))


#f.close()






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
