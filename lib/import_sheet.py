###Created by Lex Whalen

from lib.freq_list_csv import FreqList
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

#list of dictionaries with Word: word, Frequency:number
#data = sheet.get_all_records() -> returns a list of dictionaries:
#-> in form [{'Word': '扁平', 'Frequency': 687}, {'Word': '地中', 'Frequency': 625}]


##### to do -> change everything to df, don't need regular dictionaries. Also, can just use the df sorting method
class GSpreadSheet:
    def __init__(self, sheetName,column,values,resource_path):
        self.dir = os.path.dirname(__file__)
        self.resources = resource_path
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(self.resources,"creds.json"),self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(sheetName).sheet1
        self.data = self.sheet.get_all_records()
        self.column = column #this is where the words are held
        self.values = values
        self.freq_list = os.path.join(self.resources,'freq_list.csv')
        self.d = {}
        self.reordered_d = {}
        self.freq_d = FreqList(self.freq_list).readFreqList()

    def sheetScraper(self):
        total = len(self.data)
        for i in range(total):
            if self.data[i][self.column] != '':
                if self.data[i][self.values] == '':
                    #if I forget to put a zero next to a word in excel that I don't know the freq
                    self.d[self.data[i][self.column]] = 0
                else:
                    self.d[self.data[i][self.column]] = self.data[i][self.values]
    def addToDict(self,word_list):
        for i in word_list:
            self.d[i] = 0

    def reorderDict(self):
        #rearranges self.d by self.freqlist
        for word in self.d:
            if self.d[word] == 0:
                if word in self.freq_d:
                    self.d[word] = self.freq_d[word]
        self.reordered_d = sorted(self.d.items(),key=lambda x:int(x[1]),reverse=True)








