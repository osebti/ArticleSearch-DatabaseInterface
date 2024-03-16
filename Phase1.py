from pymongo import MongoClient
import subprocess
import json



while(True): # sanity check for the input 
    try:
        port = int(input("choose a port: ")) # prompting user for filename and port number
        filename = str(input("choose a file: "))
        break
        
    except:
        print("invalid input, try again")




c=MongoClient('localhost',port)   
port=str(port) # type-casting for mongo import subprocess
  
db=c["291db"]
collection=db["dblp"]





if ('dblp' in db.list_collection_names()):
    collection=db["dblp"]
    collection.drop()
    
collection=db["dblp"]



try:
    
    subprocess.run(['mongoimport','-d','291db','-c','dblp','--type','json','--file',filename,'--host','localhost','--port',port,'--numInsertionWorkers','10','--drop'])
        
except:
    print("unable to load file into database")


collection.aggregate([
  {"$set": {"year": {"$toString": "$year" } } }]
)
print("converted year to string !")
collection.create_index([("references",1)],name='ref_index')
print("references index created")
collection.create_index([("abstract","text"),("title","text"),("authors","text"),("venue","text"),("year","text")], default_language="none")
print("Collection + Indexes Created")

if ('venues' in db.list_collection_names()):
    venues=db["venues"]
    #venues.delete_many({})
    venues.drop()

collection=db["dblp"]



collection.aggregate(
[
{"$lookup":{"from":"dblp","localField":"id","foreignField":"references", "as":"cited_by"}},
{"$match":{"cited_by":{"$ne":[]}}},
{"$unwind":{"path":"$cited_by"}},
{"$group":{"_id":{"venue":"$venue"},"t_cited":{"$addToSet":"$cited_by._id"}}},
{"$project":{"times_cited":{"$size":"$t_cited"}}},
{"$merge":{"into": "venues"}}
])
print("collection 2 created")





collection.aggregate(
[
{"$group":{"_id":{"venue":"$venue"},"articleCount":{"$sum":1}}},
{"$lookup":{"from":"venues","localField":"_id.venue","foreignField":"_id.venue", "as":"articles_in"}},
{"$match":{"articles_in":{"$ne":[]}}},
{"$project":{"articleCount":1,"articles_in.times_cited":1}},
{"$merge":{"into": "venue_rank"}}
])





print("DONE with Precomputation")



