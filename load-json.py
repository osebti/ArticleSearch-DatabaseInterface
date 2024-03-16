from pymongo import MongoClient
import os

class DatabaseAccess:
    def __init__(self, port):
        self.port = port
        self.client = MongoClient('localhost', self.port)
        self.db = self.client['291db']
        if ('dblp' in self.db.list_collection_names()):
            # self.coll = self.db["dblp"]
            #self.db.collection.drop()  
            print("dropped")
        self.coll = self.db["dblp"]

    def setupCollection(self):
        self.coll.update_many({}, {"$set" : {"times_cited": 1}})
        for article in self.coll.find():
            self.coll.update_one(article, {"$set": {"year":str(article["year"])} })
            print("Reached")
            self.cursor = self.coll.find({"references":article["title"]})
            self.length = len(self.cursor)
            self.coll.update(article,{"$set":{"times_cited":self.length}})
    
    def addFile(self, file):
        comm_dir = r'"C:\Program Files\MongoDB\Tools\100\bin\mongoimport.exe"'
        # comm_dir = 'mongoimport'
        command = f'{comm_dir} --db 291db --collection dblp --drop --port 22102 --file {file} --batchSize 1000'
        os.system(command)
        self.coll.drop_indexes()
        self.coll.create_index([("authors", "text"), ("abstract", "text"), ("title", "text"), ("venue", "text"), ("year", "text"), ("references", "text")])

class Application(DatabaseAccess):
    def __init__(self, filename, port):
        super().__init__(port)
        self.filename = filename
        #self.addFile(self.filename)
        #self.setupCollection()
    
    def mainUI(self):
        while True:
            print("\nWelcome")
            print("1: Search for Articles")
            print("2: Search for authors")
            print("3: List the venues")
            print("4: Add an article")
            print("E: Exit\n")
            option = input("Enter your option: ")

            if option == '1':
                keywords = input("Enter your keyword/s: ")
                self.searchArticle(keywords)
            elif option.upper() == 'E':
                quit()
    
    @staticmethod
    def existCheck(dictionary, key):
        try:
            return dictionary[key]
        except:
            return ""

    def searchArticle(self, keywords):
        matches = {}
        search_resultsIndex = []
        search_results = []
        results = []
        keywords = keywords.split()
        for i in range(len(keywords)):
            keywords[i] = f'\"{keywords[i]}\"'
        results = self.coll.find({"$text": {"$search": " ".join(keywords)}})
        self.searchView(results)

    def searchView(self, results):
        lower_bound = 0
        upper_bound = 5
        r_length = len(list(results.clone()))
        remaining = r_length
        print(remaining)
        while True:
            print("______________________________________________________\n")
            for i in range(lower_bound, upper_bound):
                if i < r_length:
                    print(f'{i}: {results[i]["title"]}')
            print("______________________________________________________\n")
            
            while True:
                print("Press [A] to select an article")
                if remaining > 5:
                    print("Press [B] to show more results")
                print("Press [E] to go back to the main menu")
                option = input("Enter: ")
                if option.upper() == 'A':
                    while True:
                        a_no = input("Select an article number: ")
                        if a_no.isdigit() and int(a_no) < r_length:
                            self.viewSelect(results[int(a_no)])
                            break
                elif option.upper() == 'B' and remaining > 5:
                    lower_bound += 5
                    upper_bound += 5
                    remaining -= 5
                    break
                elif option == 'E':
                    return
                else:
                    continue
    
    def viewSelect(self, article):
        print(f'\nArticle ID: {article["id"]}')
        print(f'Title: {article["title"]}')
        print(f'Year: {article["year"]}')
        print(f'Author/s: {" ".join(article["author"])}')
        print(f'Abstract: {Application.existCheck(article, "abstract")}')
        print(f'No. of times cited: {article["n_citations"]}')
        print(f'Venue: {article["venue"]}')
        print(f'References: {Application.existCheck(article, "references")}')
        print("\n")

class searchArticle(DatabaseAccess):
    def __init__(self, port):
        super().__init__(port)

if __name__ == "__main__":
    filename = input("Enter filename: ")
    port = input("Enter port number: ")
    run = Application(filename, int(port))
    run.mainUI()