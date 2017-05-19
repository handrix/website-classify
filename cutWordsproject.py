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
import sys
import json
import jieba
import pymongo
import contextExtraction											#基于行块分布函数的通用网页正文抽取算法
import sklearn													#机器学习库
from MongodbConn import MongoPipeline									#该类操作数据库
#<----------------tfidf------------------->
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
#<----------------tfidf------------------->
#<-------------2binary----------------->
import binascii													#html转二进制
import struct
#<-------------2binary----------------->

class DataParser(object):
	"""docstring for DataParser"""
	"""该类解析数据loadData方法为数据库操作，DataParser为解析json数据"""
	def __init__(self):
		self.conn = MongoPipeline()

	def loadData(self, dbName='shiyan', tableName='yiyao'):						#连接数据库并读取数据
		self.conn.open_connection(dbName)
		ids = self.conn.getIds(tableName)
		self.conn.close_connection()
		return ids

	def DataParser(self, data):								#该类解析数据
		parser = json.load(data)
		_id = parser['_id']
		item = parser['item']
		

class ContextExtraction(object):
	"""docstring for ContextExtraction"""
	def __init__(self):
		pass

	def contextExtraction(self, data):
		context = contextExtraction.extract(data)
		context = contextExtraction.remove_any_tag(context)
		context = contextExtraction.remove_empty_line(context)
		return context
		

class Words2Data(object):
	"""docstring for Words2Data"""
	def __init__(self):
		self.vectorizer = CountVectorizer()					#该类会将文本中的词语转换为词频矩阵
		self.transformer = TfidfTransformer()					#该类会统计每个词语的tf-idf权值

	def words2Data(self, dataSet):
  		tfidf=self.transformer.fit_transform(self.vectorizer.fit_transform(dataSet))
  		# tfidfMatrix = tfidf.toarray()
  		# tf = self.vectorizer.fit_transform(dataSet)
  		# tfMatrix = tf.toarray()
  		return tfidf
		

class CutWords(object):
	"""docstring for CutWords"""
	def __init__(self):
		self.stopwords = list()
		self.jieba = jieba

	def loadUsrWordsTable(self, wordsTable):							#导入自定义词表
		self.jieba.load_userdict(wordsTable)

	def cutWords(self, context):
		context = context.strip(' ').strip('\n').strip()
		seg_list = self.jieba.cut(context, cut_all=False)
		return seg_list

	def stopWords(self, afterCutContext, stopWordsTable):								#参数为已经过分词处理的字符串和停用词表
		stopkey=[line.strip().decode('gb18030') for line in open(stopWordsTable).readlines()]
		if afterCutContext:
			self.stopwords = list()
			for seg in afterCutContext:									#^
				seg = str(seg)
				if seg not in stopkey:
					if seg != ' ' and seg != '\n' and seg != '	' and seg != '|' and seg != '\n' and seg != 'nbsp':								#|
						self.stopwords.append(seg)						#去停用词
			return self.stopwords
	def html2binary(self, html):											#HTML文档二进制
		temp = binascii.b2a_hex(html)
		binary = bin(int(temp, 16))[2:]
		return binary

class LR(object):
	"""docstring for LR"""
	def __init__(self, arg):
		super(LR, self).__init__()
		self.arg = arg
		
		
if __name__ == '__main__':
	example = DataParser()
	data = example.loadData()