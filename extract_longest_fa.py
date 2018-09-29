#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
Description: This script is used to extract the longest one from multipel line fasta file with the same id.
'''
import sys
from Bio import SeqIO
if len(sys.argv) < 2:
    print("python",sys.argv[0],"<fa>")
    exit(1)
fa = sys.argv[1]
out = fa.replace(".fa","_longest.fa")
long_out = open(out,'w')
dic = {}
for record in SeqIO.parse(fa, "fasta"):
    id = record.id
    seq = record.seq
    #print(id)
    #print(seq)
    lst = dic.setdefault(id,[])
    lst.append(seq)
for i in dic:
	len_max = 0
	max_len_seq = ""
	for each in dic[i]:
		if len(each) > len_max:
			len_max = len(each)
			max_len_seq = str(each)
	#print(">%s" % i)
	#print(str(max_len_seq))
	long_out.write(">%s" % i+"\n")
	start = 0
	end = start + 60
	while end < len_max:
		long_out.write(max_len_seq[start:end]+"\n")
		start = end
		end += 60
	while end >= len_max:
		long_out.write(max_len_seq[start:]+"\n")
		break
long_out.close()










