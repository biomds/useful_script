#!/usr/bin/python3 
__date__ = '20180917'
__author__ = 'hengbenxianfeng@163.com'

import sys
import os
from argparse import ArgumentParser
parser = ArgumentParser(description='''This script is used to:
(1)generate the clinical data analysis command line,
(2)make the analysis directory with writing 'id.list' in the analysis directory,
(3)and is appropriate for hiseq X and hiseq 4000 platform''')
parser.add_argument('-t','--sheet',help = 'SampleSheet of clinical data')
parser.add_argument('-f','--run_fold',help = 'Run folder name of samplesheet')
parser.add_argument('-a','--ana_fold',help = 'Analysis data folder',default='/GPFS02/GSPipeline2')
args = parser.parse_args()
if len(sys.argv) < 4:
	os.system("python %s -h" % sys.argv[0])
	exit(1)
samplesheet = args.sheet
run_fold = args.run_fold
analysis_fold = args.ana_fold

tmp = os.popen("cat %s |grep '^[1-8],'| cut -f 3 -d ,|sort -u " % samplesheet).readlines()
lst = ''.join(list(tmp)).split("\n")[:-1]
panel_sample = []
list_RT,list_416,list_422,list_425,list_14gene,list_RNA,list_YH105,list_Lu = [],[],[],[],[],[],[],[]
for i in lst:
	if i.endswith("RT"):
		list_RT.append(i)
	elif i.endswith("416"):
		list_416.append(i)
	elif i.endswith("422"):
		list_422.append(i)
	elif i.endswith("14gene"):
		list_14gene.append(i)
	elif 'RNA' in i:
		list_RNA.append(i)
	elif 'YH105' in i and 'WES' not in i:
		list_YH105.append(i)
	elif 'Lu' in i and 'WES' not in i:
		list_Lu.append(i)
	else:
		if not 'WES' in i and not 'CR' in i:
			list_425.append(i)

###### generate analysis cmd and write out id.list########
##subfunction
##(1)make directory and write id.list in it	
def write_id_list(list_sample,ana_type):
	ana_path = "%s/20%s%s" % (analysis_fold,run_fold,ana_type)
	if not os.path.exists(ana_path):
		os.mkdir(ana_path)
#	else:
#		print("You have made a directory: %s" % ana_path)
	f = open("%s/id.list" % ana_path,'w')
	for i in list_sample:
		f.write(i+"\n")
	f.close()
##(2)print analysis command line
def print_cmd(panel,analysis_fold,run_fold,ana_type,log):
	if 'K00' in run_fold:
		print ("nohup Autorun_GSCAP_new_0823-2.0.py -p %s %s/20%s%s > %s 2>&1 & " % (panel,analysis_fold,run_fold,ana_type,log))
	if 'E00' in run_fold:
		print ("nohup Autorun_GSCAP_new_0823-2.0.py -p %s.X %s/20%s%s > %s 2>&1 & " % (panel,analysis_fold,run_fold,ana_type,log))
if len(list_RT) >= 1:
	panel_sample.append(list_RT[0])
	write_id_list(list_RT,"_RT")
	print_cmd("201801-425-plutRT",analysis_fold,run_fold,"_RT","RT.log")
if len(list_416) >= 1:
	panel_sample.append(list_416[0])
	write_id_list(list_416,"_416")
	print_cmd("201601",analysis_fold,run_fold,"_416","416.log")
if len(list_422) >= 1:
	panel_sample.append(list_422[0])
	write_id_list(list_422,"_422")
	print_cmd("201702",analysis_fold,run_fold,"_422","422.log")
if len(list_425) >= 1:
	panel_sample.append(list_425[0])
	write_id_list(list_425,"")
	print_cmd("201801-425",analysis_fold,run_fold,"","425.log")
if len(list_RNA) >= 1:
	panel_sample.append(list_RNA[0])
	write_id_list(list_RNA,"_RNA")
	print_cmd("leukemia2017",analysis_fold,run_fold,"_RNA","RNA.log")
if len(list_14gene) >= 1:
	panel_sample.append(list_14gene[0])
	write_id_list(list_14gene,"_14gene")
	print_cmd("14Gene",analysis_fold,run_fold,"_14gene","14gene.log")
if len(list_YH105) >= 1:
	panel_sample.append(list_YH105[0])
	write_id_list(list_YH105,"_leukemia")
	print_cmd("leukemia2017",analysis_fold,run_fold,"_leukemia","leukemia.log")
if len(list_Lu) >= 1:
	panel_sample.append(list_Lu[0])
	write_id_list(list_Lu,"_Lu")
	print_cmd("LungFullFinal",analysis_fold,run_fold,"_Lu","Lu.log")
#for i in panel_sample:
#	print (i)
#print ('\n'.join(list(panel_sample)))










