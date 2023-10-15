import json
from operator import contains
from json.decoder import JSONDecodeError
import time
import os
from tqdm import tqdm

properties = {}
somevalue = {}
counter = 0
dir_path = "C:/Users/aless/Desktop/topCategories/topCategories/"

#getAllProperties

print("Get all properties")
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for file in os.listdir(dir_path):
    try:     
        with open(dir_path+file,'r') as f:
            data = json.load(f)       
            entities = data['entities']
            for key in entities: #entità Q
                el = entities[key]
                for claimsId in el['claims']: #proprietà P
                    statements = el['claims'][claimsId]
                    for elem in statements:
                        mainsnak = elem['mainsnak']
                        if(claimsId not in properties.keys()): 
                            toChange = {claimsId: 0} 
                            somevalue.update(toChange)
                            properties.update(toChange)
    except KeyError:
        print('key error')
        #with open('G:/asserted3/errors/rankingsError.txt','a') as errorFile:
            #errorFile.write(file)
    except JSONDecodeError as err:
        print('json error')
    pbar.update(1)
totalSomevalues = 0
#for entityType in entities:
counter = 0
totalProperties = 0
print("Count Somevalues")
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for file in os.listdir(dir_path):
    try:     
        with open(dir_path+file,'r') as f:
            data = json.load(f)       
            entities = data['entities']
            for key in entities: #entità Q
                el = entities[key]
                for claimsId in el['claims']: #proprietà P
                    statements = el['claims'][claimsId]
                    toChange = {claimsId: properties.get(claimsId)+len(statements)}
                    totalProperties += len(statements) 
                    properties.update(toChange)
                    for elem in statements:
                        mainsnak = elem['mainsnak']
                        if(mainsnak['snaktype']=='somevalue' and (claimsId in somevalue.keys())):  
                            #print(claimsId)
                            toChange = {claimsId: somevalue.get(claimsId)+1} 
                            somevalue.update(toChange)
                            totalSomevalues+=1
    except KeyError:
        print('key error')
        #with open('G:/asserted3/errors/rankingsError.txt','a') as errorFile:
            #errorFile.write(file)
    except JSONDecodeError as err:
        print('json error')
    pbar.update(1)
        
print("Somevalues:"+ str(totalSomevalues))
print("Properties:"+ str(totalProperties)) 
with open('./results/topCategories/somevalues.json','w') as outfile:
    outfile.write(json.dumps(somevalue, indent = 4))

#with open('C:/Users/aless/Desktop/newresults/properties/visual.json','w') as outfile:
#    outfile.write(json.dumps(properties, indent = 4))