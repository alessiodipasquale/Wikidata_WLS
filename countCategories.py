import json
import os
from tqdm import tqdm

categories = {}
 
dir_path = "C:/Users/aless/Desktop/topCategories/topCategories/"
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for file in os.listdir(dir_path):
    try:     
        with open(dir_path+file,'r') as f:
            data = json.load(f)       
            entities = data['entities']
            for key in entities: #entità Q
                el = entities[key]
                for claimsId in el['claims']: #proprietà P
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
        print('key error')
    except json.JSONDecodeError as err:
        print('json error')
    pbar.update(1)

    
datas = sorted(categories.items(), key = lambda item: item[1], reverse=True)

with open('./results/topCategories/categories.json','w') as output:
     output.write(json.dumps(datas, indent = 4))