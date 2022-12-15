from html import entities
import json
import os
from json.decoder import JSONDecodeError
from tqdm import tqdm

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

directory = './'
normalRankCount = 0
preferredRankCount = 0
deprecatedRankCount = 0
claimsTotalNumber = 0
totalStatements = 0
errorCounter = 0
elements = {}
properties = {}
notAssertedCount = 0
assertedCount = 0

dir_path = "./pop/"
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
    pbar.update(1)


print("Ranking and Reason of Deprecation")
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for file in os.listdir(dir_path):
    try:
        with open(dir_path+file,'r') as f:
            data = json.load(f)               
            entities = data['entities']
            for key in entities:
                el = entities[key]
                for claimsId in el['claims']:
                    statement = el['claims'][claimsId]
                    for elem in statement:
                        claimsTotalNumber +=1
                        totalStatements += 1
                        if elem['rank'] == 'normal':
                            normalRankCount +=1
                            if (isAnotherPreferred(elem, statements)):
                                notAssertedCount+=1     
                            else:
                                assertedCount+=1
                        if elem['rank'] == 'preferred':
                            preferredRankCount +=1  
                            assertedCount+=1         
                        if elem['rank'] == 'deprecated':
                            deprecatedRankCount +=1
                            notAssertedCount+=1 
                            if elem['rank'] == 'deprecated' and ("P2241" in elem["qualifiers-order"]):
                                for qualifier in elem['qualifiers']:
                                    if(qualifier == "P2241"):
                                        noval = elem['qualifiers'][qualifier]
                                        qualifier = noval[0]['datavalue']['value']['id']
                                        if(qualifier not in elements):
                                            toChange = {qualifier: 1} 
                                            elements.update(toChange)
                                        else:
                                            toChange = {qualifier: elements.get(qualifier)+1}
                                            elements.update(toChange) 
                        mainsnak = elem['mainsnak']
                        if(mainsnak['snaktype']=='novalue' and (claimsId in properties.keys())):  
                            #print(claimsId)
                            toChange = {claimsId: properties.get(claimsId)+1} 
                            properties.update(toChange)

 
    except KeyError:
            print('KeyError')
            errorCounter+=1
    except JSONDecodeError as err:
            print('JSONDecodeError')
            errorCounter+=1
    pbar.update(1)
    
outString = {
    'normal': normalRankCount,
    'preferred': preferredRankCount,
    'deprecated':deprecatedRankCount,
    'count':claimsTotalNumber
}
json_string = json.dumps(outString)
with open('./resultspop/ranking.json','w') as output:
    output.write(json_string)

data = sorted(elements.items(), key = lambda item: item[1], reverse=True)

json_string = json.dumps(data)
with open('./resultspop/reasonOfDeprecation.json','w') as output:
    output.write(json_string)

with open('/resultspop/blankNodes.json','w') as outfile:
    outfile.write(json.dumps(properties, indent = 4))

outString = {
        'asserted': assertedCount,
        'notAsserted': notAssertedCount,
        'count':claimsTotalNumber
}
json_string = json.dumps(outString)
with open('./resultspop/asserted.json','w') as output:
    output.write(json_string)
