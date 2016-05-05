"""
Script written in Spyder ( Scientific PYthon Development EnviRonment)
Created on Mon Nov 9 19:27:51 2015
@author: Karina
"""
import pandas as pd
from pandas import DataFrame

#importing gff data and intragenic region data
df = pd.read_csv('C:/Users/Karina/Desktop/Jaspar/gff.csv')
df = df[df.nothing == 'gene']

df['geneid'] = df['geneid'].str[3:12]

del df['nothing']

df.columns = ['chromonumb', 'genestart', 'geneend', 'strand', 'geneid']

df2 = pd.read_csv('C:/Users/Karina/Desktop/Jaspar/data.csv')

df2['agi1'] = df2['gene ids'].str.extract('(.........)')
df2['agi2'] = df2['gene ids'].str.extract('(.........)')

del df2['gene ids']

df2['agi1'] = df2['agi1'].str[:9]
df2['agi2'] = df2['agi2'].str[1:]

df2.columns = ['motifid', 'strand', 'motifstart', 'motifend', 'agi1', 'agi2']

indexed_gff = df.set_index('geneid')

listofpairs = [] #will be the dataset containing dna motif to gene mapping

for i in df2.index: #working on a pair of gene at a time from the dataset provided
    gene1 = df2.agi1[i]
    gene2 = df2.agi2[i]
    if gene1 in indexed_gff.index and gene2 in indexed_gff.index: #making sure genes are also in gff dataset

        genestrand = (indexed_gff.strand.loc[[gene1]]).apply(str)
        gene1strand = genestrand[0]
        genestrand2 = (indexed_gff.strand.loc[[gene2]]).apply(str)
        gene2strand = genestrand2[0]#gene2strand

        motif = df2.motifid[i]#motifID
        motifstart = int(df2.motifstart[i])
        motifend = (df2.motifend[i])

        if gene1strand == gene2strand: #if two genes are on the same strand
            gene1start = int(indexed_gff.genestart.loc[[gene1]])
            gene1end = int(indexed_gff.geneend.loc[[gene1]])
            gene2start = int(indexed_gff.genestart.loc[[gene2]])#gene2start
            gene2end = int(indexed_gff.genestart.loc[[gene2]])#gene2end
            if gene1strand == '+':
                if motifend < gene1start:
                    if gene1start-motifend <= 3000 and (motif,gene1) not in \
                            listofpairs: #want to pair motif to gene which
                            # comes after it
                            listofpairs.append((motif,gene1))
                if motifend < cstart:
                    if gene2start-motifend <= 3000 and (motif,gene2) not in \
                            listofpairs:
                        listofpairs.append((motif,gene2))
                        i += 1
            elif gene2strand == '-':
                if motifend > gene1start:#want to pair motif to gene which comes after it
                    if motifendgene1start <= 3000 and (motif,gene1) not in \
                            listofpairs:
                        listofpairs.append((motif,gene1))
                if motifend > gene2start:
                    if motifendgene2start<=3000 and (motif,gene2) not in listofpairs:
                        listofpairs.append((motif,gene2))
                        i += 1
        elif gene1strand!= gene2strandr: #if two genes are not on the same strand
            gene1start = int(indexed_gff.genestart.loc[[gene1]])
            gene1end = int(indexed_gff.geneend.loc[[gene1]])
            gene2start = int(indexed_gff.genestart.loc[[gene2]])
            gene2end = int(indexed_gff.genestart.loc[[2]])

            if gene1strand == '-'and gene2strand == '+':
                if motifend > gene1start:
                    if motifend-gene1start <= 3000 and (motif,gene1) not in listofpairs:
                        listofpairs.append((motif,gene1))
                if motifend < gene2start:
                    if gene2start-motifend <= 3000 and (motif,gene2) not in listofpairs:
                        listofpairs.append((motif,gene2))
                        i += 1
            elif gene1 == '+' and gene2strand == '+':
                if motifend < gene1start:
                    if gene1start-motifend <= 3000 and (motif,gene1) not in \
                            listofpairs:
                        listofpairs.append((motif,gene1))
                if motifend > gene2start:
                    if motifend-gene2start <= 3000 and(motif,gene2) not in listofpairs:
                        listofpairs.append((motif,gene2))
                        i += 1
    else:
        i += 1
#open("output_data.csv.txt", "w").write("\n".join(("\t".join(item)) for item in listofpairs))