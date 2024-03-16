from pymongo import MongoClient
import json 
client = MongoClient('mongodb://localhost:27017')
db = client["291db"]
dblp = db["dblp"]

agg_result= dblp.aggregate(
[{
"$group" : 
    {"_id" : "$venue", 
        "num" : {"$sum" : 1}
        }}
])
agg_result1=db.dblp.aggregate([
{"$group": { "_id": "$venue", "totalcit": { "$sum": "$n_citation" } }},
{"$sort": {
  "totalcit": -1
}}
])

agg_result_venue=[]
agg_result_num=[]
agg_result1_venue=[]
agg_result1_totalcit=[]

for x in agg_result1:
    agg_result1_venue.append(x["_id"])
    agg_result1_totalcit.append(x["totalcit"])
for x in agg_result:
    agg_result_venue.append(x["_id"])
    agg_result_num.append(x["num"])

# for x in agg_result1:
#     for items in agg_result:
#         if(x["_id"]==items["_id"]):
#             print(x["_id"],end=' ')
#             print(x["totalcit"],end=' ')
#             print(items["num"])
#             break
print("How many venues do you want to see?")
howmany=input()
Ahowmany=int(howmany)
if(Ahowmany>len(agg_result1_venue)):
    print("There are not that much venues, but here is all of them")
    for i in range(len(agg_result1_venue)):
        for j in range(len(agg_result_venue)):
            if(agg_result_venue[j]==agg_result1_venue[i]):
                print("No."+str(i+1),end=' ')
                print("Venue name: ",end=' ')
                print(agg_result_venue[j],end=' ')
                print("  Total times been referenced: ",end=' ')
                print(agg_result1_totalcit[i],end=' ')
                print("  Total articles in that venue: ",end=' ')
                print(agg_result_num[j])
else:
    for i in range(Ahowmany):
        for j in range(len(agg_result_venue)):
            if(agg_result_venue[j]==agg_result1_venue[i]):
                print("No."+str(i+1),end=' ')
                print("Venue name: ",end=' ')
                print(agg_result_venue[j],end=' ')
                print("  Total times been referenced: ",end=' ')
                print(agg_result1_totalcit[i],end=' ')
                print("  Total articles in that venue: ",end=' ')
                print(agg_result_num[j])