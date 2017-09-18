#!/usr/bin/python
#encoding:utf8

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import sys

OSMFILE = "shanghai_sample_k50.osm"
CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def process_chinese_name(element):
    node = {}
    temp = {}
    if element.tag == "node" or element.tag == "way":
        for item in element.iter("node"):
            for userid in item.attrib["user"]:
                if u'\u4e00' <= userid <= u'\u9fff':
                    node["id"] = item.attrib["id"]
                    node["type"] = item.tag
                    for i in range(len(CREATED)):
                        temp[CREATED[i]] = item.attrib[CREATED[i]]
                    node["created"] = temp
                    node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]
                else:
                    node["id"] = item.attrib["id"]
                    node["type"] = item.tag
                    for i in range(len(CREATED)):
                        temp[CREATED[i]] = item.attrib[CREATED[i]]
                    node["created"] = temp
                    node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]
        return node
    else:
        return  None



def process_map(osm_file,pretty=False):
    file_out = "{0}.json".format("include_chinese_name_data")
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(osm_file):
            el = process_chinese_name(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def parsedata():
    data = process_map(OSMFILE, True)
    pprint.pprint(data)


if __name__ == "__main__":
    parsedata()