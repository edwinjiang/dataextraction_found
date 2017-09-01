#!/usr/bin/python
#encoding:utf8

import xlrd

datafile =''

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    # data = [[sheet.cell_value(r,col)
    #          for col in range(sheet.ncols)]
    #             for r in range(sheet.nrows)]
    # print "\nList Data"
    # print data[3][2]
    #
    # for row in range(sheet.nrows):
    #     for col in range(sheet.ncols):
    #         if row == 50:
    #             print sheet.cell_value(row,col)
    # print sheet.nrows
    # print sheet.cell_type(3,2)
    # print sheet.cell_value(3,2)
    # print sheet.cell_value(3, start_rowx=1,end_rowx=4)
    #
    # print xlrd.xldate_as_tuple(sheet.cell_value(1,0))

    cv = sheet.col_values(1,start_rowx=1,end_rowx=None)

    maxval = max(cv)
    minval = min(cv)

    maxpos = cv.index(maxval)+1
    minpos = cv.index(minval)+1

    maxtime = sheet.cell_value(maxpos,0)
    realmaxtime = xlrd.xldate_as_tuple(maxtime,0)

    mintime = sheet.cell_value(minpos,0)
    realmintime = xlrd.xldate_as_tuple(mintime,0)

    data = {
        'maxtime': realmaxtime,
        'maxvalue': maxval,
        'mintime': realmintime,
        'minvalue': minval,
        'avgcoast': sum(cv)/ float(len(cv))
    }


    return data

def test():

    data = parse_file(datafile)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)

test()