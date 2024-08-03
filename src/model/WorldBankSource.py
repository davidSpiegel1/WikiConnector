# Will be a string of world bank information
import requests
import sys 
import json
from Entry import *

def search (query):
    print("Query we are looking for: ",query)


    response = requests.get("https://datacatalogapi.worldbank.org/ddhxext/Search?qname=dataset&qterm="+query+"&format=json")

    print("The response: ",response)
    if response.status_code  == 200:

        j = response.json()
        #print("Json data: ",j)
        r= j["Response"]
        v = r["value"]
        title = ""
        nameId = ""
        description = ""
        finalBit = []
        count = 158
        for cur in v:
            #for i in cur:
            #print(cur['identification'])   
            title = "TITLE: "+str(cur['identification']['title'])
            pageid = "PAGEID: "+str(cur['identification']['id'])
            snippet = "SNIPPET: "+str(cur['identification']['description'])
            finalBit.append({"title":title,"pageid":count,"snippet":snippet})
            count += 96

        print(finalBit)
        wr = WorldBankWrapper(finalBit)
        wr.toCSV()
            #print(cur["name"])
            #print(cur["description"])
            #p = cur["identification"]
            #for i in p:
            #    print(i)
        #count = r["odata.count"]
        #for i in r:
        #print(r['odata.count'])

n = len(sys.argv)
finalStr = ""
for word in range(1,n-1):
    finalStr += sys.argv[word]+"+"
finalStr += sys.argv[n-1]
search(finalStr)
