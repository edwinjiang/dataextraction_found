#!/usr/bin/python
#encoding:utf8

import xml.etree.cElementTree as ET
import codecs
import json
from pypinyin import lazy_pinyin
import httplib
import md5
import urllib
import random
from pymongo import MongoClient

'''
  以下代码是对上海地区的OSM地图数据进行分析处理：然后将处理结果转换成JSON格式并导入到MongoDB数据库
'''


OSMFILE = "shanghai_sample_k50.osm"
CREATED = ["version", "changeset", "timestamp","uid"]

appid = '20170919000083787'
secretKey = 'hystuLksvUJZNO6xtEXt'

'''
调用百度翻译API把中文翻译成英文
'''
def translate_func(text):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    fromLang = 'zh'
    toLang = 'en'
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()

    ''' API请求参数 '''
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.quote(
        text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        '''百度翻译API地址'''
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        result = eval(response.read())
        return result["trans_result"][0]["dst"]
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
'''
  处理OSM数据
'''
def process_osm_data(element):
    node = {}
    temp = {}
    refs_temp = []

    '''开始解析OSM数据'''
    if element.tag == "node" or element.tag == "way":
        '''
          解析type是node的数据
        '''
        for item in element.iter("node"):
            node["id"] = item.attrib["id"]
            node["type"] = item.tag
            for i in range(len(CREATED)):
                temp[CREATED[i]] = item.attrib[CREATED[i]]
            node["created"] = temp
            node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]
            '''
               判断是否中文，是的话，则转换为拼音
            '''
            if u'\u4e00' <= item.attrib["user"] <= u'\u9fff':
                node["user"] = lazy_pinyin(item.attrib["user"])
            else:
                node["user"] = item.attrib["user"]

        '''
           解析type是way的数据
        '''
        for item in element.iter("way"):
            node["id"] = item.attrib["id"]
            node["type"] = item.tag
            for i in range(len(CREATED)):
                temp[CREATED[i]] = item.attrib[CREATED[i]]
            node["created"] = temp
            if u'\u4e00' <= item.attrib["user"] <= u'\u9fff':
                node["user"] = lazy_pinyin(item.attrib["user"])
            else:
                node["user"] = item.attrib["user"]

            for child in item:
                for refer in child.iter("nd"):
                    refs_temp.append(refer.attrib["ref"])
            node["node_refs"] = refs_temp

            for child in item:
                for address in child.iter("tag"):
                    if address.attrib['k'] == "oneway":
                        if address.attrib['v'] == -1:
                            address.attrib['v'] = "no"
                        else:
                            address.attrib['v'] = "yes"

                    if address.attrib['k'] == "railway":
                        node["railway"] = address.attrib["v"]
                    if address.attrib['k'] == "highway":
                        node["highway"] = address.attrib["v"]
                    if address.attrib['k'] == "amenity":
                        node["amenity"] = address.attrib["v"]
                    if address.attrib['k'] == "shop":
                        node["shop"] = address.attrib["v"]
                    if address.attrib['k'] == "cycleway":
                        node["cycleway"] = address.attrib["v"]

                    if address.attrib['k'] == "name":
                        if u'\u4e00' <= address.attrib["v"] <= u'\u9fff':
                            node["name"] = address.attrib['v']

                            '''
                               判断是否包含name:en键值，如果不包含，则调用百度API进行翻译，并赋值给name:en
                            '''
                            if "name:en" not in address.attrib.keys():
                                node["name:en"] = translate_func(node["name"].encode("UTF-8"))
                            else:
                                node["name:en"] = address.attrib["v"]
                        else:
                            node["name"] = address.attrib['v']
        return node
    else:
        return  None


def process_map(osm_file,pretty=False):
    file_out = "{0}.json".format("Shanghai_osm_data")
    data = []
    '''
     注意一定要以UTF-8模式打开
    '''
    with codecs.open(file_out, "w","utf-8") as fo:
        for _, element in ET.iterparse(osm_file):
            '''
              处理OSM数据
            '''
            el = process_osm_data(element)
            if el:
                data.append(el)

                '''
                  是否对JSON文件格式进行缩进
                '''
                if pretty:
                    fo.write(json.dumps(el,encoding='utf-8',ensure_ascii=False,indent=2))
                else:
                    fo.write(json.dumps(el,encoding='utf-8',ensure_ascii=False))
    return data

def parsedata():
    '''
      数据处理主过程
    '''
    data = process_map(OSMFILE, True)

    '''
      数据加载到MongoDB
    '''
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.shaosm
    insert_data(data, db)



def insert_data(data, db):
    for realdata in data:
        db.mapdata.save(realdata)

if __name__ == "__main__":
    #解析处理OSM数据
    parsedata()