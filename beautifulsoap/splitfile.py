#!/usr/bin/python
#encoding:utf8

import xml.etree.ElementTree as ET

PATENTS = 'patent.data'


def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    """
    Split the input file into separate files, each containing a single patent.
    As a hint - each patent declaration starts with the same line that was
    causing the error found in the previous exercises.
    The new files should be saved with filename in the following format:
    "{}-{}".format(filename, n) where n is a counter, starting from 0.
    """
    xmlnum = []
    end_pos = 0
    start_pos = 0
    current_pos = 0
    file = open(filename, 'r')
    for number, content in enumerate(file):
        if content.startswith("<?xml"):
            xmlnum.append(number)

    for i in range(len(xmlnum)):
        splitfile = "{}-{}".format(PATENTS, i)
        start_pos = end_pos
        current_pos = end_pos
        newfile = open(splitfile, 'w+')
        print i+1
        with open(PATENTS, 'r') as f:
            for line in f:
                if (i + 1) == len(xmlnum):
                    current_pos += 1
                    if current_pos >= start_pos and current_pos <= len(open(PATENTS, 'r') .readlines()):
                        newfile.writelines(line)
                else:
                    current_pos += 1
                    end_pos = xmlnum[i + 1]
                    if current_pos >= start_pos and current_pos <= end_pos:
                        newfile.writelines(line)


def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()