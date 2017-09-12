#!/usr/bin/python
#encoding:utf8

from bs4 import BeautifulSoup
import os
import requests
import re
import argparse

DATADIR = ""
DATAFILE = "awrrpt_10.110.82.232_rac_722_723_201709071114.html"

def extract_data(**kwargs):
    data = []
    total = 0
    awrfile = os.path.join(DATADIR, kwargs["file"])
    print kwargs["metric"]
    with open(awrfile) as f:
        soup = BeautifulSoup(f,'lxml')
        pattern = re.compile(r'physical')
        pattern1 = re.compile(kwargs["metric"])
        #pattern1 = re.compile(r'total IO requests$')
        for rawdata in soup.find_all('table'):
            trdatas =  rawdata.find_all(name='tr')
            for trdata in trdatas:
                tddatas = BeautifulSoup(str(trdata), "html.parser")
                tddata = tddatas.find_all(name='td')
                try:
                    if  (pattern.match(tddata[0].string)):
                        data.append({'name':tddata[0].string,'total':float(tddata[1].string.replace(',','')),'per second':float(tddata[2].string.replace(',','')),'per trans':float(tddata[3].string.replace(',',''))})
                except:
                    pass
        print data
        for i in range(len(data)):
            if pattern1.search(data[i]["name"]):
                print data[i]["name"]
                total += data[i]["per second"]
        print float(total)

def _argparser():
    parser = argparse.ArgumentParser(description='AWR Data Analyze')
    parser.add_argument('-f','--file', action='store', dest='file', required=True, help='AWR File Name')
    parser.add_argument('-m','--metric', action='store', dest='metric', required=True, help='Metric Name')
    return parser.parse_args()

if __name__ == "__main__":
    parser = _argparser()
    conn_args = dict(file=parser.file, metric=parser.metric)
    extract_data(**conn_args)