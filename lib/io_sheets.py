from lib.freq_list_csv import FreqList
from lib.import_sheet import GSpreadSheet
from lib.kindle_words import KindleWords
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

###1/5/21

class ReturnedSheet:
    '''Performs operations on the GSpreadSheet. Can add the words from your kindle, just change the kindle path to where your kindle's clippings.txt is located.'''
    def __init__(self,GsheetName,col1,col2,working_dir,resource_path, word_list = ''):

        self.DIR = os.path.dirname(__file__)
        self.RESOURCES = resource_path
        self.KINDLE_PATH = r"E:\documents\My Clippings.txt"
        self.COL_1 = col1
        self.COL_2 = col2
        self.WORD_LIST = word_list
        self.WORKING_DIR = working_dir
        ###get the freq list
        self.FREQ_LIST = os.path.join(self.RESOURCES,'freq_list.csv')
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        #os.chdir(self.DIR)
        creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(self.RESOURCES,"creds.json"),scope)
        #os.chdir(self.WORKING_DIR)
        client = gspread.authorize(creds)
        self.OPENED_SHEET = client.open(GsheetName).sheet1
        self.KINDLE_WORDS = []
        self.RAW_SHEET = GSpreadSheet(GsheetName,self.COL_1,self.COL_2,self.RESOURCES)
        self.DF = {}

    def getKindleWords(self):
        if os.path.exists(self.KINDLE_PATH):
            K = KindleWords(self.KINDLE_PATH)
            K.getWords()
            self.KINDLE_WORDS = K.words_from_kindle

    def GetSheetData(self):
        self.RAW_SHEET.sheetScraper()
        if len(self.KINDLE_WORDS) > 0:
            #recall .addToDict takes a list and adds the words to the dict
            self.RAW_SHEET.addToDict(self.KINDLE_WORDS)
        self.RAW_SHEET.reorderDict()

    def AddToDF(self,word_list):
        self.RAW_SHEET.addToDict(word_list)
    
    def changeToDF(self):
        self.DF = pd.DataFrame(data = self.RAW_SHEET.reordered_d,columns = [self.COL_1,self.COL_2])

    def iter_pd(self,df):
        for val in df.columns:
            yield val
        for row in df.to_numpy():
            for val in row:
                if pd.isna(val):
                    yield ""
                else:
                    yield val

    def pandas_to_sheets(self,pandas_df, clear = True):
        # Updates all values in a workbook to match a pandas dataframe
        if clear:
            self.OPENED_SHEET.clear()
        (row, col) = pandas_df.shape
        cells = self.OPENED_SHEET.range("A1:{}".format(gspread.utils.rowcol_to_a1(row + 1, col)))
        for cell, val in zip(cells, self.iter_pd(pandas_df)):
            cell.value = val
        self.OPENED_SHEET.update_cells(cells) 
    
    def send2Sheets(self):
        self.pandas_to_sheets(self.DF)

    def UpdateSheet(self):
            self.getKindleWords()
            self.AddToDF(self.WORD_LIST)
            self.GetSheetData()
            self.changeToDF()
            self.send2Sheets()

    def saveAsCSV(self,file_path):
        self.DF.to_csv(file_path,index=False)
        

#t = ReturnedSheet("JWordsImmersion",'Word','Frequency',os.path.dirname(__file__))
#t.UpdateSheet()
#t.saveAsCSV()