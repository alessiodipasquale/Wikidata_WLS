from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

input_file = os.getenv('INPUT_JSON_FILE')
with open(input_file,'r') as file:
        list_of_entities = str(file.readlines()).split('|')

        pbar = tqdm(total=len(list_of_entities))

        if list_of_entities[0][0] == '[':
            list_of_entities[0] = list_of_entities[0][2:]
        if list_of_entities[len(list_of_entities)-1][-1] == ']':
            list_of_entities[len(list_of_entities)-1] = list_of_entities[len(list_of_entities)-1][:-2]
        string = ''
        result = []

        x = 50
        w = 0
        while w < len(list_of_entities):
            while w < x:
                if w < len(list_of_entities):
                    string += str(list_of_entities[w]+'|')
                w += 1
                pbar.update(1)
            if x == w:
                result.append(string[0:len(string)-1])
                string = ''
            x += 50

        with open(os.getenv('OUTPUT_JSON_FILE'),'w') as f:
            for r in result:
                f.write(r+'\n')

