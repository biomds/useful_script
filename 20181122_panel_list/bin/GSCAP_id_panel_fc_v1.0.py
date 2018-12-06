#!/usr/bin/python
# *-* coding:utf-8 *-*
__date__ = '2018.11.22'
__author__ = 'cheng.chen@geneseeq.com'
import os
import sys
from argparse import ArgumentParser


panel_dic = {"RT":"P474H4K.cfg","416":"P416H4K.cfg","422":"P422H4K.cfg","425":"P425H4K.cfg","14gene":"14gene.cfg","RNA":"LeuH4K.cfg","YH105":"LeuH4K.cfg","Lu":"LungH4K.cfg"}

### samplesheet split

def sample_sheet_treat(samplesheet,run_fold):
	tmp = os.popen("cat %s |grep '^[1-8],'| cut -f 3 -d ,|sort -u " % samplesheet).readlines()
	lst = ''.join(list(tmp)).split("\n")[:-1]
	list_RT,list_416,list_422,list_425,list_14gene,list_RNA,list_YH105,list_Lu = [],[],[],[],[],[],[],[]
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
		else:
			if  not 'WES' in i and not 'WGS' in i:
				list_425.append(i)
	def write_list(lst,panel,run_fold,name):
		if len(lst) >= 1:
			lst_name = "id_" + str(name)
			f = open(lst_name, "w")
			for i in lst:
				f.write(i+"\t"+panel+"\t"+run_fold+"\n")
			f.close()
	# panel_list = [list_RT,list_416,list_422,list_425,list_14gene,list_RNA,list_YH105,list_Lu]
	write_list(list_RT,panel_dic["RT"],run_fold,"list_RT")
	write_list(list_416,panel_dic["416"],run_fold,"list_416")
	write_list(list_422,panel_dic["422"],run_fold,"list_422")
	write_list(list_425,panel_dic["425"],run_fold,"list_425")
	write_list(list_14gene,panel_dic["14gene"],run_fold,"list_14gene")
	write_list(list_RNA,panel_dic["RNA"],run_fold,"list_RNA")
	write_list(list_YH105,panel_dic["YH105"],run_fold,"list_YH105")
	write_list(list_Lu,panel_dic["Lu"],run_fold,"list_Lu")
if __name__ == "__main__":
	parser = ArgumentParser(description='''This script is used to:
	(1)generate the clinical sample(s) ID,panel,FC file,
	(2)and is appropriate for hiseq X and hiseq 4000 platform''')
	parser.add_argument('-t', '--sheet', help='SampleSheet of clinical data')
	parser.add_argument('-f', '--run_fold', help='Run folder name of samplesheet')
	parser.add_argument('-p', '--panel', help="Panel [{}]. default=None".format(
		" ".join([x.split("/")[-1] for x in set(panel_dic.values())])), default=None)
	args = parser.parse_args()
	if len(sys.argv) < 3:
		os.system("python %s -h" % sys.argv[0])
		exit(1)
	samplesheet = args.sheet
	run_fold = args.run_fold
	sample_sheet_treat(samplesheet,run_fold)




