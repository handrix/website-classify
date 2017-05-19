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
import random
from sklearn import linear_model
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import roc_auc_score 
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import fbeta_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

load = cutWordsproject.DataParser()

datas = load.loadData('test', 'eightGramData')
train = list()
train_classifiy = list()
test = list()
test_classifiy = list()

for data in datas:

	# feature = data['feature'].split('\t')
	# feature = map(float, feature)
	feature = data['feature']
	if '111.com' in data['_id']:
		train.append(feature)
		train_classifiy.append(int(data['classify']))
	else:
		test.append(feature)
		test_classifiy.append(int(data['classify']))

clfLogistic = LogisticRegression(penalty='l2', C=2.9,solver = 'lbfgs')
clfLogistic.fit(train, train_classifiy)
scoreLogistic = clfLogistic.score(test, test_classifiy)
y_pred = list()
for pre in test:
	pre = clfLogistic.predict(pre).tolist()[0]
	y_pred.append(pre)
	# print len(pre)
	# a = clfLogistic.predict_proba(pre)
	# print a

a = precision_score(test_classifiy, y_pred, average='binary')
b = recall_score(test_classifiy, y_pred, average='binary')
c = f1_score(test_classifiy, y_pred, average='binary')

print a,b,c,scoreLogistic   