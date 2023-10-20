from html import entities
from itertools import count
import json
import os
from json.decoder import JSONDecodeError
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

dir_path = os.getenv('INPUT_DIR')
normalRankCount = 0
preferredRankCount = 0
deprecatedRankCount = 0
claimsTotalNumber = 0
totalStatements = 0
noResponseCounter = 0
properties = {}

count = {'Q106466760': 0, 'Q104378399': 0, 'Q27058': 0, 'Q77066609': 0, 'Q7882489': 0, 'Q29998666': 0, 'Q70650920': 0, 'Q744069': 0, 'Q873222': 0, 'Q105769095': 0, 'Q107217620': 0, 'Q22979588': 0, 'Q1434353': 0, 'Q112980637': 0, 'Q106160493': 0, 'Q29485': 0, 'Q840148': 0, 'Q86454040': 0, 'Q18912752': 0, 'Q18603603': 0, 'Q28962310': 0, 'Q60070514': 0, 'Q105675146': 0, 'Q9492': 0, 'Q107356532': 0, 'Q30108381': 0, 'Q30230067': 0, 'Q56644435': 0, 'Q109104929': 0, 'Q6136054': 0, 'Q17949': 0, 'Q357662': 0, 'Q2496920': 0, 'Q4895105': 0, 'Q5432619': 0, 'Q18706315': 0, 'Q54943392': 0, 'Q27055432': 0, 'Q25895909': 0, 'Q35779580': 0, 'Q109012782': 0, 'Q16886573': 0, 'Q54975531': 0, 'Q344495': 0, 'Q20734200': 0, 'Q100349848': 0, 'Q41755623': 0, 'Q701040': 0, 'Q363948': 0, 'Q1255828': 0, 'Q110558700': 0, 'Q880643': 0, 'Q28831311': 0, 'Q37113960': 0, 'Q319141': 0, 'Q17024293': 0, 'Q74524855': 0, 'Q73290844': 0, 'Q11169': 0, 'Q45025362': 0, 'Q32188232': 0, 'Q26162470': 0, 'Q6878417': 0, 'Q3918409': 0, 'Q110290991': 0, 'Q900584': 0, 'Q97161074': 0, 'Q38131096': 0, 'Q59783740': 0, 'Q2478058': 0, 'Q21097088': 0, 'Q21655367': 0, 'Q21818619': 0, 'Q24238356': 0, 'Q224952': 0, 'Q65088633': 0, 'Q108163': 0, 'Q3984452': 0, 'Q50376823': 0, 'Q56685043': 0, 'Q29509080': 0, 'Q791801': 0, 'Q110143752': 0, 'Q21683367': 0, 'Q16868120': 0, 'Q26877139': 0, 'Q41719': 0, 'Q280943': 0, 'Q2132119': 0, 'Q84590041': 0, 'Q28962312': 0, 'Q18122778': 0, 'Q13649246': 0, 'Q26932615': 0, 'Q59864995': 0, 'Q603908': 0, 'Q5727902': 0, 'Q21097017': 0, 'Q748250': 0, 'Q3847033': 0, 'Q24025284': 0, 'unknown': 0}
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for filename in os.listdir(dir_path):
    try:
        f = os.path.join(dir_path, filename)
        with open(f,'r') as f:
            data = json.load(f)
            entities = data['entities']
            for key in entities:
                el = entities[key]
                for claimsId in el['claims']:
                    statement = el['claims'][claimsId]
                    for statementId in el['claims'][claimsId]:
                        qualifiers =el['claims'][claimsId]
                        element = qualifiers.pop()
                        if 'qualifiers' in element:
                            qualifier = element['qualifiers']

                            if 'P5102' in qualifier:
                                for element in qualifier['P5102']:
                                    datavalue = element['datavalue']
                                    if datavalue['value']['id'] in count.keys():
                                        if(claimsId not in properties.keys()): 
                                            toChange = {claimsId: 1} 
                                            properties.update(toChange)
                                        else:
                                            toChange = {claimsId: properties.get(claimsId)+1} 
                                            properties.update(toChange)
                            if 'P1480' in qualifier:
                                for element in qualifier['P1480']:
                                    datavalue = element['datavalue']
                                    if datavalue['value']['id'] in count.keys():
                                        if(claimsId not in properties.keys()): 
                                            toChange = {claimsId: 1} 
                                            properties.update(toChange)
                                        else:
                                            toChange = {claimsId: properties.get(claimsId)+1} 
                                            properties.update(toChange)

    except KeyError:
        print('Key Error')
    except json.JSONDecodeError as err:
        print('Json Decode Error')
    pbar.update(1)

with open(os.getenv('OUTPUT_DIR')+'/propertiesQualifiers.json','w') as outfile:
    outfile.write(json.dumps(properties, indent = 4))
