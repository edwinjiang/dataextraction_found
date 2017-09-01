#!/usr/bin/python
#encoding:utf8

import os
import csv

dataset_path = './dataset'
csv_file_name = './beatles-diskography.csv'

def parse_file(datafile):
    data = []

    with open(datafile) as f:
        rawdata = csv.DictReader(f)
        for line in rawdata:
            data.append(line)
    print data
    return data

def test():
    datafile = os.path.join(dataset_path, csv_file_name)
    d = parse_file(datafile)

    # firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    #
    # tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}
    #
    # assert d[0] == firstline
    # assert d[9] == tenthline

test()