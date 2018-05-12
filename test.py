import pymongo

clinet = pymongo.MongoClient("localhost", 27017)
db = clinet["comments"]
jike = db['jike']

print(jike.insert({'id':1}))

for post in jike.find():
    print(post)