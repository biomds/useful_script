#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
if len(sys.argv) < 2:
	print "python",sys.argv[0],"<info.csv>"
	exit(1)
dic = {}
f = open(sys.argv[1],'r')
f.readline() # skip the first line
for i in f:
	i = i.strip().split(",")
	key,value = i[0],i[3]
	lst = dic.setdefault(key,[])
	lst.append(float(value))
for k in sorted(dic):
	s = sum(dic[k])
	print k,s

