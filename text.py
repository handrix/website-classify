import MongodbConn
import cutWordsproject
from sklearn.preprocessing import normalize
from scipy import sparse

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

load = cutWordsproject.DataParser()

conn = MongodbConn.MongoPipeline()
conn.open_connection("new_shiyan", "125.223.31.171")

datas = load.loadData('new_shiyan', 'cutWords')


def data2memrry(x):
	x = x.strip('\n').split('\t')
	x = map(float, x)
	return x
# num = 0
# train = list()
for data in datas:
	# print num
	# num += 1
	# feature = normalize(data2memrry(data['ana_result']))
	# print num
	# train.append(feature)
	feature = data2memrry(data['feature'])
	if '111.com' in data['_id']:
		if data['kind'] ==  '1':
			conn.process_item({"_id":data['_id'],"feature":feature,"classify":data['kind']},"WODpositive_111")
		else:
			conn.process_item({"_id":data['_id'],"feature":feature,"classify":data['kind']},"WODnagitive_111")
	if '360kad.com' in data['_id']:
		if data['kind'] == '1':
			conn.process_item({"_id":data['_id'],"feature":feature,"classify":data['kind']},"WODpositive_kad")
		else:
			conn.process_item({"_id":data['_id'],"feature":feature,"classify":data['kind']},"WODnagitive_kad")

# for data in datas:
# 	feature = data2memrry(data['feature'])
# 	if '111.com' in data['_id']:
# 		if data['classify'] ==  '1':
# 			conn.process_item({"_id":data['_id'],"feature":feature,"classify":data['classify']},"positive_111")
# 		else:
# 			conn.process_item({"_id":data['_id'],"feature":feature,"classify":data['classify']},"nagitive_111")
# 	if '360kad.com' in data['_id']:
# 		if data['classify'] == '1':
# 			conn.process_item({"_id":data['_id'],"feature":feature,"classify":data['classify']},"positive_kad")
# 		else:
# 			conn.process_item({"_id":data['_id'],"feature":feature,"classify":data['classify']},"nagitive_kad")