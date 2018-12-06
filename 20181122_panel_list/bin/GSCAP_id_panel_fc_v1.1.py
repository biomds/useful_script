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

dic_list = {}
dic_pair = {}
out = open("id.list",'w')
def list_treat(ana_fold,FC):
	## id_list check##
	id_lists = glob.glob("id_list_*")
	if len(id_lists ) >=1:
		if 'id_list_leu2017' in id_lists:
			leu2017_dir =  "%s/20%s_leukemia" %(ana_fold,FC)
			if not os.path.exists(leu2017_dir):
				os.makedirs("%s/raw" % leu2017_dir)
				shutil.copyfile('id_list_leu2017',"%s/id.list" %leu2017_dir)
			id_lists.remove('id_list_leu2017')
		ana_dir = "%s/20%s" %(ana_fold,FC)
		if not os.path.exists(ana_dir):
			os.makedirs("%s/raw" % (ana_dir))
		for each in id_lists:
			os.system("cp %s %s" % (each,ana_dir))
	else:
		print("\033[1;33m"+"No id_list!"+"\033[0m")
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
			#out.write(line_out)


# id_pair treat ##
def pair_treat(id_pair):
	pair = open(id_pair,'r')
	id_cp = open("id.cp", "w")
	new_pair = "id.pair"
	op = open(new_pair,'w')
	for i in pair:
		i = i.strip().split("\t") #i[0] is B sample,i[1] is tumor sample,i[2] is patient name,i[3] is panel
		if i[3] == 'lu':
			i[3] = 'Lu'
		lst = dic_pair.setdefault(i[3],[])
		lst.append(i[0])
		lst.append(i[1])
		op.write(i[0]+"\t"+i[1]+"\n")
	for k2,v2 in dic_pair.items():
		set_pair = set(v2)
		for k1,v1 in dic_list.items():
			set_list = set(v1)
			if k1 == k2:
				pair_uniq = set_pair - set_list
				for i in pair_uniq:
					#print ",".join([i,panel_dic[k1],"-"])
					line_out = ",".join([i,panel_dic[k1],"-"])
					#out.write(line_out)
					id_cp.write(i+"\n")
	id_cp.close()
out.close()
if __name__ == '__main__':
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
	list_treat(ana_fold,FC)
	pair_treat(pair)
#	shutil.copyfile("id.list","%s/20%s" %(ana_fold,FC)
#	shutil.copyfile("id.cp", "%s/20%s" % (ana_fold, FC))
#	shutil.copyfile()
