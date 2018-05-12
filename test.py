import pymongo

clinet = pymongo.MongoClient("localhost", 27017)
db = clinet["comments"]
jike = db['jike']

for topic in jike.find():
    print(topic['_id'])