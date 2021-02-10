###Created by Lex Whalen

import os
import pandas as pd


class FreqList:
    #assumesCSV
    #returns a df of the frequency list.
    def __init__(self, ref_file):
        self.ref_file = ref_file

    def readFreqList(self):
        orig = pd.read_csv(self.ref_file)
        df = orig
        df.columns = ['Word','Frequency']
        words = [i for i in df['Word']]
        freq = [i for i in df['Frequency']]
        d = dict(zip(words,freq))
        return d





