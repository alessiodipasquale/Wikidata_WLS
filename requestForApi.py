import requests
import json
import os
from tqdm import tqdm
API_ENDPOINT = "https://www.wikidata.org/w/api.php"
i = 0
import os
with open('/home/admin/starFormatted.json','r') as file:
    pbar = tqdm(total=24000)
    line = (file.readline()).rstrip("\n")
    while line:       
        params = {
            'action': 'wbgetentities',
            'format': 'json',
            'ids': line,
            'uselang': 'en'
        }
        if not os.path.exists('/home/admin/stars/stars_'+str(i)+".json"):
            r = requests.get(API_ENDPOINT, params = params)
            with open('/home/admin/stars/stars_'+str(i)+".json", "w") as outfile:
                json.dump(r.json(), outfile, indent = 4)
        i+=1
        pbar.update(1)
        line = (file.readline()).rstrip("\n")
pbar.close()
