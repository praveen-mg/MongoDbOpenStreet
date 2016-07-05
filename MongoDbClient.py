from pymongo import MongoClient
import pprint
client = MongoClient('localhost', 27017)

db = client.work

def find():
    cities = db.city.find({ "name": "PIE"})
    for a in cities:
        pprint.pprint(a)


if __name__ == '__main__':
    find()
