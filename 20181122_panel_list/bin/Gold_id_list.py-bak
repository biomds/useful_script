#!/usr/bin/python
# *-* coding:utf-8 *-*
__date__ = '2018.11.22'
__author__ = 'cheng.chen@geneseeq.com'
import os
import sys
from argparse import ArgumentParser
### samplesheet split
def sample_sheet_treat(samplesheet):
	tmp = os.popen("cat %s |grep '^[1-8],'| cut -f 3 -d ,|sort -u " % samplesheet).readlines()
	lst = ''.join(list(tmp)).split("\n")[:-1]
	log = open("Sample.log",'w')
	sample_all = len(lst)
	print "\033[1;33m"+"Total sample(s) number:" + str(sample_all) +"\033[0m"
	log.write("Total sample(s) number:" + str(sample_all)+"\n")
	list_RT,list_416,list_422,list_425,list_14gene,list_RNA,list_YH105,list_Lu = [],[],[],[],[],[],[],[]
	other = []
	for i in lst:
		if "RT" in i:
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
		elif 'WGS' in i or 'WES' in i:
			other.append(i)
		else:
			if  not 'WES' in i and not 'WGS' in i:
				list_425.append(i)
	print "Other sample(s):" + str(len(other))
	log.write("Other sample(s):" + str(len(other))+"\n")
	for each in other:
		print each
		log.write(each+"\n")
	print "\033[1;33m"+"Sample(s) need to be analysed:" + str(sample_all - len(other)) +"\033[0m"
	log.write("Sample(s) need to be analysed:" + str(sample_all - len(other)) +"\n")
	def write_list(lst,name):
		if len(lst) >= 1:
			sample_num = 0
			lst_name = "id_" + str(name)
			f = open(lst_name, "w")
			for i in lst:
				sample_num += 1
				f.write(i+"\n")
			f.close()
			print lst_name+":" + str(sample_num)
			log.write(lst_name+":" + str(sample_num) + "\n")
	write_list(list_RT,"list_RT")
	write_list(list_416,"list_416")
	write_list(list_422,"list_422")
	write_list(list_425,"list_425")
	write_list(list_14gene,"list_14gene")
	write_list(list_RNA,"list_RNA")
	write_list(list_YH105,"list_leu2017")
	write_list(list_Lu,"list_Lu")
	### cmd line ###
	pwd = os.getcwd()
	FC = os.path.basename(pwd)
	ana_fold_leu = "/GPFS05/GSPipeline5/20{}_leukemia".format(FC)
	ana_fold_new = "/GPFS05/GSPipeline5/20{}".format(FC)
	print "\033[1;33m"+ "The command line is:"+"\033[0m"
	log.write("The command line is:"+"\n")
	if len(list_YH105) > 1:
		if 'E00' in FC:
			print "nohup Autorun_GSCAP_new_0823-2.0.py -p leukemia2017.X {} > leukemia.log 2>&1 &".format(ana_fold_leu)
			log.write("nohup Autorun_GSCAP_new_0823-2.0.py -p leukemia2017.X {} > leukemia.log 2>&1 &".format(ana_fold_leu)+"\n")
		if 'K00' in FC:
			print "nohup Autorun_GSCAP_new_0823-2.0.py -p leukemia2017 {} > leukemia.log 2>&1 &".format(ana_fold_leu)
			log.write("nohup Autorun_GSCAP_new_0823-2.0.py -p leukemia2017 {} > leukemia.log 2>&1 &".format(ana_fold_leu)+"\n")
	print "nohup /GPFS01/home/njsh/scripts/Lvws/GSCAP_new_Pipline/Auto_RunGSCAP.py -f {} -i id.list -p id.pair > Gold.log 2>&1 & " .format(ana_fold_new)
	log.write( "nohup /GPFS01/home/njsh/scripts/Lvws/GSCAP_new_Pipline/Auto_RunGSCAP.py -f {} -i id.list -p id.pair > Gold.log 2>&1 & " .format(ana_fold_new)+"\n")
if __name__ == "__main__":
	parser = ArgumentParser(description='''This script is used to generate the clinical sample(s) ID.
\nlist(s) can be generated up to 8,including [list_RT,list_416,list_422,list_425,list_14gene,list_RNA,list_leu2017,list_Lu]''')
	parser.add_argument('-t', '--sheet', help='SampleSheet of clinical data')
	args = parser.parse_args()
	if len(sys.argv) < 2:
		os.system("python %s -h" % sys.argv[0])
		exit(1)
	samplesheet = args.sheet
	sample_sheet_treat(samplesheet)




