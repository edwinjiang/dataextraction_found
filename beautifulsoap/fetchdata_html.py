#!/usr/bin/python
#encoding:utf8

from bs4 import BeautifulSoup
import os
import requests
import re
import boto


DATADIR = ""
DATAFILE = "awr_rac.html"

# doc = urllib.request.urlopen('http://www.bkzy.org/Index/Declaration?intPageNo=1')
# doc = doc.read().decode('utf-8')
#
# soup = BeautifulSoup(doc, "html.parser")

def extract_data(file):
    with open(file) as f:
        soup = BeautifulSoup(f,'lxml')

        #awrdata = soup.find(summary="System Statistics - Per Transaction")
        pattern = re.compile(r'^physical')
        #
        # for a in soup.find_all("tr",scope='row'):
        #     if pattern.match(a.text):
        #         print a.text
        for rawdata in soup.find_all('table',summary="System Statistics (Global). . per Second Average - average of per-instance per Second rates. per Second Std Dev - standard deviation of per-instance per Second rates. per Second Min - minimum of per-instance per Second rates. per Second Max - maximum of per-instance per Second rates"):
            for data in rawdata.find_all('td'):
                print data.text


def fetch():
    awrfile = os.path.join(DATADIR, DATAFILE)
    extract_data(awrfile)

if __name__ == "__main__":
    # conn = boto.connect_s3()
    # url = conn.generate_url(3600,'GET',bucket='edwintest-s3',key='vagrant and docker command')
    # print url
    fetch()