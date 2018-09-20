#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
if len(sys.argv) < 2:
	print "python",sys.argv[0],"<info.csv>"
	exit(1)
dic_reads = {}
dic_bases = {}
dic_Q20 = {}
dic_Q30 = {} 
dic_GC = {}
dic_N = {}
f = open(sys.argv[1],'r')
f.readline() # skip the first line
for i in f:
	i = i.strip().split(",")
	lane,read,base,Q20,Q30,GC,N = i[0],i[2],i[3],i[4],i[5],i[6],i[7]
	#key,value = i[0],i[3]
	lst_reads = dic_reads.setdefault(lane,[])
	lst_reads.append(int(read))
	lst_bases = dic_bases.setdefault(lane,[])
	lst_bases.append(float(base))
	lst_Q20 = dic_Q20.setdefault(lane,[])
	lst_Q20.append(float(Q20))
	lst_Q30 = dic_Q30.setdefault(lane,[])
	lst_Q30.append(float(Q30))
	lst_GC = dic_GC.setdefault(lane,[])
	lst_GC.append(float(GC))
	lst_N = dic_N.setdefault(lane,[])
	lst_N.append(float(N))

dic_total = {}
for k in sorted(dic_reads):
	s = sum(dic_reads[k])
	lst_total = dic_total.setdefault(k,[])
	lst_total.append(s)
	#print k,s
for k in sorted(dic_bases):
	s = sum(dic_bases[k])
	s = "%.2f" % s
	lst_total = dic_total.setdefault(k,[])
	lst_total.append(s)
	#print k,s
for k in sorted(dic_Q20):
	s = sum(dic_Q20[k]) / len(dic_Q20[k])
	s = "%.2f" % s
	lst_total = dic_total.setdefault(k,[])
	lst_total.append(s)
	#print k,s
for k in sorted(dic_Q30):
	s = sum(dic_Q30[k]) / len(dic_Q30[k])
	s = "%.2f" % s
	lst_total = dic_total.setdefault(k,[])
	lst_total.append(s)
	#print k,s
for k in sorted(dic_GC):
	s = sum(dic_GC[k]) / len(dic_GC[k])
	s = "%.2f" % s
	lst_total = dic_total.setdefault(k,[])
	lst_total.append(s)
	#print k,s
for k in sorted(dic_N):
	s = sum(dic_N[k]) / len(dic_N[k])
	s = "%.2f" % s
	lst_total = dic_total.setdefault(k,[])
	lst_total.append(s)
	#print k,s
print "#########################"
head = "Lane,Reads,Base(G),Q20(%),Q30(%),GC(%),N(%)"
print head
for i in dic_total:
	a = dic_total[i]
	a = str(a)
	a = a.replace("'","") # replace "'" with ""
	a = a.replace("[","") # replace "[" with ""
	a = a.replace("]","") # replace "]" with ""
	a = a.replace(" ","") # replace " " with ""
	print i+","+a

###########################OUT like below####################################
'''
Lane,Reads,Base(G),Q20(%),Q30(%),GC(%),N(%)
L001,764708002,114.89,98.09,94.59,45.03,0.01
L002,753316752,111.07,98.53,96.06,47.50,0.03
L003,785620246,116.71,98.20,95.73,48.23,0.04
L004,795534574,118.21,98.78,96.58,48.74,0.02
'''
