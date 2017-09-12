#!/usr/bin/python
#encoding:utf8

import codecs
import csv
import json
import pprint
import re

DATAFILE = 'arachnid.csv'
FIELDS = {'rdf-schema#label': 'label',
          'URI': 'uri',
          'rdf-schema#comment': 'description',
          'synonym': 'synonym',
          'name': 'name',
          'family_label': 'family',
          'class_label': 'class',
          'phylum_label': 'phylum',
          'order_label': 'order',
          'kingdom_label': 'kingdom',
          'genus_label': 'genus'}


def process_file(filename, fields):
    process_fields = fields.keys()
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            # YOUR CODE HERE
            if line["name"] == "NULL":
                name = str(line["rdf-schema#label"])
            else:
                name = str(line["name"])

            synonym_data = parse_array(line["synonym"]) if line["synonym"] != 'NULL' else None

            rdf_schema_label = str(line["rdf-schema#label"]).split('(')[0].lstrip().rstrip()
            URL = str(line["URI"]).lstrip().rstrip()
            description = str(line["rdf-schema#comment"]).lstrip().rstrip()
            family_label = str(line["family_label"]).lstrip().rstrip() if line["family_label"] != 'NULL' else None
            class_label = str(line["class_label"]).lstrip().rstrip() if line["class_label"] != 'NULL' else None
            phylum_label = str(line["phylum_label"]).lstrip().rstrip() if line["phylum_label"] != 'NULL' else None
            order_label = str(line["order_label"]).lstrip().rstrip() if line["order_label"] != 'NULL' else None
            kingdom_label = str(line["kingdom_label"]).lstrip().rstrip() if line["kingdom_label"] != 'NULL' else None
            genus_label = str(line["genus_label"]).lstrip().rstrip() if line["genus_label"] != 'NULL' else None

            data.append({fields["rdf-schema#label"]: rdf_schema_label,
                         fields["URI"]: URL,
                         fields["rdf-schema#comment"]: description,
                         fields["name"]: name,
                         fields["synonym"]: synonym_data,
                         "classification": {fields["family_label"]: family_label,
                                            fields["class_label"]: class_label,
                                            fields["phylum_label"]: phylum_label,
                                            fields["order_label"]: order_label,
                                            fields["kingdom_label"]: kingdom_label,
                                            fields["genus_label"]: genus_label}
                         })

    return data


def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    data = process_file(DATAFILE, FIELDS)
    print "Your first entry:"
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None,
        "name": "Argiope",
        "classification": {
            "kingdom": "Animal",
            "family": "Orb-weaver spider",
            "order": "Spider",
            "phylum": "Arthropod",
            "genus": None,
            "class": "Arachnid"
        },
        "uri": "http://dbpedia.org/resource/Argiope_(spider)",
        "label": "Argiope",
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }

    assert len(data) == 76
    assert data[0] == first_entry
    assert data[17]["name"] == "Ogdenia"
    assert data[48]["label"] == "Hydrachnidiae"
    assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]


if __name__ == "__main__":
    test()