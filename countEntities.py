#import libraries
from html import entities
import json
import os
from json.decoder import JSONDecodeError
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

errors = 0
dir_path = os.getenv('INPUT_DIR') 
total = 0
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
#iterate to count all the entities
for file in os.listdir(dir_path):
    try:     
        with open(dir_path+file,'r') as f:
            data = json.load(f)       
            entities = data['entities']
            total += len(entities)
        pbar.update(1)
                                                  
    except KeyError:
        print(file)
        errors += 1
    except JSONDecodeError as err:
        print(file)
        errors += 1

outString = {
        'entities': total,
}
json_string = json.dumps(outString)
with open(os.getenv('OUTPUT_DIR')+'/entities.json','w') as output:
    output.write(json_string)

print("Errors: "+str(errors))