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
            
            title = "TITLE: "+str(answer["trackName"])
            nameid = "PAGEID: "+str(answer["trackId"])
            description = "SNIPPET: "+" artist name: "+str(answer["artistName"])+"\nn track name: "+str(answer["trackName"])+"\n release date: "+str(answer["releaseDate"])

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

