import json
from operator import contains
import requests
from json.decoder import JSONDecodeError
import time
import os
from tqdm import tqdm

properties = {}
counter = 0;
dir_path = "./galaxy/"

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
                            properties.update(toChange)
    except KeyError:
        print('key error')
        #with open('G:/asserted3/errors/rankingsError.txt','a') as errorFile:
            #errorFile.write(file)
    except JSONDecodeError as err:
        print('json error')

totalBlank = 0
#for entityType in entities:
counter = 0
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
                    for elem in statements:
                        mainsnak = elem['mainsnak']
                        if(mainsnak['snaktype']=='novalue' and (claimsId in properties.keys())):  
                            #print(claimsId)
                            toChange = {claimsId: properties.get(claimsId)+1} 
                            properties.update(toChange)
                            totalBlank+=1
    except KeyError:
        print('key error')
        #with open('G:/asserted3/errors/rankingsError.txt','a') as errorFile:
            #errorFile.write(file)
    except JSONDecodeError as err:
        print('json error')
        
print(totalBlank) 
with open('/results/blankCounter.txt') as b:
    b.write(totalBlank)
with open('/results/blankNodes.json','w') as outfile:
    outfile.write(json.dumps(properties, indent = 4))