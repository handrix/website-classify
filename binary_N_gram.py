# -*- coding: UTF-8 -*-     
'''
Created on Jun 10, 2016

@author: zequnfeng
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
conn.open_connection("test")
conn2 = MongodbConnLocal.MongoPipeline()
conn2.open_connection("test")
datas = load.loadData('test', 'onegram')

def binaryNgram(n, data):
    # strs = webParser.contextExtraction(data)
    # strs = Document(data).summary()
    # strs = html2text.html2text(strs).replace(' ', '').replace('\t', '').replace('\n', '')
    # strs = binascii.b2a_hex(strs)
    first = 0
    bowls = list()
    for x in range(len(data)/1):
        first = 2 * x
        end = first + 2 * n
        s = data[first:end]
        # if len(s) == 2 * n:
        if len(s) != 2 * n:
            break
        bowls.append(s)
    return bowls
fea = list()
classifi = list()
for data in datas:
    # classifier = list()

    # binary = binaryNgram(8, data['feature'])
    # if len(binary) != 0:

        # binary = binaryNgram(1, data['feature'])
    # pattern = re.compile(r'http://www.111.com.cn/product/.*')
    # match = pattern.match(data['_id'])    
    # if match:
    #     classifier.append(1)
    # else:
    #     classifier.append(0)
    fea.append(data['feature'])
    classifi.append(data['classifier'])
    # conn2.process_item({"_id":data['_id'],"feature":binary,"classifier":data['classifier']},"eightgram")

tfidf = words2DataParser.words2Data(fea)
fea = list()
tfidf = tfidf.toarray()

for x in range(len(tfidf)):
    conn2.process_item({"feature":tfidf[x],"classifier":classifi[x]},"oneGramData")
