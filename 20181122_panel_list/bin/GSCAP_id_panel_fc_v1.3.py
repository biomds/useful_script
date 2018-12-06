#!/usr/bin/python
# *-* coding:utf-8 *-*
__date__ = '2018.11.22'
__author__ = 'cheng.chen@geneseeq.com'
import os
import sys
import glob
import shutil
from argparse import ArgumentParser
panel_dic = {"RT":"P474H4K.cfg","416":"P416H4K.cfg","422":"P422H4K.cfg","425":"P425H4K.cfg","14gene":"14gene.cfg","RNA":"LeuH4K.cfg","leu2017":"LeuH4K.cfg","Lu":"LungH4K.cfg"}

### help part ###
parser = ArgumentParser(description='''This script is used to:
	(1)generate the clinical sample(s) ID,panel,FC file,
	(2)and is appropriate for hiseq X and hiseq 4000 platform''')
parser.add_argument('-f', '--run_fold', help='Run folder name of samplesheet')
parser.add_argument('-i', '--id_pair', help='Name of id.pair')
parser.add_argument('-a', '--ana_fold', help='Analysis data folder', default='/GPFS05/GSPipeline5')
parser.add_argument('-p', '--panel', help="Panel [{}]. default=None".format(
	" ".join([x for x in set(panel_dic.values())])), default=None)
args = parser.parse_args()
if len(sys.argv) < 3:
	os.system("python %s -h" % sys.argv[0])
	exit(1)
FC = args.run_fold
pair = args.id_pair
ana_fold = args.ana_fold
### work to do ###
dic_list = {}
dic_pair = {}
out = open("id.list.all",'w')
def list_treat(ana_fold,FC):
	## id_list check##
	id_lists = glob.glob("id_list_*")
	if len(id_lists ) >=1:
		## make folder ##
		if 'id_list_leu2017' in id_lists:
			leu2017_dir =  "%s/20%s_leukemia" %(ana_fold,FC)
			if not os.path.exists(leu2017_dir):
				os.makedirs("%s/raw" % leu2017_dir) ## make leukemia analysis folder
				#os.system("cp id_list_leu2017 %s/id.list" % leu2017_dir) ## copy 'id_list_leu2017' to leukemia analysis folder and rename it as id.list
				os.system("echo %s >%s/kit.txt" % (FC,leu2017_dir))
		# make new pipeline folder
		ana_dir = "%s/20%s" %(ana_fold,FC)
		if not os.path.exists(ana_dir):
			os.makedirs("%s/raw" % (ana_dir))
			os.system("echo %s >%s/kit.txt" % (FC,ana_dir))
		for each in id_lists:
			if each != 'id_list_leu2017':
				os.system("cp %s %s" % (each,ana_dir))
	else:
		print("\033[1;33m"+"No id_list!"+"\033[0m")
		exit(1)
	## id_list  ##
	for each in id_lists:
		i = each.split("_")[-1]
		lst = dic_list.setdefault(i,[])
		f = open(each,'r')
		for sample in f:
			sample = sample.strip()
			lst.append(sample)
		f.close()
	for k1,v1 in dic_list.items():
		for one in v1:
			line_out = ",".join([one,panel_dic[k1],FC])
			#print (line_out)
			out.write(line_out+"\n")

# id_pair treat ##
def pair_treat(id_pair):
	pair = open(id_pair,'r')
	id_cp = open("id.cp.all", "w")
	new_pair = "id.pair.all"
	op = open(new_pair,'w')
	for i in pair:
		i = i.strip().split("\t") #i[0] is B sample,i[1] is tumor sample,i[2] is patient name,i[3] is panel
		if len(i) < 4:
			pass
		if i[3] == 'lu':
			i[3] = 'Lu'
		if i[3] == 'Leu2017':
			i[3] = 'leu2017'
		lst = dic_pair.setdefault(i[3],[])
		lst.append(i[0])
		lst.append(i[1])
		op.write(i[0]+","+i[1]+","+i[3]+"\n")
	for k2,v2 in dic_pair.items():
		set_pair = set(v2)
		for k1,v1 in dic_list.items():
			set_list = set(v1)
			if k1 == k2:
				pair_uniq = set_pair - set_list
				for i in pair_uniq:
					#print ",".join([i,panel_dic[k1],"-"])
					line_out = ",".join([i,panel_dic[k1],"-"])
					out.write(line_out+"\n")
					id_cp.write(i+","+panel_dic[k1]+"\n")
	pair.close()
	id_cp.close()
	op.close()

def cp_pair_treat(id_cp,new_pair,ana_fold,FC):
	leu2017_dir = "%s/20%s_leukemia" % (ana_fold, FC)
	ana_dir = "%s/20%s" % (ana_fold, FC)
	### id.cp.all treat ###
	cp = open(id_cp,'r')

	leu_cp = []
	new_cp = []
	for i in cp:
		i = i.strip().split(',')
		if i[1] == 'LeuH4K.cfg':
			leu_cp.append(i[0])
		else:
			new_cp.append(i[0])
	if os.path.exists(leu2017_dir):
		leu_op = open("%s/id.cp" % leu2017_dir,'w')
		for each in leu_cp:
			leu_op.write(each+"\n")
		leu_op.close()
	if os.path.exists(ana_dir):
		new_cp_o = open("%s/id.cp" % ana_dir,'w')
		for each in new_cp:
			new_cp_o.write(each+"\n")
		new_cp_o.close()
	### id.pair.all treat ###
	pair = open(new_pair, 'r')
	if os.path.exists(leu2017_dir):
		leu_pair = open("%s/id.pair" % leu2017_dir, 'w')
	if os.path.exists(ana_dir):
		new_pair_o = open("%s/id.pair" % ana_dir, 'w')
	for j in pair:
		check,tumor,panel = j.strip().split(",")
		if panel == 'leu2017' or panel == 'Leu2017':
			leu_pair.write(check+"\t"+tumor+"\n")
		else:
			new_pair_o.write(check+"\t"+tumor+"\n")
	#leu_pair.close()
	#new_pair_o.close()
def id_list_all_treat(ana_fold,FC,id_list_all):
	leu2017_dir = "%s/20%s_leukemia" % (ana_fold, FC)
	ana_dir = "%s/20%s" % (ana_fold, FC)
	### id.list.all treat ###
	if os.path.exists(leu2017_dir):
		os.system("cat %s |grep LeuH4K.cfg |grep %s |cut -f 1 -d , >%s/id.list " % (id_list_all,FC,leu2017_dir))
		os.system("ln -s %s /GPFS01/GSPipeline" % leu2017_dir) # link dir
	if os.path.exists(ana_dir):
		os.system("cat %s |grep LeuH4K.cfg -v >%s/id.list" % (id_list_all, ana_dir))
		os.system("ln -s %s /GPFS01/GSPipeline" % ana_dir) # link dir

list_treat(ana_fold,FC)
pair_treat(pair)
id_cp = "id.cp.all"
new_pair = "id.pair.all"
id_list_all = "id.list.all"
cp_pair_treat(id_cp,new_pair,ana_fold,FC)
out.close()
id_list_all_treat(ana_fold,FC,id_list_all)
