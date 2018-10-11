#!/usr/bin/python
# -*- coding:utf-8 -*-
import csv
#import xlwt
from xlsxwriter import Workbook
import subprocess
import sys
import os
import gzip
import pandas as pd
if len(sys.argv) < 3:
	print("python",sys.argv[0],"<info.csv.bak> <info.csv.bak_dir>")
	print("Example:\npython",sys.argv[0],"info.csv.bak L1-SR16008")
	exit(1)
info_bak = sys.argv[1]
csv_out = open(sys.argv[2] + ".csv",'w')

info_dir = os.path.realpath(info_bak)
FC = info_dir.split("/")[3].split("_")[-1]

SampleSheet = ""
BCL_dirs = ["/GPFS02/SequencingData2","/GPFS04/SequencingData4"]
for Dir in BCL_dirs:
	sheet = subprocess.call("ls %s/*%s/SampleSheet.csv >/dev/null 2>&1 " %(Dir,FC),shell = True) ## ">/dev/null 2>&1" skip superfluous information
	if sheet == 2: ## SampleSheet.csv does not exist in this dir
		pass
	if sheet == 0: ## SampleSheet.csv exists in this dir
		SampleSheet = "%s/*%s/SampleSheet.csv" % (Dir,FC)
head = subprocess.check_output("grep Sample_ID %s " % SampleSheet,shell = True).strip().split(",")
head_len = len(head)
#print(head_len)
############# info.csv.bak2csv###########
f = open(info_bak,'r')
dic = {}
head = "Sample ID,index,Reads,Length,Total_base(Mbases),GC(%),Q20(%),Q30(%)"
csv_out.write(head+"\n")
for n,line in enumerate(f):
	if line.startswith("#"):
		continue
	i = line.strip().split(",")
	n = n+1
	if(n -4) % 4 == 2:
		fq1,read1_n,len1,base1_n,GC_1,Q20_1,Q30_1 = i[0],i[1],i[2],float(i[3]),float(i[4]),float(i[5]),float(i[6])
	if (n % 4) == 0:
		fq2,read2_n,len2,base2_n,GC_2,Q20_2,Q30_2 = i[0],i[1],i[2],float(i[3]),float(i[4]),float(i[5]),float(i[6])
		tmp_name = fq1.split("_")
		sample = tmp_name[0]
		lane = tmp_name[2][3]
		sample_id = tmp_name[0] + "_" + tmp_name[2]
		index = ""
		if "Undetermined" in fq2:
			index = "-"
		else:
			if head_len == 11:
				p7_index = subprocess.check_output("grep ^%s, %s|grep %s |cut -f 7 -d , " % (lane,SampleSheet,sample),shell=True).strip()
				p5_index = subprocess.check_output("grep ^%s, %s|grep %s |cut -f 9 -d , " % (lane,SampleSheet,sample),shell=True).strip()
				if p5_index.count("N") == len(p5_index):
					index = p7_index.replace("N","")
		#elif p5_index.count("N") > 0 and p5_index.count("N") < len(p5_index):
		#	index = index = p7_index.replace("N","")+ "+" + p5_index.replace("N","")  
				else:
					index = p7_index.replace("N","")+ "+" + p5_index.replace("N","")
			if head_len == 9:
				p7_index = subprocess.check_output("grep ^%s, %s|grep %s |cut -f 7 -d , " % (lane,SampleSheet,sample),shell=True).strip()
				index = p7_index.replace("N","")
			else:#if head_len != 9 or head_len != 11:
			#print ("Error SampleSheet header")
				pass
		reads = str(read1_n)
		length = str(len1)
		total_bases = "%.2f" % (base1_n + base2_n)
		GC = "%.2f" % ((GC_1 + GC_2) / 2)
		Q20 = "%.2f" % ((Q20_1 + Q20_2) / 2)
		Q30 = "%.2f" % ((Q30_1 + Q30_2) / 2)
		
		lst=[sample_id,index,reads,length,total_bases,GC,Q20,Q30]
		lst = ",".join(lst)
		dic[fq2] = lst   
		#csv_out.write(lst+"\n")
f.close()
for k,v in sorted(dic.items(),key=lambda i:i[0]): ##sort by key
	csv_out.write(v+"\n")
csv_out.close()

###########csv2xlsx############
csv_file = sys.argv[2] + ".csv"
f = open(csv_file,"r")
read = csv.reader(f)
xlsx_out = sys.argv[2] + ".xlsx"
workbook = Workbook(xlsx_out)
worksheet =workbook.add_worksheet()
for r,row in enumerate(read):
	for c,col in enumerate(row):
		worksheet.write(r,c,col)
