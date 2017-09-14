#!/usr/bin/python
#encoding:utf8
import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        # YOUR CODE HERE
        for tag in element.iter("tag"):
            print tag.attrib['k']
            if lower.search(tag.attrib['k']):
                keys["lower"] += 1
            elif lower_colon.search(tag.attrib['k']):
                keys["lower_colon"] += 1
            elif problemchars.search(tag.attrib['k']):
                keys["problemchars"] += 1
            else:
                keys["other"] += 1

    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


def test():

    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()