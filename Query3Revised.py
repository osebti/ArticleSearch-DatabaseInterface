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
find_result=dblp.find({},{'references':1,'_id':0})

idList=[]
agg_result_venue=[]
agg_result_num=[]
referenceList=[]
TimesBeenReferencedList=[]

for x in agg_result:
    agg_result_venue.append(x["_id"])
    agg_result_num.append(x["num"])
    TimesBeenReferencedList.append(0)
for x in find_result:
    if(x!={}):
        for items in x["references"]:
            referenceList.append(items)
agg_result1=dblp.aggregate([
 {"$match" : {"id" : {"$in" : referenceList}}},
 {"$group" : {"_id" : "$venue", "referencedTime" : {"$sum" : 1}}}

 ])
for x in agg_result1:
    tem2=x["_id"]
    for i in range(len(agg_result_venue)):
        tem=agg_result_venue[i]
        if (tem==tem2):
            TimesBeenReferencedList[i]=TimesBeenReferencedList[i]+x["referencedTime"]


for i in range(len(TimesBeenReferencedList)):
    for j in range(0,len(TimesBeenReferencedList)-i-1):
        if(TimesBeenReferencedList[j]<TimesBeenReferencedList[j+1]):
            TimesBeenReferencedList[j],TimesBeenReferencedList[j+1]=TimesBeenReferencedList[j+1],TimesBeenReferencedList[j]
            agg_result_venue[j],agg_result_venue[j+1]=agg_result_venue[j+1],agg_result_venue[j]
            agg_result_num[j],agg_result_num[j+1]=agg_result_num[j+1],agg_result_num[j]
print("How many venues do you want to see?")
howmany=input()
Ahowmany=int(howmany)
if(Ahowmany>len(agg_result_venue)):
    print("There are not that much venues, but here is all of them")
    for i in range(len(agg_result_num)):
        print("No."+ str(i+1),end=' ')
        print("Venue Type: ",end='')
        print(agg_result_venue[i], end='')
        print(" Times been referenced: ",end='')
        print(TimesBeenReferencedList[i],end='')
        print(" Num of articles in that Venue: ", end='')
        print(agg_result_num[i])
else:
    for i in range(Ahowmany):
        print("No."+ str(i+1),end=' ')
        print("Venue Type: ",end='')
        print(agg_result_venue[i], end='')
        print(" Times been referenced: ",end='')
        print(TimesBeenReferencedList[i],end='')
        print(" Num of articles in that Venue: ", end='')
        print(agg_result_num[i])
