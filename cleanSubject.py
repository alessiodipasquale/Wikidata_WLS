# import required module
import os
import json
import sys
from tqdm import tqdm
# assign directory

with open('/Users/alessiodipasquale/Projects/TesiWikidata/newAnalysis/galaxy.json', 'r') as jsonFile: 
    data = json.load(jsonFile)
    pbar = tqdm(total=len(data))
    outputDirectory = '/Users/alessiodipasquale/Projects/TesiWikidata/newAnalysis/galaxyTranslated.json'
    i = 1
    for elem in data:
        pbar.update(1)        
        entity = str(elem['item'].replace('http://www.wikidata.org/entity/','')) + '|'
        i+=1
        with open(outputDirectory, 'a') as f:
            f.write(entity)
pbar.close()