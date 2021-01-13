import csv

###1/5/21

class KindleWords:

    def __init__(self,path):
        self.path = path
        self.words_from_kindle = []
    
    def getWords(self):
        with open(self.path, 'r',encoding = 'utf8') as file:
            raw_text = [line for line in file]
            for index, block in enumerate(raw_text):
                if '===' in block:
                    #index-1 gives the word
                    if raw_text[index-1] != '\n':
                        self.words_from_kindle.append(raw_text[index-1].split('\n')[0])
                
