#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
Description: 
	This script is used to extract the bases of samples and undertermined ones from the json files and then combine the output files to an excel file named with flow cell
Author: 
	Cheng Chen
Email:
	hengbenxianfeng@163.com
Date:
	20180724 14:00
'''
import sys
import os
import json
import re
import glob
if len(sys.argv) < 3:
	print("python3",sys.argv[0],"json_path Flow_cell")
	exit(1)
js_path = sys.argv[1] #BCLTMP
js = glob.glob(js_path+"/L00*/Data/Intensities/BaseCalls/Stats/*json")
for in_file in js:
	lane = in_file.split("/")[1]
	out_file = lane + "_stat.txt"
	with open(in_file,'r') as f:
		ou = open(out_file,'w')
		data = json.load(f)
		dic={}
		for a in data["ConversionResults"]:
			for b in a["DemuxResults"]:
				for c in b["IndexMetrics"]:
                #print (c["IndexSequence"],"\t",b["Yield"])
					#ou.write('\t'.join([c["IndexSequence"],str(b["Yield"]),b["SampleName"]])+"\n")
					lst=[c["IndexSequence"],str(b["Yield"]),b["SampleName"]]
					k=lst[0]
					v=lst[1]+"\t"+lst[2]
					dic[k] = v
                #print (b["Yield"])
			for d in data["UnknownBarcodes"]:
				for k,v in d["Barcodes"].items():
					if not re.search(r'N+',k):
						#ou.write("\t".join([k,str(v)])+"\n")
						dic[k] = str(v) + "\t" + "-"
		for ky,val in sorted(dic.items(), key=lambda d:d[0]):
			ou.write('\t'.join([ky,str(val)])+"\n")
		ou.close()
	f.close()

###write to excel ####
# add time:  2017.7.24
import pandas as pd
lanes = glob.glob("L00*txt")
lanes = sorted(lanes)
out_name = sys.argv[2] + ".xls" # Flow cell id

writer = pd.ExcelWriter(out_name)
for lane in lanes:
	sheet_name = lane.split(".")[0]
	df = pd.read_csv(lane,sep="\t")
	df.columns=["Index","Base(bp)","Sample name"] 
	df.to_excel(writer,sheet_name,index=None)
writer.save()

