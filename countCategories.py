#import the libraries
import json
import os
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

categories = {}
 
#iterate to find all the P31
dir_path = os.getenv('INPUT_DIR') 
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for file in os.listdir(dir_path):
    try:     
        with open(dir_path+file,'r') as f:
            data = json.load(f)       
            entities = data['entities']
            for key in entities: 
                el = entities[key]
                for claimsId in el['claims']: 
                    if(claimsId == "P31"):
                        statements = el['claims'][claimsId]
                        for statement in statements:
                            datavalue = statement['mainsnak']['datavalue']['value']
                            if datavalue['id'] in categories.keys():
                                toChange = {datavalue['id']: categories.get(datavalue['id'])+1 }
                            else:
                                toChange = {datavalue['id']: 1 }
                            categories.update(toChange)
    except KeyError:
        print('Key Error')
    except json.JSONDecodeError as err:
        print('Json Decode Error')
    pbar.update(1)

#sort the dictionary
datas = sorted(categories.items(), key = lambda item: item[1], reverse=True)

with open(os.getenv('OUTPUT_DIR')+'/categories.json','w') as output:
     output.write(json.dumps(datas, indent = 4))