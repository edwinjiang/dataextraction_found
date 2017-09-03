#!/usr/bin/python
#encoding:utf

import csv
import os

DATADIR = ""
DATAFILE = "745090.csv"


def parse_file(datafile):
    name = ""
    data = []
    with open(datafile, 'rb') as f:

       rawdata = csv.reader(f)
       for i, rows in enumerate(rawdata):
           if i == 0:
               name = rows[1]
           if i > 1:
               data.append(rows)
    # Do not change the line below
    return (name, data)


def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    name, data = parse_file(datafile)

    assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
    assert data[0][1] == "01:00"
    assert data[2][0] == "01/01/2005"
    assert data[2][5] == "2"


if __name__ == "__main__":
    test()
    # 8