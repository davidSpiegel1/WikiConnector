#  https://itunes.apple.com/search?term=jack+johnson


import requests
import json
import sys
from Entry import *

def search( message ):

    print("What the message is", message)



    response = requests.get("https://itunes.apple.com/search?format=json&term="+message)


    if response.status_code == 200:
        j = response.json()
        n = j["resultCount"]
        print("Result Count: ",n)
        r = j["results"]
        title = ""
        nameid = ""
        description = ""
        finalBit = []

        for answer in r:
            print("Entry: ",answer)
            if "trackName" in answer:
                title = "TITLE: "+str(answer["trackName"])
            else:
                title = "TITLE: ERR. NOT FOUND"
            if "trackId" in answer:
                nameid = "PAGEID: "+str(answer["trackId"])
            else:
                nameid = "PAGEID: ERR. NOT FOUND"
            if "artistName" in answer and "releaseDate" in answer and "trackName" in answer:
                description = "SNIPPET: "+" artist name: "+str(answer["artistName"])+"\nn track name: "+str(answer["trackName"])+"\n release date: "+str(answer["releaseDate"])
            else:
                description = "SNIPPET: ERR. NOT FOUND"

            finalBit.append({"title":title.replace(",",""),"pageid":nameid.replace(",",""),"snippet":description.replace(",","")})
        print(finalBit)
        wr = AppleMusicWrapper(finalBit)
        wr.toCSV()
        
    #print(x.text)


n = len(sys.argv)
finalStr = ""
for word in range(1,n-1):
    finalStr += sys.argv[word]+"+"
finalStr += sys.argv[n-1]
search(finalStr)

