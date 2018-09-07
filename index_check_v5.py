#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Chen Cheng'
__date__ = '20180906'

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
        #print(each)
        for i in new_table:
            #print(i)
            alldiff = 0
            p7diff = 0
            p5diff = 0
            if len(p7_seq) == 6:
                for j in range(6):
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
        #print(each)
        for i in new_table:
            alldiff = 0
            p7diff = 0
            p5diff = 0
            if len(p7_seq) == 6:
                for j in range(6):
                    if p7_seq[j] != i[3][j]:
                        p7diff += 1
                alldiff = p7diff + p5diff
                new=[p7_name,p7_seq,p5_name,p5_seq,"===",alldiff,p7diff,p5diff]
                tmp = new + i
                result.append(tmp)
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
                if len(i[3]) == 8:
                    for j in range(8):
                        if p7_seq[j] != i[3][j]:
                            p7diff += 1
                    alldiff = p7diff + p5diff
                    new=[p7_name,p7_seq,p5_name,p5_seq,"===",alldiff,p7diff,p5diff]
                    tmp = new + i
                    result.append(tmp)
dic = {}
out = open("index_check.csv",'w')
header = ["InP7ID","InP7Seq","InP5ID","InP5Seq","===","AllDiff","P7Diff","P5Diff","IndexPool","CheckedID","P7ID","P7Seq","P5ID","P5Seq","P5Seq(NovaSeq)"]
header = ','.join(header)
#print(header)
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
#    print((k))
out.close()
#################index treat########################
index1 = []
index2 = []
result_index = []
def index_append(index):
    f_index = open("index.txt",'r')
    for each in f_index:
        each = each.strip()
        if each not in index:
            index.append(each)
    f_index.close()
index_append(index1)
index_append(index2)
for i in index1:
    tmp1 = i.split()
    if len(tmp1) == 2:
        tmp1.append(".")
        tmp1.append(".")
    else:
        pass
    for j in index2:
        tmp2 = j.split()
        if len(tmp2) == 2:
            tmp2.append(".")
            tmp2.append(".")
        else:
            pass
        #print(tmp1,tmp2)
        alldiff_index = 0
        p7diff_index = 0
        p5diff_index = 0
        if tmp1[3] !="." and tmp2[3] !=".":
            if len(tmp1[1]) == 6:
                for n in range(6):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                    if tmp1[3][n] != tmp2[3][n]:
                        p5diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
                #print(tmp_index)
                #print(tmp1,tmp2,alldiff_index,p7diff_index,p5diff_index)
            if len(tmp1[1]) == 8 and len(tmp2[1]) ==6:
                for n in range(6):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                    if tmp1[3][n] != tmp2[3][n]:
                        p5diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
            if len(tmp1[1]) == 8 and len(tmp2[1]) >=8:
                for n in range(8):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                    if tmp1[3][n] != tmp2[3][n]:
                        p5diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
                #print(tmp_index)
                #print(tmp1,tmp2,alldiff_index,p7diff_index,p5diff_index)
            if len(tmp1[1]) == 10 and len(tmp2[1]) ==6:
                for n in range(6):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                    if tmp1[3][n] != tmp2[3][n]:
                        p5diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
                #print(tmp_index)
                #result_index = 
                #print(tmp1,tmp2,alldiff_index,p7diff_index,p5diff_index)            
            if len(tmp1[1]) == 10 and len(tmp2[1]) ==8:
                for n in range(8):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                    if tmp1[3][n] != tmp2[3][n]:
                        p5diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
                #print(tmp_index)
                #print(tmp1,tmp2,alldiff_index,p7diff_index,p5diff_index)
            if len(tmp1[1]) == 10 and len(tmp2[1]) ==10:
                for n in range(10):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                    if tmp1[3][n] != tmp2[3][n]:
                        p5diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
                #print(tmp_index)
                #print(tmp1,tmp2,alldiff_index,p7diff_index,p5diff_index)           
        if tmp1[3] =="." or tmp2[3] ==".":
            if len(tmp1[1]) == 6:
                for n in range(6):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
                #print(tmp_index)
                #print(tmp1,tmp2,alldiff_index,p7diff_index,p5diff_index)
            if len(tmp1[1]) == 8 and len(tmp2[1]) ==6:
                for n in range(6):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
            if len(tmp1[1]) == 8 and len(tmp2[1]) >=8:
                for n in range(8):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
                #print(tmp_index)
                #print(tmp1,tmp2,alldiff_index,p7diff_index,p5diff_index)
            if len(tmp1[1]) == 10 and len(tmp2[1]) ==6:
                for n in range(6):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
                #print(tmp_index)
                #print(tmp1,tmp2,alldiff_index,p7diff_index,p5diff_index)            
            if len(tmp1[1]) == 10 and len(tmp2[1]) ==8:
                for n in range(8):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
                #print(tmp_index)
                #print(tmp1,tmp2,alldiff_index,p7diff_index,p5diff_index)
            if len(tmp1[1]) == 10 and len(tmp2[1]) ==10:
                for n in range(10):
                    if tmp1[1][n] != tmp2[1][n]:
                        p7diff_index += 1
                alldiff_index = p7diff_index + p5diff_index
                tmp_index = [tmp1,"===",alldiff_index,p7diff_index,p5diff_index,tmp2]
                result_index.append(tmp_index)
                #print(tmp_index)
                #print(tmp1,tmp2,alldiff_index,p7diff_index,p5diff_index)                      
header_index = ["P7ID_1","P7Seq_1","P5ID_1","P5Seq_1","===","AllDiff","P7Diff","P5Diff","P7ID_2","P7Seq_2","P5ID_2","P5Seq_2"]            
header_index = ','.join(header_index)
print(header_index)
o_index = open("out_index_check.csv","w")
o_index.write(header_index+"\n")
dic_index = {}
for i in result_index:
    if i[0] == i[5]:
        pass
    else:
        k=str(i)
        dic_index[k]=i[2]
for k,v in sorted(dic_index.items(),key=lambda x:x[1]):
    key = k
    key = key.replace("'","")
    key = key.replace("[","")
    key = key.replace("]","")
    o_index.write(key+"\n") 
o_index.close()