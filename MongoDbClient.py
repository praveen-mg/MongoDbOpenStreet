from pymongo import MongoClient
import pprint
client = MongoClient('localhost', 27017)

db = client.work

def find():
    cities = db.city.find({ "name": "PIE"})
    for a in cities:
        pprint.pprint(a)
    #user_cboothroyd = db.city.find({"created.user" : "cboothroyd"})
    
    #for a in user_cboothroyd:
        #pprint.pprint(a)
        
    #print "Number contributed by cboothroyd", user.count()
    print "Total number of distinct Users:",len(db.city.distinct("created.user"))
    #print ""db.city.find({"type":"node"}).count()

if __name__ == '__main__':
    find()
