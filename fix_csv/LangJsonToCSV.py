import os
import json
import pandas as pd

PATH = os.getcwd()
DICT_FLDR = os.path.join(PATH,'dicts')
test_PATH = os.path.join(DICT_FLDR,'明鏡国語辞典')


#col 0,5 important

#t_path = os.path.join(test_PATH,'term_bank_1.json')

def createDF(f):
    #pretty it up
    df = pd.read_json(f)
    df = df.drop(columns = [i for i in df if i not in [0,5]])
    df.columns = ['Word','Definition']
    for i in range(len(df['Definition'])):
        df['Definition'][i]=df['Definition'][i][0]

    return df

def generateCSV(folder_name,end_name):
    #for file in os.listdir()
    FLDR_DIR = os.path.join(DICT_FLDR,folder_name)
    dfs = []
    for file_name in os.listdir(FLDR_DIR):
        if file_name != 'index.json':
            df = createDF(os.path.join(FLDR_DIR,file_name))
            dfs.append(df)
    combo_df = pd.concat(dfs)
    combo_df.to_csv('{}.csv'.format(end_name),index=False)

def massGenerate():
    for folder_name in os.listdir(DICT_FLDR):
        generateCSV(folder_name = folder_name,end_name=folder_name)

#massGenerate()

