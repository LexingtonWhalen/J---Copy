import os
import pandas as pd
from lib.freq_list_csv import FreqList

###1/5/21

class CSVSorter():

    def __init__(self,csv_file,freq_list):
        self.csv_file = csv_file
        #freq_list is a dictionary {'Word':Frequency value}
        self.freq_list = FreqList(freq_list).readFreqList()
    
    def create_df(self):
        '''Used to create the initial frequency df. Must be formatted like in example.csv'''
        self.df = pd.read_csv(self.csv_file)
        self.df['Frequency'].fillna(0,inplace=True)
        

    def sort_by_freq(self):
        #sorts the csv by freq
        for word in self.df['Word']:
            if word in self.freq_list.keys():
                self.df.loc[(self.df['Word'] == word,'Frequency')] = self.freq_list[word]

        self.df= self.df.sort_values(by='Frequency',ascending=False)

    def add_list(self,l):
        '''Adds a list of WORDS (only words!) to your df.
        You must sort afterwords.'''

        for word in l:
            
            try:
                new_row = {'Word':word,'Frequency':self.freq_list[word]}
            except KeyError:
                #couldnt find the work in the freq list
                new_row={'Word':word,'Frequency':0}

            self.df = self.df.append(new_row,ignore_index=True)
            #get only unique words
            self.df.drop_duplicates(subset=['Word'],inplace=True)

    def create_csv(self,name):
        '''Creates a csv file. Add .csv to the name to work.'''
        self.df.to_csv(index=False,encoding = 'utf-8',path_or_buf='{}'.format(name))


        

#test = CSVSorter('tester.csv','freq_list.csv')
#test.create_df()
#test.add_list(['扁平','地中'])
#test.sort_by_freq()
#print(test.df)
#test.create_csv('tester1.csv')
