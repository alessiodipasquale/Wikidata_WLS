from html import entities
import json
import os
from json.decoder import JSONDecodeError
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

dir_path = os.getenv('INPUT_DIR')

directory = './'
normalRankCount = 0
preferredRankCount = 0
deprecatedRankCount = 0
claimsTotalNumber = 0
totalStatements = 0
noResponseCounter = 0
counter=0

elements = {}

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
                            counter+=1 
    except KeyError:
            noResponseCounter+=1
    except JSONDecodeError as err:
            noResponseCounter+=1
    pbar.update(1)

data = sorted(elements.items(), key = lambda item: item[1], reverse=True)

json_string = json.dumps(data)
with open(os.getenv('OUTPUT_DIR')+'/reasonOfDeprecation.json','w') as output:
    output.write(json_string)
