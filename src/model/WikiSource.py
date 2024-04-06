import requests
import json
import sys
from Entry import *


def search( message ):
    
    print("Searching message: ",message)

    response = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&formatversion=2&srsearch="+message)


    if response.status_code == 200:
        j = response.json()
        #print("Search Info: ",j["query"]["searchinfo"])
        answers = j["query"]["search"]
        finalBit = []
        for answer in answers:
            #print(answer)
            title = "TITLE: "+str(answer["title"])
            pageid = "PAGEID: "+str(answer["pageid"])
            snippet = "SNIPPET: "+str(answer["snippet"])
            finalBit.append({"title":title,"pageid":pageid,"snippet":snippet})
        print(finalBit)
        wr = WikiWrapper(finalBit)
        wr.toCSV()
    
    else:
        print("Error: Query did not work. Status code of: ",response.status_code)
    
n = len(sys.argv)
finalStr = ""
for word in range(1,n-1):
    finalStr += sys.argv[word]+"%20"

finalStr += sys.argv[n-1]
search(finalStr)






