from html import entities
import json
import os
from json.decoder import JSONDecodeError
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

dir_path = os.getenv('INPUT_DIR')

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

errorJsonCounter = 0
errorKeyCounter = 0

elements = {}
propertiesNovalue = {}
propertiesSomevalue = {}
somevaluesWithReason = {}

deprecatedSomevalues = {}
notAssertedCount = 0
assertedCount = 0

notAssertedSomevalues = 0
AssertedSomevalues = 0
countSomevalues = 0

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
                        if(claimsId not in propertiesNovalue.keys()): 
                            toChange = {claimsId: 0} 
                            propertiesNovalue.update(toChange)
                        if(claimsId not in propertiesSomevalue.keys()): 
                            toChange = {claimsId: 0} 
                            propertiesSomevalue.update(toChange)
    except KeyError:
        print('Key Error')
    except JSONDecodeError as err:
        print('Json Decode Error')
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
                        mainsnak = elem['mainsnak']
                        if elem['rank'] == 'normal':
                            normalRankCount +=1
                            if (isAnotherPreferred(elem, statements)):
                                notAssertedCount+=1
                                if mainsnak['snaktype']=='somevalue':
                                    notAssertedSomevalues+=1
                                    countSomevalues+=1     
                            else:
                                assertedCount+=1
                                if mainsnak['snaktype']=='somevalue':
                                    AssertedSomevalues+=1
                                    countSomevalues+=1     
                        if elem['rank'] == 'preferred':
                            preferredRankCount +=1  
                            assertedCount+=1    
                            if mainsnak['snaktype']=='somevalue':
                                    AssertedSomevalues+=1 
                                    countSomevalues+=1     
                        if elem['rank'] == 'deprecated':
                            deprecatedRankCount +=1
                            notAssertedCount+=1
                            if mainsnak['snaktype']=='somevalue':
                                notAssertedSomevalues+=1 
                            if elem['rank'] == 'deprecated' and ("P2241" in elem["qualifiers-order"]):
                                if mainsnak['snaktype']=='somevalue':
                                    if(claimsId not in somevaluesWithReason):
                                        toChange = {claimsId: 1} 
                                        somevaluesWithReason.update(toChange)
                                    else:
                                        toChange = {claimsId: somevaluesWithReason.get(claimsId)+1}
                                        somevaluesWithReason.update(toChange)

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
                            if(mainsnak['snaktype']=='somevalue' and elem['rank'] == 'deprecated'):  
                                if(claimsId not in deprecatedSomevalues):
                                    toChange = {claimsId: 1} 
                                    deprecatedSomevalues.update(toChange)
                                else:
                                    toChange = {claimsId: deprecatedSomevalues.get(claimsId)+1}
                                    deprecatedSomevalues.update(toChange)
                        if(mainsnak['snaktype']=='novalue' and (claimsId in propertiesNovalue.keys())):  
                            toChange = {claimsId: propertiesNovalue.get(claimsId)+1} 
                            propertiesNovalue.update(toChange)

                        if(mainsnak['snaktype']=='somevalue' and (claimsId in propertiesSomevalue.keys())):  
                            toChange = {claimsId: propertiesSomevalue.get(claimsId)+1} 
                            propertiesSomevalue.update(toChange)

 
    except KeyError:
            print('KeyError')
            errorKeyCounter+=1
    except JSONDecodeError as err:
            print('JSON Decode Error')
            errorJsonCounter+=1
    pbar.update(1)
    
outString = {
    'normal': normalRankCount,
    'preferred': preferredRankCount,
    'deprecated':deprecatedRankCount,
    'count':claimsTotalNumber
}

outError = {
    'jsonError': errorJsonCounter,	
    'keyError': errorKeyCounter
}

jsonErr_string = json.dumps(outError)
with open(os.getenv('OUTPUT_DIR')+'errors.json','w') as output:
    output.write(jsonErr_string)

json_string = json.dumps(outString)
with open(os.getenv('OUTPUT_DIR')+'ranking.json','w') as output:
    output.write(json_string)

data = sorted(elements.items(), key = lambda item: item[1], reverse=True)

json_string = json.dumps(data)
with open(os.getenv('OUTPUT_DIR')+'reasonOfDeprecation.json','w') as output:
    output.write(json_string)

with open(os.getenv('OUTPUT_DIR')+'blankNodes.json','w') as outfile:
    outfile.write(json.dumps(propertiesNovalue, indent = 4))

    
with open(os.getenv('OUTPUT_DIR')+'somevalues.json','w') as outfile:
    outfile.write(json.dumps(propertiesSomevalue, indent = 4))

dataSomevalues = sorted(deprecatedSomevalues.items(), key = lambda item: item[1], reverse=True)

json_string1 = json.dumps(dataSomevalues)
with open(os.getenv('OUTPUT_DIR')+'somevaluesWithDeprecation.json','w') as output:
    output.write(json_string1)

outString = {
        'asserted': assertedCount,
        'notAsserted': notAssertedCount,
        'count':claimsTotalNumber
}
json_string = json.dumps(outString)
with open(os.getenv('OUTPUT_DIR')+'asserted.json','w') as output:
    output.write(json_string)


outString1 = {
        'asserted': AssertedSomevalues,
        'notAsserted': notAssertedSomevalues,
        'count':assertedCount
}
json_string2 = json.dumps(outString1)
with open(os.getenv('OUTPUT_DIR')+'assertedSomevalues.json','w') as output:
    output.write(json_string2)

data = sorted(somevaluesWithReason.items(), key = lambda item: item[1], reverse=True)

json_string3 = json.dumps(data)
with open(os.getenv('OUTPUT_DIR')+'somevaluesWithReason.json','w') as output:
    output.write(json_string3)