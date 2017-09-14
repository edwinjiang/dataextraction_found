#!/usr/bin/python
#encoding:utf8
import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):
    # YOUR CODE HERE
    context = ET.iterparse(filename)
    data = {'bounds': 0,
            'member': 0,
            'nd': 0,
            'node': 0,
            'osm': 0,
            'relation': 0,
            'tag': 0,
            'way': 0}
    for event, elem in context:
        data[elem.tag] += 1
    return data


def test():
    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                    'member': 3,
                    'nd': 4,
                    'node': 20,
                    'osm': 1,
                    'relation': 1,
                    'tag': 7,
                    'way': 1}


if __name__ == "__main__":
    test()