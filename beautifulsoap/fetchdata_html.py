#!/usr/bin/python
#encoding:utf8

from bs4 import BeautifulSoup
import os
import requests
import re

DATADIR = ""
DATAFILE = "awrrpt_10.110.82.232_rac_718_719_201709071003.html"

def extract_data(file):
    data = []
    total = 0
    with open(file) as f:
        soup = BeautifulSoup(f,'lxml')
        pattern = re.compile(r'^physical')
        pattern1 = re.compile(r'total IO requests')
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
                total += data[i]["per trans"]
        print float(total)


def fetch():
    awrfile = os.path.join(DATADIR, DATAFILE)
    extract_data(awrfile)

if __name__ == "__main__":
    fetch()