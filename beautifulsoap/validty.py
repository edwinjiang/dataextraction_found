#!/usr/bin/python
#encoding:utf8

import csv
import pprint

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

#skip n lines of CSV files 
# def skip_lines(input_file,skip):
#     for i in range(0,skip):
#         next(input_file)


def process_file(input_file, output_good, output_bad):
    data_good = []
    data_bad = []
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for listdata in reader:
            if listdata['URI'].find('dbpedia.org') > 0:
                valid_year = listdata['productionStartYear'][:4]
                try:
                    valid_year = int(valid_year)
                    if (valid_year >= 1886) and (valid_year <= 2014):
                        data_good.append(listdata)
                    else:
                        data_bad.append(listdata)
                except ValueError:
                    if valid_year == 'NULL':
                        data_bad.append(listdata)

    with open(OUTPUT_GOOD, "w") as good:
        writer = csv.DictWriter(good, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in data_good:
            writer.writerow(row)

    with open(OUTPUT_BAD, "w") as bad:
        writer = csv.DictWriter(bad, delimiter=",", fieldnames=header)
        writer.writeheader()
        for row in data_bad:
            writer.writerow(row)

def test():
    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)

if __name__ == "__main__":
    test()