#!/usr/bin/python
#encoding:utf8

from bs4 import BeautifulSoup
import os
import requests
import re
import argparse
from ConfigParser import SafeConfigParser
import json

DATADIR = ""
DATAFILE = "awrrpt_10.110.82.232_rac_722_723_201709071114.html"
# IO metrics
# physical reads io requests and physical read multiblock io requests and physical write IO requests and physical write multiblock IO request  redo writes    iops
# physical read total bytes ,  physical write total bytes, physical multiblock read total bytes, physical multibkock write total bytes, redo size   mbytes
# buffer cache ratio
# db file sequential read time and db file scattered read time
def extract_data(**kwargs):
    data = []
    result = {}
    total = 0
    awrfile = os.path.join(DATADIR, kwargs["file"])

    with open(awrfile) as f:
        soup = BeautifulSoup(f,'lxml')
        # parse metric configure file
        metric_parser = SafeConfigParser(allow_no_value=True)
        metric_parser.read('metric.conf')
        for section_name in metric_parser.sections():
            # print('Section:', section_name)
            # print('Options:', metric_parser.options(section_name))
            metric_item=[]
            for name, value in metric_parser.items(section_name):
                metric_item.append(value)
            pattern = re.compile(metric_item[1])
            #pattern1 = re.compile(kwargs["metric"])
            pattern1 = re.compile(metric_item[2])

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
            #print data
            for i in range(len(data)):
                if pattern1.search(data[i]["name"]):
                    #print data[i]["name"]
                    total += data[i]["per second"]
                    result[data[i]["name"]] = data[i]["per second"]
            result["Total"] = total
            #print type(result)
            json_dic1 = json.dumps(result)
            #print type(json_dic1)
            print json_dic1

def _argparser():
    parser = argparse.ArgumentParser(description='AWR Data Analyze')
    parser.add_argument('-f','--file', action='store', dest='file', required=True, help='AWR File Name')
    #parser.add_argument('-m','--metric', action='store', dest='metric', required=True, help='Metric Name')
    return parser.parse_args()

if __name__ == "__main__":
    parser = _argparser()
    #conn_args = dict(file=parser.file, metric=parser.metric)
    conn_args = dict(file=parser.file)
    extract_data(**conn_args)