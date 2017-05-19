# -*- coding: UTF-8 -*-     
'''
Created on Jun 10, 2016

@author: sun
'''

import MongodbConn
import MongodbConnLocal
import cutWordsproject
import binascii
import struct
import re
from readability.readability import Document
import html2text

# import numzhuan

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
webParser = cutWordsproject.ContextExtraction()

load = cutWordsproject.DataParser()
conn = MongodbConn.MongoPipeline()
conn.open_connection("new_shiyan")
conn2 = MongodbConnLocal.MongoPipeline()
conn2.open_connection("test")
datas = load.loadData('new_shiyan', 'kangduoai_n_1')

def binaryNgram(n, data):
    # strs = webParser.contextExtraction(data)
    strs = Document(data).summary()
    strs = html2text.html2text(strs).replace(' ', '').replace('\t', '').replace('\n', '')
    strs = binascii.b2a_hex(strs)
    # first = 0
    # bowls = list()
    # for x in range(len(strs)/1):
    #     first = 2 * x
    #     end = first + 2 * n
    #     s = strs[first:end]
    #     # if len(s) == 2 * n:
    #     if len(s) != 2 * n:
    #         break
    #     bowls.append(s)
    return strs

for data in datas:
    classifier = list()
    binary = binaryNgram(1, data['item'])
    pattern = re.compile(r'http://www.360kad.com/product/.*')
    match = pattern.match(data['_id'])    
    if match:
        classifier.append(1)
    else:
        classifier.append(0)
    conn2.process_item({"_id":data['_id'],"feature":binary,"classifier":classifier[0]},"1gram")
