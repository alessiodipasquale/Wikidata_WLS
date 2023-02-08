import json
import os
from tqdm import tqdm

dir_path = 'E:/wikidata-debate/visual_heritage/'
pbar = tqdm(total=len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
for file in os.listdir(dir_path):
	try:     
		with open(dir_path+file,'r') as f:
			with open('E:/wikidata-debate/visual_heritage_reduced/'+file,'w') as outfile:
				file = json.load(f)
				outfile.write(json.dumps(file,separators=(',', ':')))
	except json.JSONDecodeError as err:
		print(file)
	pbar.update(1)
