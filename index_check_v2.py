#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Chen Cheng'
__date__ = '20180814'

import os
import xlrd
import sys
work = xlrd.open_workbook("Barcode-collections.xlsx")
f = open("index.txt",'r')
index = []
for dex in f:
    dex = dex.strip().split("\t")
    index.append(dex)
sheets = work.sheet_names() #sheets=['ctdna2.0-dual-10', 'ctdna2.0-dual-8', '96-Dual', '10X-Single', '96-Single', '24-Single', '94-DU']
sheets.remove("ctdna2.0-dual-8")
sheets.remove("10X-Single")
print (sheets)

table = []
for sheet in sheets:
    book = work.sheet_by_name(sheet)
    row_n = book.nrows
    for i in range(1,row_n):
        row_value = book.row_values(i)
        tmp = [sheet] + row_value # add indexpool,[sheet] is now a list
        table.append(tmp)
new_table = []
for i in table:
    if "" in i:
        i[4],i[5],i[6] = ".",".","."
        new_table.append(i)
    else:
        new_table.append(i)
result = []
for each in index:
    if len(each) == 4:
        p7_name = each[0]
        p7_seq = each[1]
        p5_name = each[2]
        p5_seq = each[3]
        print(each)
        for i in new_table:
            alldiff = 0
            p7diff = 0
            p5diff = 0
            if len(p7_seq) == 8:
                for j in range(8):
                    if i[5] != ".":
                        if p7_seq[j] != i[3][j]:
                            p7diff += 1
                        if p5_seq[j] != i[5][j]:
                            p5diff += 1
                    if i[5] == ".":
                        if p7_seq[j] != i[3][j]:
                            p7diff += 1
                    alldiff = p7diff + p5diff
                new=[p7_name,p7_seq,p5_name,p5_seq,"===",alldiff,p7diff,p5diff]
                tmp = new + i
                result.append(tmp) 
            if len(p7_seq) == 10:
                if len(i[3]) == 10:
                    for j in range(10):
                        if i[5] != ".":
                            if p7_seq[j] != i[3][j]:
                                p7diff += 1
                            if p5_seq[j] != i[5][j]:
                                p5diff += 1
                        if i[5] == ".":
                            if p7_seq[j] != i[3][j]:
                                p7diff += 1
                        alldiff = p7diff + p5diff
                    new=[p7_name,p7_seq,p5_name,p5_seq,"===",alldiff,p7diff,p5diff]
                    tmp = new + i
                    result.append(tmp)
                if len(i[3]) == 8:
                    for j in range(8):
                        if i[5] != ".":
                            if p7_seq[j] != i[3][j]:
                                p7diff += 1
                            if p5_seq[j] != i[5][j]:
                                p5diff += 1
                        if i[5] == ".":
                            if p7_seq[j] != i[3][j]:
                                p7diff += 1
                                #i[4] = "."
                                #i[5] = "."
                                #i[6] = "."    
                        alldiff = p7diff + p5diff
                new=[p7_name,p7_seq,p5_name,p5_seq,"===",alldiff,p7diff,p5diff]
                tmp = new + i
                result.append(tmp)
                #print(p7_name,p7_seq,p5_name,p5_seq,"===",alldiff,p7diff,p5diff,i)
    if len(each) == 2:
        p7_name = each[0]
        p7_seq = each[1]
        p5_name = "."
        p5_seq = "."
        print(each)
        for i in new_table:
            alldiff = 0
            p7diff = 0
            p5diff = 0
            if len(p7_seq) == 8:
                for j in range(8):
                    if p7_seq[j] != i[3][j]:
                        p7diff += 1
                alldiff = p7diff + p5diff
            new=[p7_name,p7_seq,p5_name,p5_seq,"===",alldiff,p7diff,p5diff]
            tmp = new + i
            result.append(tmp)
            if len(p7_seq) == 10:
                if len(i[3]) == 10:
                    for j in range(10):
                        if p7_seq[j] != i[3][j]:
                            p7diff += 1
                    alldiff = p7diff + p5diff
                elif len(i[3]) == 8:
                    for j in range(8):
                        if p7_seq[j] != i[3][j]:
                            p7diff += 1
                    alldiff = p7diff + p5diff
                else:
                    pass
                new=[p7_name,p7_seq,p5_name,p5_seq,"===",alldiff,p7diff,p5diff]
                tmp = new + i
                result.append(tmp)
                #print(result)
                #rint(p7_name,p7_seq,p5_name,p5_seq,"===",alldiff,p7diff,p5diff,i)
dic = {}
out = open("index_check.csv",'w')
header = ["InP7ID","InP7Seq","InP5ID","InP5Seq","===","AllDiff","P7Diff","P5Diff","IndexPool","CheckedID","P7ID","P7Seq","P5ID","P5Seq","P5Seq(NovaSeq)"]
#header = str(header)
#header = header.replace("[","")
#header = header.replace("]","")
#header = header.replace("'","")
header = ','.join(header)
print(header)
out.write(header+"\n")
for i in result:
    tmp = str(i)
    dic[tmp] = i[5]
for k,v in sorted(dic.items(),key=lambda x:x[1]):
    k = k.replace("[","")
    k = k.replace("]","")
    k = k.replace("'","")
    k = k.replace(" ","")
    out.write(k+"\n")
    print((k))
out.close()
