#coding:utf-8
#auth_ZequnFeng

import MongodbConn
import cutWordsproject
import random
from sklearn import linear_model
from numpy import *
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import roc_auc_score 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

load = cutWordsproject.DataParser()

conn = MongodbConn.MongoPipeline()
conn.open_connection("new_shiyan")
datas = load.loadData('new_shiyan', 'newSvd_1000')

positive_111 = list()
nagitive_111 = list()
positive_kad = list()
nagitive_kad = list()
num = 0
for data in datas:
	num +=1
	if '111.com' in data['_id']:
		if data['classify'] == '1':
			positive_111.append(data['feature'])
		else:
			nagitive_111.append(data['feature'])
	else:
		if data['classify'] == '1':
			positive_kad.append(data['feature'])
		else:
			nagitive_kad.append(data['feature'])		

train = list()
train_classify = list()
for x in range(1000):
	positive_111[x] = positive_111[x].strip('\n').split('\t')
	positive_111[x] = map(float, positive_111[x])
	nagitive_111[x] = nagitive_111[x].strip('\n').split('\t')
	nagitive_111[x] = map(float, nagitive_111[x])
	train.append(positive_111[x])
	train_classify.append(1)
	train.append(nagitive_111[x])
	train_classify.append(0)

print 'length of train:',len(train)
classifier = LogisticRegression()

classifier.fit(train, train_classify)

test = list()
test_classify = list()
# print len(positive_111), len(nagitive_111)
temp = positive_kad[2000:2500] + nagitive_kad[2000:2500]
for x in temp:
	x = x.strip('\n').split('\t')
	x = map(float, x)
	test.append(x)
for x in range(1000):
	if x <= 499:
		test_classify.append(1)
	else:
		test_classify.append(0)
print 'length of test:',len(test)
score = classifier.score(test, test_classify)

clf = linear_model.SGDClassifier(loss='log')

print 'off line train score of P:', score

clf.fit(train, train_classify)
score2 =  clf.score(test, test_classify)
print score2


temp_score = list()
temp_lable = list()

for x in range(len(test)):
	temp_lable.append(test_classify[x])
	temp_score.append(classifier.predict_proba(test[x])[0][1])
c = roc_auc_score(temp_lable, temp_score)
print 'off line train score of AUC:', c

# clf = linear_model.SGDClassifier()
# clf.fit(train, train_classify)
# b = clf.score(test, test_classify)
# print b

for a in range(len(test)):
	# print classifier.predict_proba(test[a]), classifier.predict(test[a]), test_classify[a]
	if float(clf.predict_proba(test[a])[0][1]) > float(0.416) and float(clf.predict_proba(test[a])[0][1]) < float(0.594):
		train.append(test[a]); train_classify.append(test_classify[a])
		tmplist = list()
		tmplist.append(test_classify[a])
		clf.partial_fit(test[a], tmplist)
		tmplist = list()
b = clf.score(test, test_classify)
print '!!!on line train score of  P!!!:', b

temp_score = list()
temp_lable = list()

for x in range(len(test)):
	temp_lable.append(test_classify[x])
	temp_score.append(classifier.predict_proba(test[x])[0][1])
c = roc_auc_score(temp_lable, temp_score)
print 'on line train score of AUC:', c