#_*_coding:utf-8_*_
#auth_ZequnFeng

#
#　　　　　　　　┏┓　　　┏┓+ +
#　　　　　　　┏┛┻━━━┛┻┓ + +
#　　　　　　　┃　　　　　　　┃ 　
#　　　　　　　┃　　　━　　　┃ ++ + + +
#　　　　　　 ████━████ ┃+
#　　　　　　　┃　　　　　　　┃ +
#　　　　　　　┃　　　┻　　　┃
#　　　　　　　┃　　　　　　　┃ + +
#　　　　　　　┗━┓　　　┏━┛
#　　　　　　　　　┃　　　┃　　　　　　　　　　　
#　　　　　　　　　┃　　　┃ + + + +
#　　　　　　　　　┃　　　┃　　　　Code is far away from bug with the animal protecting　　　　　　　
#　　　　　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug　　
#　　　　　　　　　┃　　　┃
#　　　　　　　　　┃　　　┃　　+　　　　　　　　　
#　　　　　　　　　┃　 　　┗━━━┓ + +
#　　　　　　　　　┃ 　　　　　　　┣┓
#　　　　　　　　　┃ 　　　　　　　┏┛
#　　　　　　　　　┗┓┓┏━┳┓┏┛ + + + +
#　　　　　　　　　　┃┫┫　┃┫┫
#　　　　　　　　　　┗┻┛　┗┻┛+ + + +
#


import re

from readability.readability import Document
import html2text
import random
import MongodbConnLocal
import cutWordsproject
import MongodbConn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from scipy.io import mmwrite, mmread
from sklearn import feature_extraction
#<---------------------讲真，python要是再不对中文友好点我就把这几行代码写成宏-------------------------------->
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#<---------------------讲真，python要是再不对中文友好点我就把这几行代码写成宏-------------------------------->

load = cutWordsproject.DataParser()						#实例化加载数据类
webParser = cutWordsproject.ContextExtraction()				#实例化正文提取类
wordsParser = cutWordsproject.CutWords()					#实例化分词类
words2DataParser = cutWordsproject.Words2Data()				#实例化量化类

def method1():
	conn = MongodbConn.MongoPipeline()
	conn.open_connection("new_shiyan")
	# wordsParser.loadUsrWordsTable('wordsTable.txt')
	datas = load.loadData('new_shiyan', 'kangduoai_n_1')
	dataSet = list()
	# f = open('corups.txt', 'a')
	num = 0
	for data in datas:
		if num%100==0:
			print num
		num += 1
		temp = list()
		if data['_id'] and data['item']:
			pattern = re.compile(r'http://www.360kad.com/product/.*')
			match = pattern.match(data['_id'])
			if match:
				temp.append('1')
			else:
				temp.append('0')
			context = webParser.contextExtraction(str(data['item']))
			context = re.sub('[A-Za-z|\d|_ ..|{]','',context)
			context = context.replace(' ', '').replace('\t', '').replace("\r", "").replace('\n', '')

			afterCut = wordsParser.cutWords(context)
			afterStopWords = wordsParser.stopWords(afterCut, 'stopwords.txt')
			temp.append(data['_id'])
			temp.append(' '.join(afterStopWords))
			# print temp[2]
			# f.write(temp[0] + '\t' + temp[1] + '\t' + temp[2] + '\n')
			conn.process_item({"_id":temp[1],"ana_result":temp[2],"kind":temp[0]},"cutWordWithOutDictionary")
			dataSet.append(temp)
	return dataSet
	# conn.close_connection()
	# f.close()
# method1()
conn = MongodbConn.MongoPipeline()
conn.open_connection("test")
conn2 = MongodbConnLocal.MongoPipeline()
conn2.open_connection("test")
datas = load.loadData('test', 'eightgram')

classify = list()
ana_result = list()
new_result = list()
wordstable = list()
url = list()
for data in datas:
	temp = list()
	num = len(data['feature'])/10
	url.append(str(data['_id']))
	ana_result.append(' '.join(data['feature'][:num]))
	classify.append(str(data['classifier']))
	# tmp = data['feature'].split(' ')
	# temp.append(tmp)
	# new_result.append(temp)


print 'start sort tfidf'
tfidf = words2DataParser.words2Data(ana_result)
ana_result = list()
# tfidf = mmread('tfidf.mtx')

print 'success sort tfidf.start sort svd'
svd = TruncatedSVD(n_components=200)
svdResult = svd.fit_transform(tfidf)
tfidf = list()
# tfidf = tfidf.toarray()
print 'success sort svd'




# print len(lalalalal)
for x in range(len(url)):
	tempurl = url[x]
	tempclassify = classify[x]
	result = svdResult[x].tolist() 
	# result = map(str, result)
	# result = '\t'.join(result)
	conn.process_item({"_id":tempurl,"classify":tempclassify,"feature":result},"eightGramData")
