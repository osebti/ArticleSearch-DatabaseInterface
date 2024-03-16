from pymongo import MongoClient

global c
c=MongoClient() # change this later to the right value 
global db
db=c["291db"]
global table
table=db["dblp"]
global venues
venues=db["venues"]



def mainMenu():
    while(True):
        print("\n\n----------- MAIN MENU -----------\n")
        print("-- PRESS 1 TO SEARCH FOR ARTICLE -- ") # user selection prompts
        print("-- PRESS 2 TO SEARCH FOR AUTHOR -- ")
        print("-- PRESS 3 TO LIST TOP VENUES -- ")
        print("-- PRESS 4 TO ADD AN ARTICLE -- ")
        print("-- PRESS 5 TO EXIT --")
        opt=input("\n Press Here: ")

        try: # sanity check 
            opt=int(opt)
        except:
            print("\nInvalid input")

        if(opt==1): # parsing unit block that binds input to function
            searchArticle()
        elif(opt==2):
            searchAuthor()
        elif(opt==3):
            listVenues()
        elif(opt==4):
            addArticle()
        elif(opt==5): # exit program with exit() if input = 5
            print("\n ----- Program Ending Now -----")
            exit()
        else:
            print("\nInvalid option")
             


def addArticle():
    global c,db,table
    print("Fill in the following details to add the article:\n") # input prompts
    id=str(input("id: "))
    title=str(input("Title: "))
    authors=str(input("Authors (seperated by one comma and space): "))
    year=str(input("Year: "))
    references=[]
    try:
        temp=int(year)
        authors=authors.split(", ")
    except:
        print("Invalid Input") # return to menu if sanity check fails
        return

    if table.find_one({"id":id})==None:
        dict={"authors":authors,"id":id,"title":title,"year":year,"references":references,"n_citations":0,"abstract":None,"venue":None}
    
        try:
            table.insert_one(dict)
        except:
            print(" -- Unable to add new article\n")
    else:
        print("-- id provided is not unique\n\n")
    return 




def searchArticle():
    author=str(input("search for an article: "))

    author=author.strip()
    author=author.split()
    search=""
    for word in author:
        search+='"'+word+'"' + " "
    search.strip()
    
    cur=table.find({"$text":{"$search":search}},
                   {"_id":0})

    i=1
    array=[]
    for result in cur:
        array.append(result["id"])
        print(i,end=": ")
        print("id: "+str(result["id"]) + " || Title: "+ str(result["title"])+ " || Year: "+ str(result["year"])+ " || Venue: "+ str(result["venue"])+"\n")
        i+=1

    selection=input("type the a valid row number to select an article or press anything else to return\n Select here: ")
    if len(selection.split())>1: # checking length of input 
        return
    try:
        selection=int(selection)
    except:
        return
    if(selection<=len(array) and selection>0):
        print("\nArticle Information:")
        try:
            print("Abstract: "+str(result["abstract"]+"\n"))
        except:
            print("No Abstract")
        try:
            print("Authors: "+ str(result["authors"]))
        except:
            print("No Authors")
        article_id=str(array[selection-1])
        print("\nReferenced by the following articles:\n")
        cur=table.find(
            {"references":article_id},
            {"id":1,"title":1,"year":1}
            )
        for article in cur:
            print("id: " + str(article["id"]) + " || Title: "+ str(article["title"])+ " || Year: "+ str(article["year"]))
            print("\n")





def selectAuthor(author:str): # takes in author name 
    cur=table.find( {"authors":author}).sort("year")
    
    print("\nAuthor Articles:")
    for result in cur:
        print("title: "+ str(result["title"]) + " year: " + str(result["year"])+ " venue: " + str(result["venue"])+"\n")
    print("\n")
    return 
    


def searchAuthor():
    author=str(input("Search for an author: "))
    author=author.strip()
    search= '\\b' + author + '\\b'
    
    
    cur=table.aggregate(pipeline=
    [
    {"$match":{"$text": {"$search":author}}},
    {"$unwind":"$authors"},
    {"$match":{"authors":{"$regex":search,"$options":"i"}}},
    {"$group": { "_id": "$authors", "num_publications":{"$sum":1}}}
    ])

    i=1
    array=[]
    for result in cur:
        array.append(result)
        print(i,end=": ")
        print(result)
        i+=1

    selection=input("-- Type the a valid row number to select author OR press anything else to return: ")
    if len(selection.split())>1: # checking length of input 
        return
    try:
        selection=int(selection)
    except:
        return

    if(selection<=len(array) and selection>0):
        selectAuthor(array[selection-1]["_id"])
        return




def listVenues():
    n=input("Select number of top venues you would like to see: ")
    if len(n.split())>1:
        print("invalid input")
        return

    try:
        n=int(n)
        if(n<=0 or n>venues.count_documents({})):
            print("Invalid input: number selected is either negative or too large \n")
            return

    except:
        print("Invalid input\n")
        return

    v_rank=db['venue_rank']
    top_venues=v_rank.find({"_id.venue":{"$ne":""}}).sort("articles_in.times_cited",-1).limit(n)
    print("Top venues:")
    for venue in top_venues:
        print(venue)
    return


mainMenu()
