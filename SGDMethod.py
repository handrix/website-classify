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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

load = cutWordsproject.DataParser()

# conn = MongodbConn.MongoPipeline()
# conn.open_connection("test")
data_nagitive_111 = load.loadData('new_shiyan', 'nagitive_111')
data_positive_111 = load.loadData('new_shiyan', 'positive_111')
data_positive_kad = load.loadData('new_shiyan', 'positive_kad')
data_nagitive_kad = load.loadData('new_shiyan', 'nagitive_kad')

positive_111 = list()
nagitive_111 = list()
positive_kad = list()
nagitive_kad = list()

train = list()
train_classify = list()

test = list()
test_classify = list()

def data2memrry(x):
	x = x.strip('\n').split('\t')
	x = map(float, x)
	return x

num = 0
for data in zip(data_positive_kad, data_nagitive_kad):
	num += 1
	if num <= 8000:
		try:
			test.append(data[0]['feature'])
			test_classify.append(1)
		except:
			continue
		test.append(data[1]['feature'])
		test_classify.append(0)

# for data in data_positive_kad:
# 	test.append(data['feature'])
# 	test_classify.append(1)
for data in data_nagitive_kad:
	# num += 1
	# if num > 7307:
	test.append(data['feature'])
	test_classify.append(0)

for data in data_nagitive_111:
	train.append(data['feature'])
	train_classify.append(0)

for data in data_positive_111:
	train.append(data['feature'])
	train_classify.append(1)



# for x in range(2000):
# 	positive_111[x] = positive_111[x].strip('\n').split('\t')
# 	positive_111[x] = map(float, positive_111[x])
# 	nagitive_111[x] = nagitive_111[x].strip('\n').split('\t')
# 	nagitive_111[x] = map(float, nagitive_111[x])
# 	train.append(positive_111[x])
# 	train_classify.append(1)
# 	train.append(nagitive_111[x])
# 	train_classify.append(0)

print 'length of train:',len(train)

# print len(positive_111), len(nagitive_111)
# temp = positive_kad[500:1000] + nagitive_kad[500:1000]
# for x in temp:
# 	x = x.strip('\n').split('\t')
# 	x = map(float, x)
# 	test.append(x)
	
# for x in range(1000):
# 	if x <= 499:
# 		test_classify.append(1)
# 	else:
# 		test_classify.append(0)
print 'length of test:',len(test)

# scaler = StandardScaler()
# scaler.fit(train)
# train = scaler.transform(train)
# test = scaler.transform(test)
# print type(train), type(test)

n = len(train)
# print np.ceil(10**6 / n)
alpha = 0.000001								#learning_rate
clf = SGDClassifier(loss = 'log',penalty='l2',n_iter = 1, warm_start=False, random_state=42, alpha=alpha)
clf.fit(train, train_classify)
scoreSGD = clf.score(test, test_classify)

clfLogistic = LogisticRegression(penalty='l2', max_iter=50, C=3.0,solver = 'lbfgs')
clfLogistic.fit(train, train_classify)
scoreLogistic = clfLogistic.score(test, test_classify)

# scoreLogistic = float(1) - scoreLogistic
print 'bgdErrorRate:', scoreLogistic

#随机下降算法实现的模型更新
# alpha = 0.0001
num = 0

for a in range(len(test)):
	
	previousScore = scoreSGD
	# print 'sgd:',clf.predict_proba(test[a])[0][1], clf.predict(test[a]), test_classify[a]
	if float(clf.predict_proba(test[a])[0][1]) > float(0.45) and float(clf.predict_proba(test[a])[0][1]) < float(0.55):
		num += 1
		clf.set_params(n_iter=1,alpha = alpha)
		# train.append(test[a]); train_classify.append(test_classify[a])
		tmplist = list()
		tmplist.append(test_classify[a])
		clf.partial_fit(test[a], tmplist)
		score = clf.score(test, test_classify)
		# if score > previousScore:
		# 	alpha *= 0.5
		# previousScore = score
		# print 'iterScore:', score, num
print num
score = clf.score(test, test_classify)
# score = float(1) - score
print 'online learning ErrorRate:',score


SGDtempScore = list()
BGDtempScore = list()
for x in range(len(test)):
	predic = clfLogistic.predict_proba(test[x])[0][1]
	SGDtempScore.append(float(clf.predict_proba(test[x])[0][1]))
	BGDtempScore.append(float(predic))
	# print predic, clfLogistic.predict(test[x])[0]

SGDAucScore = roc_auc_score(test_classify, SGDtempScore)
BGDAucScore = roc_auc_score(test_classify, BGDtempScore)

print 'SGDAuc:',SGDAucScore,'BGDAuc:',BGDAucScore

#批量梯度下降算法实现的模型更新
# for a in range(len(test)):
# 	# print 'sgd:',clf.predict_proba(test[a])[0][1], clf.predict(test[a]), test_classify[a]
# 	if float(clfLogistic.predict_proba(test[a])[0][1]) > float(0.4) and float(clfLogistic.predict_proba(test[a])[0][1]) < float(0.6):
# 		train.append(test[a]); train_classify.append(test_classify[a])
# 		clfLogistic.fit(train, train_classify)
# 		score = clfLogistic.score(test, test_classify)
# 		print score