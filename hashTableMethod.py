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

import MongodbConn
import cutWordsproject
from sklearn.decomposition import TruncatedSVD

conn = MongodbConn.MongoPipeline()
load = cutWordsproject.DataParser()
conn.open_connection("test")

datas = load.loadData('test', 'eightgram')
wordsTable = {}
num = 0
for data in datas:
	print num
	num += 1
	words = data['feature']
	for word in words:
		if word not in wordsTable:
			wordsTable[word] = 0
datas = load.loadData('test', 'eightgram')
svd = TruncatedSVD(n_components=300)
tf = list()
for data in datas:
	tempList = list()
	temp = wordsTable
	words = data['feature']
	for word in words:
		temp[word] += 1
	for value in temp.values():
		tempList.append(value)
	tempStr = map(int, tempList)
	# svd = TruncatedSVD(n_components=300)
	# print tempStr
	# tempStr = svd.fit_transform(tempStr)
	# tempStr = tempStr[0].tolist()
	tf.append(tempStr)
	# conn.process_item({"_id":data['_id'],"feature":tempStr,"classifier":data['classifier']},"eightGramData")
