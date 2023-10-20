import requests
import json
import os
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

input_file = os.getenv('INPUT_JSON_FILE')
API_ENDPOINT = "https://www.wikidata.org/w/api.php"
i = 0
import os
with open(input_file,'r') as file:
    pbar = tqdm(total=60001)
    line = (file.readline()).rstrip("\n")
    while line:       
        params = {
            'action': 'wbgetentities',
            'format': 'json',
            'ids': line,
            'uselang': 'en'
        }
        if not os.path.exists(os.getenv('OUTPUT_DIR')+'/random_'+str(i)+".json"):
            r = requests.get(API_ENDPOINT, params = params)
            with open(os.getenv('OUTPUT_DIR')+'random_'+str(i)+".json", "w") as outfile:
                json.dump(r.json(), outfile, indent = 4)
        i+=1
        pbar.update(1)
        line = (file.readline()).rstrip("\n")
pbar.close()
