#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import gzip
if len(sys.argv) < 3:
    print "python",sys.argv[0],"<fq1> <fq2>"
    exit(1)
fq1 = sys.argv[1]
fq2 = sys.argv[2]
PE_reads = 0
ref_size = 6000000
base = 0
f1 = gzip.open(fq1)
for n,line in enumerate(f1):
    if (n+1) % 4 == 2:
        line = line.strip()
        PE_reads+= 1
        base += len(line)
f1.close()
f2 = gzip.open(fq2)
for n,line in enumerate(f2):
    if (n-4) % 4 == 1:
        line = line.strip()
        base += len(line)
f2.close()
cov_ref= base / (ref_size * 0.99)
print "The reference genome is:%s" % str(ref_size)
print  "There are %s PE reads" % PE_reads
print "The reference coverage is:%.2f" % cov_ref
