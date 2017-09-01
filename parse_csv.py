#!/usr/bin/python
#encoding:utf8

import os
import pandas as pd

dataset_path = './dataset'
csv_file_name = './beatles-diskography.csv'
number = 10

def parse_file(datafile):
    data = []
    raw_data = pd.read_csv(datafile, nrows=number).fillna(value='').to_dict(orient='dict')
    for i in range (number):
        data.append({'Title':raw_data['Title'][i],'UK Chart Position':raw_data['UK Chart Position'][i],'Label':raw_data ['Label'][i],'Released':raw_data ['Released'][i],'US Chart Position':raw_data['US Chart Position'][i],'RIAA Certification':raw_data['RIAA Certification'][i],'BPI Certification':raw_data['BPI Certification'][i]})
    return data

def test():
    datafile = os.path.join(dataset_path, csv_file_name)
    d = parse_file(datafile)

    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}

    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline

test()
