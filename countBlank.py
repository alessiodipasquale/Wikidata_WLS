import json
from operator import contains
from json.decoder import JSONDecodeError
import time
import os
from tqdm import tqdm

properties = {}
novalue = {}
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
                            novalue.update(toChange)
                            properties.update(toChange)
    except KeyError:
        print('key error')
        #with open('G:/asserted3/errors/rankingsError.txt','a') as errorFile:
            #errorFile.write(file)
    except JSONDecodeError as err:
        print('json error')
    pbar.update(1)
totalBlank = 0
#for entityType in entities:
counter = 0
totalProperties = 0
print("Count No Values")
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
                        if(mainsnak['snaktype']=='novalue' and (claimsId in novalue.keys())):  
                            #print(claimsId)
                            toChange = {claimsId: novalue.get(claimsId)+1} 
                            novalue.update(toChange)
                            totalBlank+=1
    except KeyError:
        print('key error')
        #with open('G:/asserted3/errors/rankingsError.txt','a') as errorFile:
            #errorFile.write(file)
    except JSONDecodeError as err:
        print('json error')
    pbar.update(1)
        
print("Blank:"+ str(totalBlank))
print("Properties:"+ str(totalProperties)) 
with open('./results/topCategories/blank.json','w') as outfile:
    outfile.write(json.dumps(novalue, indent = 4))

with open('./results/topCategories/properties.json','w') as outfile:
    outfile.write(json.dumps(properties, indent = 4))