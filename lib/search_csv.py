###Created by Lex Whalen

import pandas as pd
import os

class SingleDict():
    #is a single csv dictionary turned into a pd dataframe.
    def __init__(self,csv_path,file_name):
        self.file_name = file_name
        self.csv_folder = csv_path
        self.df = None

        #initiate the df
        self.initialize()

    def initialize(self):
        self.addDF()

    def addDF(self):
        df = pd.read_csv(os.path.join(self.csv_folder,self.file_name))
        self.df = df
    
    def search(self, query):
        #note the csv must be in form "Word" "Definition"
        results = self.df[self.df['Word'] == query]['Definition'].tolist()
        if results:
            return results

class MasterDict():
    #holds each separate df in in a dictionary
    def __init__(self,csv_folder,dict_list):
        self.df_dict = {}
        self.csv_folder=csv_folder
        self.dict_list = dict_list
    
    def initialize(self):
        self.massAdd()

    def add_DF_to_dict(self,csv_file_name):
        #adds a single entry of form {'csv_name': df object}
        file_dir = os.path.join(self.csv_folder,csv_file_name)
        self.df_dict[csv_file_name.split('.csv')[0]] = SingleDict(self.csv_folder,file_dir)

    def massAdd(self):
        #loops through the files in dict_list and adds them to the self.df_dict
        #for file_name in os.listdir(self.csv_folder):
        #    self.add_DF_to_dict(file_name)
        for file_name in self.dict_list:
            #check that the files is .csv
            if (os.path.splitext(file_name)[1] == '.csv'):
                self.add_DF_to_dict(file_name)
            else:
                raise TypeError("Dictionaries must be .csv.")
    
    def massSearch(self,query):
        #returns list of lists
        #ex: [['J Dict Name','result1'],[,]...]
        results_list = []
        for key in self.df_dict:
            query_result = self.df_dict[key].search(query=query)
            if query_result:
                results_list.append([key,query_result])
        return results_list

