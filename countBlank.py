# import libraries
import json
from operator import contains
from json.decoder import JSONDecodeError
import time
import os
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# initialize variables
properties = {}
novalue = {}
counter = 0
dir_path = os.getenv('INPUT_DIR') 

#iterate to get all properties
print("Get all properties")
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for file in os.listdir(dir_path):
    try:     
        with open(dir_path+file,'r') as f:
            data = json.load(f)       
            entities = data['entities']
            for key in entities: 
                el = entities[key]
                for claimsId in el['claims']: 
                    statements = el['claims'][claimsId]
                    for elem in statements:
                        mainsnak = elem['mainsnak']
                        if(claimsId not in properties.keys()): 
                            toChange = {claimsId: 0} 
                            novalue.update(toChange)
                            properties.update(toChange)
    except KeyError:
        print('key error')
    except JSONDecodeError as err:
        print('json error')
    pbar.update(1)

totalBlank = 0
counter = 0
totalProperties = 0

print("Count No Values")
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
#iterate to count all novalue
for file in os.listdir(dir_path):
    try:     
        with open(dir_path+file,'r') as f:
            data = json.load(f)       
            entities = data['entities']
            for key in entities: 
                el = entities[key]
                for claimsId in el['claims']: 
                    statements = el['claims'][claimsId]
                    toChange = {claimsId: properties.get(claimsId)+len(statements)}
                    totalProperties += len(statements) 
                    properties.update(toChange)
                    for elem in statements:
                        mainsnak = elem['mainsnak']
                        if(mainsnak['snaktype']=='novalue' and (claimsId in novalue.keys())):  
                            toChange = {claimsId: novalue.get(claimsId)+1} 
                            novalue.update(toChange)
                            totalBlank+=1
    except KeyError:
        print('Key Error')
    except JSONDecodeError as err:
        print('Json Decode Error')
    pbar.update(1)
        
print("Blank:"+ str(totalBlank))
print("Properties:"+ str(totalProperties)) 
with open(os.getenv('OUTPUT_DIR')+'/novalue.json','w') as outfile:
    outfile.write(json.dumps(novalue, indent = 4))

with open(os.getenv('OUTPUT_DIR')+'/properties.json','w') as outfile:
    outfile.write(json.dumps(properties, indent = 4))