#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import os
import sys
if len(sys.argv) < 2:
	print "python",sys.argv[0],"ln.sh"
	exit(1)

sample_x = []
sample_4k = []
f = open("ln.sh","r")
for line in f:
	line = line.strip()
	if re.search(r'^$',line): #匹配到空行就pass,r表示关闭转义字符的特殊含义
		pass
	elif line.startswith("=|#"):
		pass
	elif re.search(r'bai',line):
		pass
	else:
		def get_name(lin): ##定义子函数，得到样本名称
			lin = lin.split()[-2] #分割后得到倒数第二列
			lin = os.path.basename(lin) #得到倒数第二列的文件名称
			lin = lin.split(".")[0] #得到样本名称
			return lin #返回样本名称
		if re.search(r'E00',line): #匹配hiseq X平台对应样本
			sample_x.append(get_name(line)) #将样本名称append到sample_x的列表中
		if re.search(r'K00',line): #匹配hiseq 4000平台对应样本
			sample_4k.append(get_name(line)) #将样本名称append到sample_4k的列表中
sample_x = set(sample_x) #去重
sample_4k = set(sample_4k) #去重
## print out
## hiseq X
with open("id.tmd-x10",'w') as f1:
	for i in sample_x:
		f1.write(i+"\n")
f1.close()
## hiseq 4000
with open("id.tmd-4k",'w') as f2:
	for i in sample_4k:
		f2.write(i+"\n")
f2.close()

