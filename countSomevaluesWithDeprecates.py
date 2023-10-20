import json
from operator import contains
from json.decoder import JSONDecodeError
import time
import os
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

dir_path = os.getenv('INPUT_DIR')

properties = {}
somevalue = {}
counter = 0

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
                            somevalue.update(toChange)
                            properties.update(toChange)
    except KeyError:
        print('Key Error')
    except JSONDecodeError as err:
        print('Json Decode Error')
    pbar.update(1)

totalSomevalues = 0
counter = 0
totalProperties = 0

print("Count Somevalues with deprecated")
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
                    toChange = {claimsId: properties.get(claimsId)+len(statements)}
                    totalProperties += len(statements) 
                    properties.update(toChange)
                    for elem in statements:
                        mainsnak = elem['mainsnak']
                        if(mainsnak['snaktype']=='somevalue' and (claimsId in somevalue.keys()) and elem['rank'] == 'deprecated'):  
                            toChange = {claimsId: somevalue.get(claimsId)+1} 
                            somevalue.update(toChange)
                            totalSomevalues+=1
    except KeyError:
        print('Key Error')
    except JSONDecodeError as err:
        print('Json Decode Error')
    pbar.update(1)
        
print("Somevalues with deprecated:"+ str(totalSomevalues))
print("Total Statements:"+ str(totalProperties)) 
with open(os.getenv('OUTPUT_DIR')+'/somevaluesDeprecated.json','w') as outfile:
    outfile.write(json.dumps(somevalue, indent = 4))