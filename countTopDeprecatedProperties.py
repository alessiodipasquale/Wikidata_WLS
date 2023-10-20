import json
import os
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

dir_path = os.getenv('INPUT_DIR')

properties = {}

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
                    if(claimsId not in properties.keys()): 
                            toChange = {claimsId: 0} 
                            properties.update(toChange)
                    for elem in statements:
                        if elem['rank'] == 'deprecated':
                            toChange = {claimsId: properties.get(claimsId)+1} 
                            properties.update(toChange)
    except KeyError:
        print('Key Error')
    except json.JSONDecodeError as err:
        print('Json Decode Error')
    pbar.update(1)

    
with open(os.getenv('OUTPUT_DIR')+'/propertiesDeprecated.json','w') as output:
    output.write(json.dumps(properties, indent = 4))