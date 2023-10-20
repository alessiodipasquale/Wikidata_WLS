# import required module
import os
import json
from tqdm import tqdm
from dotenv import load_dotenv
# load .env file
load_dotenv()
# open json file
with open(os.getenv('INPUT_JSON_FILE'), 'r') as jsonFile: 
    data = json.load(jsonFile)
    pbar = tqdm(total=len(data))
    i = 1
    # iterate through the json list
    for elem in data:
        pbar.update(1)       
        #replace http://www.wikidata.org/entity/ with empty string 
        entity = str(elem['item'].replace('http://www.wikidata.org/entity/','')) + '|'
        i+=1
        #write to output file
        with open(os.getenv('OUTPUT_DIR')+'/subjects.json', 'a') as f:
            f.write(entity)
pbar.close()