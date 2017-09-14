#!/usr/bin/python
#encoding:utf8

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

"""
具体来说，你应该完成以下任务：

    你应该只处理两种类型的顶级标记：“节点”和“道路”
    “节点”和“道路”应该转换为常规键值对，以下情况除外：
        CREATED 数组中的属性应该添加到键“created”下
        经纬度属性应该添加到“pos”数组中，以用于地理空间索引编制。确保“pos”数组中的值是浮点型，不是字符串。
    如果二级标记“k”值包含存在问题的字符，则应忽略
    如果二级标记“k”值以“addr:”开头，则应添加到字典“address”中
    如果二级标记“k”值不是以“addr:”开头，但是包含“:”，你可以按照自己认为最合适的方式进行处理。例如，你可以将其拆分为二级字典，例如包含“addr:”，或者转换“:”以创建有效的键。
    如果有第二个用于区分街道类型/方向的“:”，则应该忽略该标记，例如：

"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def shape_element(element):
    node = {}
    temp = {}
    refs_temp = []
    temp_address = {}
    if element.tag == "node" or element.tag == "way":
        # YOUR CODE HERE
        for item in element.iter("node"):
            node["id"] = item.attrib["id"]
            node["type"] = item.tag

            if "visible" in item.attrib.keys():
                node["visible"] = item.attrib["visible"]

            for i in range(len(CREATED)):
                temp[CREATED[i]] = item.attrib[CREATED[i]]
            node["created"] = temp

            node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]

            for child in item:
                for address in child.iter("tag"):
                    if address.attrib['k'].startswith("addr:") and address.attrib['k'].count(":") == 1:
                        temp_address[address.attrib['k'].split(":")[1]] = address.attrib['v']
                    if address.attrib['k'] == "amenity":
                        node["amenity"] = address.attrib['v']
                    if address.attrib['k'] == "cuisine":
                        node["cuisine"] = address.attrib['v']
                    if address.attrib['k'] == "phone":
                        node["phone"] = address.attrib['v']
                    if address.attrib['k'] == "name":
                        node["name"] = address.attrib['v']

                node["address"] = temp_address

        for item in element.iter("way"):
            node["id"] = item.attrib["id"]
            node["type"] = item.tag
            # if item.hasAttribute["visible"] != None:
            #     node ["visible"] = item.attrib["visible"]
            for i in range(len(CREATED)):
                temp[CREATED[i]] = item.attrib[CREATED[i]]
            node["created"] = temp

            for child in item:
                for refer in child.iter("nd"):
                    refs_temp.append(refer.attrib["ref"])
            node["node_refs"] = refs_temp

            for child in item:
                for address in child.iter("tag"):
                    if address.attrib['k'].startswith("addr:") and address.attrib['k'].count(":") == 1:
                        temp_address[address.attrib['k'].split(":")[1]] = address.attrib['v']
                    if address.attrib['k'] == "amenity":
                        node["amenity"] = address.attrib['v']
                    if address.attrib['k'] == "cuisine":
                        node["cuisine"] = address.attrib['v']
                    if address.attrib['k'] == "phone":
                        node["phone"] = address.attrib['v']
                    if address.attrib['k'] == "name":
                        node["name"] = address.attrib['v']

                node["address"] = temp_address

        return node
    else:
        return None


def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('example.osm', True)
    pprint.pprint(data)

    correct_first_elem = {
        "id": "261114295",
        "visible": "true",
        "type": "node",
        "pos": [41.9730791, -87.6866303],
        "created": {
            "changeset": "11129782",
            "user": "bbmiller",
            "version": "7",
            "uid": "451048",
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
        "street": "West Lexington St.",
        "housenumber": "1412"
    }
    assert data[-1]["node_refs"] == ["2199822281", "2199822390", "2199822392", "2199822369",
                                     "2199822370", "2199822284", "2199822281"]


if __name__ == "__main__":
    test()