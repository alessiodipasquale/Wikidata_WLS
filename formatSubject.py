with open('/Users/alessiodipasquale/Projects/TesiWikidata/newAnalysis/spaceTranslated.json','r') as file:

        list_of_entities = str(file.readlines()).split('|')
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
            if x == w:
                result.append(string[0:len(string)-1])
                string = ''
            x += 50
        with open('/Users/alessiodipasquale/Projects/TesiWikidata/newAnalysis/spaceFormatted.json','w') as f: #subjectForAPI
            for r in result:
                f.write(r+'\n')

