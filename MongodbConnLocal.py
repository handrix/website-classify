#code=utf-8
import pymongo

import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

class MongoPipeline:

    
    # host = '127.0.0.1'
    host = '127.0.0.1'
    port =27017
#     mongo_db ="calender"
#     mongo_db = ""



    def open_connection(self,mongo_db):
        self.client = pymongo.MongoClient(self.host,self.port)
        self.db = self.client[mongo_db]
        print "connected"

    def close_connection(self):
        self.client.close()

    def process_item(self, item, collection_name):
        self.db[collection_name].insert(item)
        return item
    
    def getIds(self,collection_name):
        collection = self.db[collection_name]
        return collection.find()
    def GetNation(self,collection_name,id):
        return self.db[collection_name].find_one({'_id':id})
    def existsornot(self,collection_name,id):
        ting = self.db[collection_name].find_one({'_id':id})
        if ting == None:
            return 0
        else: 
            return 1
if __name__ == "__main__":
    temp = list()
#     conn = MongoPipeline()
#     conn.open_connection('drug')
# #    item = {"taskname":"1","startdate":"19","startdate":"20"}
# #    conn.process_item(item, "date_config")
#     ids = conn.getIds('data')
#     conn.close_connection()
#     for x in ids:
#         temp.append(x['name'])
#         try:
#             if x['product_name']:
#                 temp.append(x['product_name'])
#         except:
#             pass
#         else:
#             pass
#         finally:
#             pass

#     temp = list(set(temp))
#     f = open('wordsTable.txt', 'a')
#     for tem in temp:
#         f.write(tem + '\n')
#     f.close()
    


    
    
