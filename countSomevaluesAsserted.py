from html import entities
import json
import os
from json.decoder import JSONDecodeError
from tqdm import tqdm

errors = 0
directory = './'
normalRankCount = 0
preferredRankCount = 0
deprecatedRankCount = 0
claimsTotalNumber = 0
totalStatements = 0
dir_path = "C:/Users/aless/Desktop/datasetJournal/galaxy_reduced/galaxy_reduced/"

#f = open('G:/tipi.json')
#data = json.loads(f.read())    
noResponseCounter = 0
def isAnotherNormal(this,list):
    for elem in list:
        if(elem['rank'] == 'normal'  and elem != this):
                return True

def isAnotherDeprecated(this,list):
    for elem in list:
        if(elem['rank'] == 'deprecated'  and elem != this):
                return True

def isAnotherPreferred(this,list):
    for elem in list:
        if(elem['rank'] == 'preferred' and elem != this):
                return True


#for elem in data:
notAssertedCount = 0
assertedCount = 0
claimsTotalNumber = 0
    #typeString=elem['type']
    #entity = str(typeString.replace('http://www.wikidata.org/entity/',''))
    #print(entity) 
    #if not os.path.exists('G:/asserted3/'+entity+'.json'):
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for file in os.listdir(dir_path):
    claimsTotalNumber = 0
    #if file.startswith(entity+'.json'):
    try:     
        with open(dir_path+file,'r') as f:
        #with open('C:/Users/aless/Desktop/Tesi/asserted/input/input.json','r') as f:
            data = json.load(f)       
            entities = data['entities']
            for key in entities: #entità Q
                el = entities[key]
                for claimsId in el['claims']: #proprietà P
                    statements = el['claims'][claimsId]
                    for elem in statements: #elem è il singolo statement, statements tutti, fissata la P di sopra
                        claimsTotalNumber +=1
                        totalStatements += 1
                        mainsnak = elem['mainsnak']

                        if elem['rank'] == 'normal' and mainsnak['snaktype']=='somevalue':
                            if (isAnotherPreferred(elem, statements)):
                                notAssertedCount+=1     
                            else:
                                assertedCount+=1
                        if elem['rank'] == 'preferred' and mainsnak['snaktype']=='somevalue':
                            assertedCount+=1         
                        if elem['rank'] == 'deprecated' and mainsnak['snaktype']=='somevalue':
                            notAssertedCount+=1
        pbar.update(1)
                   
                                
    except KeyError:
        print('error')
        errors += 1
        #with open('G:/asserted3/errors/rankingsError.txt','a') as errorFile:
            #errorFile.write(file)
    except JSONDecodeError as err:
        print('error')
        errors += 1
        #with open('G:/asserted3/errors/rankingsError.txt','a') as errorFile:
            #   errorFile.write(file)

outString = {
        'asserted': assertedCount,
        'notAsserted': notAssertedCount,
        'count':totalStatements
}
json_string = json.dumps(outString)
with open('C:/Users/aless/Desktop/Wikidata_WLS/results/somevalues/asserted/galaxy.json','w') as output:
    output.write(json_string)

print("Errors: "+str(errors))