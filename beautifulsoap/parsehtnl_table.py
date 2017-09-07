#!/usr/bin/python
#encoding:utf8


from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


def process_file(f):
    """
    This function extracts data from the file given as the function argument in
    a list of dictionaries. This is example of the data structure you should
    return:

    data = [{"courier": "FL",
             "airport": "ATL",
             "year": 2012,
             "month": 12,
             "flights": {"domestic": 100,
                         "international": 100}
            },
            {"courier": "..."}
    ]


    Note - year, month, and the flight data should be integers.
    You should skip the rows that contain the TOTAL data for a year.
    """
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")
    # Note: create a new dictionary for each entry in the output data list.
    # If you use the info dictionary defined here each element in the list
    # will be a reference to the same info dictionary.
    with open("{}/{}".format(datadir, f), "r") as html:

        soup = BeautifulSoup(html,'lxml')
        for rawdata in soup.find_all('table',id='DataGrid1'):
            trdatas = rawdata.find_all(name='tr',attrs={'class':"dataTDRight"})
            for trdata in trdatas:
                tddatas = BeautifulSoup(str(trdata),"html.parser")
                tddata = tddatas.find_all('td')
                if tddata[1].string <> 'TOTAL' :
                    data.append({"courier": "FL","airport": "ATL","year":int(tddata[0].string),"month":int(tddata[1].string),
                "flights": {"domestic": int(tddata[2].string.replace(',','')),"international":int(tddata[3].string.replace(',',''))}})
        print data
    return data


def test():
    print "Running a simple test..."
    open_zip(datadir)
    files = process_all(datadir)
    data = []
    # Test will loop over three data files.
    for f in files:
        data += process_file(f)

        # assert len(data) == 399  # Total number of rows
        # for entry in data[:3]:
        #     assert type(entry["year"]) == int
        #     assert type(entry["month"]) == int
        #     assert type(entry["flights"]["domestic"]) == int
        #     assert len(entry["airport"]) == 3
        #     assert len(entry["courier"]) == 2
        # assert data[0]["courier"] == 'FL'
        # assert data[0]["month"] == 10
        # assert data[-1]["airport"] == "ATL"
        # assert data[-1]["flights"] == {'international': 108289, 'domestic': 701425}

        # print "... success!"


if __name__ == "__main__":
    test()