#!/usr/bin/python
# -*- coding:utf-8 -*-
__date__ = '20181007'
__author__ = 'hengbenxianfeng@163.com'
'''
Description: This script is used to sort a vcf file by chromosome and position for human project.
'''
import sys
if len(sys.argv) < 3:
	print("python",sys.argv[0],"<in_vcf> <out_vcf>")
	exit(1)
dic1 = {}
dic2 = {}
head = []
chr_list = ["chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX","chrY","chrM"]
in_vcf = sys.argv[1]
out_vcf = sys.argv[2]
f = open(in_vcf,'r')
o = open(out_vcf,'w')
for line in f:
	if line.startswith("#"): ## read header 
		o.write(line) ## write head out
	else:
		i = line.strip("\n").split("\t")
		Chr = i[0] ## chromosome
		pos = i[1] ## position
		key = Chr+'_'+pos ## key
		lst = dic1.setdefault(Chr,[]) ## a dictionary which key is chromosome and value is a position list 
		lst.append(pos) ## append position to a list
		dic2[key] = line ## a dictionary which key is chromosome combined with position and value is a total line
for ch in chr_list: ## read chr_list
	if ch in dic1:  ## judge whether dic1 contains everyone of chr_list
		for k in sorted(dic1[ch]): ## sort dic1's value
			key = ch + '_' + k ## build a new key
			o.write(dic2[key]) ## write body out of the vcf file to a sorted vcf file

f.close()
o.close()
