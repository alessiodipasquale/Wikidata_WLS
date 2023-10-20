from html import entities
import json
import os
from json.decoder import JSONDecodeError
from tqdm import tqdm
import sys
from dotenv import load_dotenv

load_dotenv()

dir_path = os.getenv('INPUT_DIR')

directory = './'
normalRankCount = 0
preferredRankCount = 0
deprecatedRankCount = 0
claimsTotalNumber = 0
totalStatements = 0
errorCounter = 0

result = {}
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for file in os.listdir(dir_path):
    try:
        with open(dir_path+file,'r') as f:
            data = json.load(f)               
            entities = data['entities']
            for key in entities:
                el = entities[key]
                for claimsId in el['claims']:
                    if(claimsId == 'P162'):
                        print(el)
                        statement = el['claims'][claimsId]
                        for elem in statement:
                           mainsnak = elem['mainsnak']
                           if(mainsnak['snaktype']=='novalue'):
                                result = el
                                with open(os.getenv('OUTPUT_DIR')+'/search.json','w') as output:
                                    output.write(json.dumps(result, indent = 4))
                                sys.exit()
        pbar.update(1)
    except KeyError:
            print('KeyError')
            errorCounter+=1
    except JSONDecodeError as err:
            print('JSONDecodeError')
            errorCounter+=1
 
