#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2021/11/09 09:51
# @Author : chen cheng
# @FileName: spider_genecards.py
# @Email : cheng.chen@geneseeq.com
# @Software: Notepad++

import os
import sys
import re
import time
import urllib
from bs4 import BeautifulSoup



def get_pos_seqid(url):
    """
    从genecards网站爬取基因的染色体位置信息及序列编号：
    例如：
    gene;GRCh37/hg19 by Entrez Gene;GRCh37/hg19 by Ensembl;RefSeq DNA sequence
    TP53;chr17:7,571,739-7,590,808;chr17:7,565,097-7,590,856;NC_000017.11
    """
    user_agent = 'Mozilla/6.0'
    headers={'User-Agent':user_agent}
    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    dls = soup.find_all('dl')
    pos_entrez = '-'
    pos_ensembl = '-'
    seqid = '-'
    
    # 染色体位置信息
    dls = soup.find_all('dl')
    for dl in dls:
        dl_text = dl.text
        #print(dl_text)
        if 'chr' in dl_text:
            #print(dl_text)
            pos = re.findall('chr.*\d{1}', dl_text)
            genome = re.findall('\(GRCh37.*\)', dl_text)
            if genome:
                if 'Entrez' in genome[0]:
                    pos_entrez = pos[0]
                if 'Ensembl' in genome[0]:
                    pos_ensembl = pos[0]
    
    # 基因序列号
    links = soup.find_all(attrs={'class':'gc-subsection'})
    for link in links:
        link_text = link.text
        if 'NC_' in link_text or 'NT_' in link_text:
            ref = re.findall('Ref.*Gene',link_text)
            seqid =  re.findall('N._.*\d+',link_text)
    
    return pos_entrez, pos_ensembl, seqid


def main():
    if len(sys.argv) < 2:
        print('python', sys.argv[0], '<gene.list>')
        sys.exit(1)
    
    
    gene_list = sys.argv[1]
    f = open(gene_list, 'r')
    
    general_url = 'https://www.genecards.org/cgi-bin/carddisp.pl?gene='
    
    header = 'Gene\tGRCh37/hg19 by Entrez Gene\tGRCh37/hg19 by Ensembl\tRefSeq DNA sequence\n'
    print(header)
    o = open('gene_card.tsv', 'w')
    o.write(header)
    for i in f:
        geneid = i.strip().split(',')[0]
        gene_url = general_url + geneid
        #print(geneid, gene_url)
        pos_entrez, pos_ensembl, seqid = get_pos_seqid(gene_url)
        seqid = ';'.join(seqid)
        res = '\t'.join([geneid, pos_entrez, pos_ensembl, seqid])
        print(res)
        # print(geneid, pos_entrez, pos_ensembl, seqid)]
        o.write(res + '\n')
        time.sleep(1.5)
    
    f.close()
    o.close()
    
    
if __name__ == '__main__':
    main()




   