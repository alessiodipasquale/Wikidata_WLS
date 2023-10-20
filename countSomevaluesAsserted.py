from html import entities
import json
import os
from json.decoder import JSONDecodeError
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

dir_path = os.getenv('INPUT_DIR')

errors = 0
directory = './'
normalRankCount = 0
preferredRankCount = 0
deprecatedRankCount = 0
claimsTotalNumber = 0
totalStatements = 0    
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


notAssertedCount = 0
assertedCount = 0
claimsTotalNumber = 0

pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for file in os.listdir(dir_path):
    claimsTotalNumber = 0
    try:     
        with open(dir_path+file,'r') as f:
            data = json.load(f)       
            entities = data['entities']
            for key in entities: 
                el = entities[key]
                for claimsId in el['claims']:
                    statements = el['claims'][claimsId]
                    for elem in statements: 
                        claimsTotalNumber +=1
                        totalStatements += 1
                        mainsnak = elem['mainsnak']

                        if elem['rank'] == 'normal' and mainsnak['snaktype']=='somevalue':
                            if (isAnotherPreferred(elem, statements)):
                                notAssertedCount+=1     
                            else:
                                assertedCount+=1
                        if elem['rank'] == 'preferred' and mainsnak['snaktype']=='somevalue':
                            assertedCount+=1         
                        if elem['rank'] == 'deprecated' and mainsnak['snaktype']=='somevalue':
                            notAssertedCount+=1
        pbar.update(1)
                   
                                
    except KeyError:
        print('Key Error')
        errors += 1
    except JSONDecodeError as err:
        print('Json Decode Error')
        errors += 1

outString = {
        'asserted': assertedCount,
        'notAsserted': notAssertedCount,
        'count':totalStatements
}
json_string = json.dumps(outString)

with open(os.getenv('OUTPUT_DIR')+'/somevaluesAsserted.json','w') as output:
    output.write(json_string)

print("Errors: "+str(errors))