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
	a = a.replace("'","")
	a = a.replace("[","")
	a = a.replace("]","")
	a = a.replace(" ","")
	print i+","+a
