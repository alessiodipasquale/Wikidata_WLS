import json
import os
from tqdm import tqdm
errors = 0
directory = './'
normalRankCount = 0
preferredRankCount = 0
deprecatedRankCount = 0
claimsTotalNumber = 0
totalStatements = 0

#f = open('G:/tipi.json')
#data = json.loads(f.read())    
noResponseCounter = 0
def isAnotherNormal(this,list):
    for elem in list:
        if(elem['rank'] == 'normal'  and elem != this):
                return True

def isAnotherDeprecated(this,list):
    for elem in list:
        if(elem['rank'] == 'deprecated'  and elem != this):
                return True

def isAnotherPreferred(this,list):
    for elem in list:
        if(elem['rank'] == 'preferred' and elem != this):
                return True

properties = {}
assertedProperties = {}
dir_path = "E:/wikidata-debate/stars_reduced/"
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
                    if(claimsId not in properties.keys()): 
                            toChange = {claimsId: 0} 
                            properties.update(toChange)
                    if(claimsId not in assertedProperties.keys()): 
                            toChange = {claimsId: 0} 
                            assertedProperties.update(toChange)
                    for elem in statements:
                        if elem['rank'] == 'normal':
                            if (isAnotherPreferred(elem, statements)):
                                toChange = {claimsId: properties.get(claimsId)+1} 
                                properties.update(toChange)   
                            else:
                                toChange = {claimsId: assertedProperties.get(claimsId)+1} 
                                assertedProperties.update(toChange)    
                        if elem['rank'] == 'preferred':
                            toChange = {claimsId: assertedProperties.get(claimsId)+1} 
                            assertedProperties.update(toChange)          
                        if elem['rank'] == 'deprecated':
                            toChange = {claimsId: properties.get(claimsId)+1} 
                            properties.update(toChange) 
    except KeyError:
        print('key error')
        #with open('G:/asserted3/errors/rankingsError.txt','a') as errorFile:
            #errorFile.write(file)
    except json.JSONDecodeError as err:
        print('json error')
    pbar.update(1)

    
with open('C:/Users/aless/Desktop/newresults/otherAnalysis/propertiesNotAsserted/stars.json','w') as output:
    output.write(json.dumps(properties, indent = 4))

with open('C:/Users/aless/Desktop/newresults/otherAnalysis/propertiesAsserted/stars.json','w') as output:
    output.write(json.dumps(assertedProperties, indent = 4))