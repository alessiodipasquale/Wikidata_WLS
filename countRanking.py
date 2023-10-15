from html import entities
import json
import os
from json.decoder import JSONDecodeError
from tqdm import tqdm

directory = './'
normalRankCount = 0
preferredRankCount = 0
deprecatedRankCount = 0
claimsTotalNumber = 0
totalStatements = 0
errorCounter = 0

dir_path = "C:/Users/aless/Desktop/topCategories/topCategories/"

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
                        if elem['rank'] == 'preferred':
                            preferredRankCount +=1        
                        if elem['rank'] == 'deprecated':
                            deprecatedRankCount +=1 
        pbar.update(1)
    except KeyError:
            print('KeyError')
            errorCounter+=1
    except JSONDecodeError as err:
            print('JSONDecodeError')
            errorCounter+=1
    
outString = {
    'normal': normalRankCount,
    'preferred': preferredRankCount,
    'deprecated':deprecatedRankCount,
    'count':claimsTotalNumber
}
json_string = json.dumps(outString)
with open('C:/Users/aless/Desktop/Wikidata_WLS/results/topCategories/ranking.json','w') as output:
    output.write(json_string)

print('Total Statements: '+str(totalStatements))
print('Errors: '+str(errorCounter))