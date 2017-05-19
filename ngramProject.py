#_*_coding:utf-8_*_

import snownlp
from readability.readability import Document
from sklearn.decomposition import TruncatedSVD
from sklearn.random_projection import sparse_random_matrix
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from numpy import *
import json
import jieba
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

class JsonParser(object):
	def __init__(self):
		super(JsonParser, self).__init__()
#		self.fileName = fileName
		self.regexTargetUrl = r'http://www.360kad.com/product/.*'
		self.regexHTML1 = r'<script.*?</script>'
		self.regexHTML2 = r'<.*?>'
		self.regexHTML3 = r'&#13;'
		self.regexSymbol = r'\s+'
		self.newstring = ''
		self.featureList = list()										#特征列表
		self.stopwords = list()										#stop words list


	def topicModel(self, text, topicNum):
		if text:									#关键词提取方法
			topic_model = snownlp.SnowNLP(text)
			topicList = topic_model.keywords(topicNum)
			return ' '.join(topicList)

	def readFile(self, fileName):
		file = open(fileName, 'r')
		line = file.readline()
		while line:
			line = file.readline().strip().rstrip(',').lstrip('[').rstrip(']')					#这数据真特么恶心
			yield line

	def divideWords(self, summary):										#分词方法
		stopkey=[line.strip().decode('gb18030') for line in open('stopwords.txt').readlines()]
		if summary:
			seg_list = jieba.cut(summary, cut_all=False)						#结巴分词得到分词后list
			for seg in seg_list:									#^
				if seg not in stopkey:								#|
					self.stopwords.append(seg)						#去停用词
			summary = ' '.join(self.stopwords)							#|
			self.stopwords = list()									#clear list
			return summary									#return word's string

	def parserJson(self, line):										#传入的没line为一行jsonData
#		file = open(fileName, 'r')
#		line = file.readline()				
		while line:											#若该行不为空
			json_context = json.loads(line) 
#			print type(json_context['_id']), json_context['item'] #type(json_context['item'])
			webSite_url = json_context['_id']
#			webSite_context = re.subn(self.regex2,self.newstring, Document(json_context['item']).summary())
			webSite_context = Document(json_context['item']).summary()
			webSite_context = re.sub(self.regexHTML2, self.newstring , webSite_context)		#正则替换
			webSite_context = re.sub(self.regexHTML3, self.newstring , webSite_context)		#正则替换
			webSite_context = re.sub(self.regexSymbol, self.newstring, webSite_context)		#正则替换
			if webSite_context:
				return webSite_context
			else:
				pass
#			if webSite_context:
#				seg_list = jieba.cut(webSite_context, cut_all=False)				#结巴分词得到分词后list
#				for seg in seg_list:								#^
#					if seg not in stopkey:							#|
#						stopwords.append(seg)						#去停用词
#				webSite_context = ' '.join(stopwords)						#|
#				stopwords = list()
#			topicWordsList = webSite_context								

#			webSite_context = str(re.subn(self.regex1, self.newstring, str(re.subn(self.regex2, self.newstring, json_context['item']))))

	def cutWords(self):
		lines = open('stopWords.txt', 'r').readlines()							#初期想法，并没什么乱用，放着凑行数
		lineFinalWorld = ""										#储存分词去停用词后的字符串
		for line in lines:
#			line = line.decode('gbk').encode('utf-8')
			self.stopWordsList.append(line)
		stopWords = {}.fromkeys(self.stopWordsList)							#建立停用词表
		for datas in dataSet:
			segsList = " ".join(jieba.cut(datas, cut_all=False)).split(" ")					#分词
			for segs in segsList:
				if segs not in stopWords:
					lineFinalWorld = lineFinalWorld + '\t' + segs
					self.featureList.append(lineFinalWorld)
				lineFinalWorld = ""								#清空

	def tfidfFunction(self):
		tfidf = tfidfMethod(corpus)
		vectorizer=CountVectorizer()
		transformer=TfidfTransformer()
		tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))				#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵#
		print type(tfidf), "tfidfpass"
		svd = TruncatedSVD(n_components=2)
		svdResult = svd.fit_transform(tfidf)
		return svdResult

	def logisticRegression(self, samples, classifi, targets):
		classifier = logisticRegression()
		classifier.fit(samples, classifi)
		for target in targets:
			x = classifier.predict()





if __name__ == '__main__':
	parser = JsonParser()
#	parser.parser()
	try:
		for line in parser.readFile('360kad.json'):
			a = parser.parserJson(line)
			b = parser.divideWords(a)
			c = parser.topicModel(b, 10)
			print c
			print '<--------------------------------------------------------------------------->'
	except:
		pass
	finally:
		pass
