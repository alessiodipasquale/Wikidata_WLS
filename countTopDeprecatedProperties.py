import json
import os
from tqdm import tqdm

properties = {}
 
dir_path = "E:/wikidata-debate/visual_heritage_reduced/"
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
                            toChange = {claimsId: len(statements)} 
                            properties.update(toChange)
                    for elem in statements:
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

    
with open('C:/Users/aless/Desktop/newresults/otherAnalysis/propertiesDeprecated/visual.json','w') as output:
    output.write(json.dumps(properties, indent = 4))