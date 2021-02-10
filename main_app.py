###Created by Lex Whalen

from tkinter import *
import tkinter as tk
from tkinter import messagebox,filedialog
import os
from datetime import datetime

from lib.search_csv import SingleDict,MasterDict
from lib.kindle_words import KindleWords
from lib.freq_list_csv import FreqList
from lib.import_sheet import GSpreadSheet
from lib.io_sheets import ReturnedSheet
from lib.sort_and_create import CSVSorter

###1/5/21

###TO DO
#**** ADD LANGUAGE SPECIFIC BUTTONS/ text
#**** ADD METHOD TO GET RID OF WORD IN LIST
#**** MAKE PRETTY
#make resizeable
#add sounds

class App():
    def __init__(self):

        #paths and important directories
        self.PATH = os.getcwd()
        self.RESOURCES = os.path.join(self.PATH,'resources')
        self.LANGUAGES_FLDR = os.path.join(self.RESOURCES,'languages')
        self.MAIN_SETTINGS_TXT = os.path.join(self.RESOURCES,'main_settings.txt')
        self.MAIN_SETTINGS_DICT = {}

        #for opening settings files
        def read_settings(f,delimiter,out_dict):
            with open(f,encoding='utf8') as file:
                for line in file:
                    if line[0] != '\n':
                        #print(line.rstrip('\n').split(':'))
                        setting,entry = line.rstrip('\n').split(':')
                        out_dict[setting] = entry
        
        #read the MAIN_SETTINGS_TXT:
        read_settings(self.MAIN_SETTINGS_TXT,':',self.MAIN_SETTINGS_DICT)

        #identify the language and its settings
        self.SELECTED_LANG = self.MAIN_SETTINGS_DICT['lang']
        self.SELECTED_LANG_FLDR = os.path.join(self.LANGUAGES_FLDR,self.SELECTED_LANG)
        self.SELECTED_LANG_SETTINGS_TXT = os.path.join(self.SELECTED_LANG_FLDR,'settings.txt')
        self.FREQ_LIST_CSV = os.path.join(self.SELECTED_LANG_FLDR,'freq_list.csv')

        #read the LANG_SETTINGS_TXT:
        self.SELECTED_LANG_SETTINGS_DICT = {}
        read_settings(self.SELECTED_LANG_SETTINGS_TXT,':',self.SELECTED_LANG_SETTINGS_DICT)

        #load language specific content
        self.LANG_RESOURCES = os.path.join(self.LANGUAGES_FLDR,self.SELECTED_LANG)
        
        self.IMAGES = os.path.join(self.LANG_RESOURCES,'images')
        self.CSV_DICT_FOLDER = os.path.join(self.LANG_RESOURCES,'dict_csv_folder')
        self.USER_CSV_FOLDER = os.path.join(self.LANG_RESOURCES,'user_csv_folder')
        self.USER_CSV_BACKUPS = os.path.join(self.USER_CSV_FOLDER,'csv_backups')

        self.GSPREAD_BACKUPS = os.path.join(self.LANG_RESOURCES,'gspread_backup_folder')
        self.GSPREAD_REQS = os.path.join(self.LANG_RESOURCES,'gspread_reqs')

        #get the last available csv file for use in sort csv button
        self.LAST_CSV_BACKUP = [os.path.join(self.USER_CSV_FOLDER,i) for i in os.listdir(self.USER_CSV_FOLDER) if os.path.splitext(i)[1]=='.csv'].pop()
        
        #list of unknown words we add to google sheets
        self.UNKNOWNS = []

        #for the selected dictionaries
        self.SELECTED_DICTS = []

        #images
        self.TOP_BAR_IMG = os.path.join(self.IMAGES,'top_bar_img.png')

        ###colors
        self.DARK = self.MAIN_SETTINGS_DICT['dark']
        self.WHITE = self.MAIN_SETTINGS_DICT['white']
        self.WIN_BG = self.SELECTED_LANG_SETTINGS_DICT['win_bg']
        self.SIDE_FRAME_BG = self.SELECTED_LANG_SETTINGS_DICT['side_frame_bg']
        self.TITLE_FRAME_BG = self.SELECTED_LANG_SETTINGS_DICT['title_frame_bg']
        self.SEARCH_FRAME_BG = self.SELECTED_LANG_SETTINGS_DICT['search_frame_bg']
        self.SEARCH_RESULTS_BG = self.SELECTED_LANG_SETTINGS_DICT['search_results_bg']
        self.UTIL_FRAME_BG = self.SELECTED_LANG_SETTINGS_DICT['util_frame_bg']
        self.SELECTED_WORDS_BG = self.SELECTED_LANG_SETTINGS_DICT['selected_words_bg']

        #window
        self.WIN_WIDTH = int(self.MAIN_SETTINGS_DICT['win_width'])
        self.WIN_HEIGHT = int(self.MAIN_SETTINGS_DICT['win_height'])
        self.WIN_GEO = "{}x{}".format(self.WIN_WIDTH,self.WIN_HEIGHT)
        self.WIN = Tk()
        self.WIN.geometry(self.WIN_GEO)
        self.WIN.title("{}".format(self.SELECTED_LANG_SETTINGS_DICT["win_title"]))
        self.TOP_BAR_IMG = PhotoImage(file=self.TOP_BAR_IMG)
        self.WIN.iconphoto(False,self.TOP_BAR_IMG)
        self.WIN.configure(background = self.WIN_BG)

        ###specifics to text and messageboxes
        self.FONT_NAME = self.SELECTED_LANG_SETTINGS_DICT['font_name']
        self.ERROR_TITLE = self.SELECTED_LANG_SETTINGS_DICT['error_title']
        self.WARNING_TITLE = self.SELECTED_LANG_SETTINGS_DICT['warning_title']

        ####This is the part that contains the buttons and stuff related to searching words. The main frame.
        self.SIDE_FRAME_WIDTH = int(self.MAIN_SETTINGS_DICT['side_frame_width']) 
        self.SIDE_FRAME_HEIGHT = int(self.MAIN_SETTINGS_DICT['side_frame_height'])
        self.SIDE_FRAME = Frame(self.WIN,width=self.SIDE_FRAME_WIDTH,height=self.SIDE_FRAME_HEIGHT)
        self.SIDE_FRAME.place(relx = 0,rely=0,anchor = NW)
        self.SIDE_FRAME.config(background=self.SIDE_FRAME_BG)

        #title frame
        self.TITLE_FRAME_WIDTH = int(self.MAIN_SETTINGS_DICT['title_frame_width'])
        self.TITLE_FRAME_HEIGHT = int(self.MAIN_SETTINGS_DICT['title_frame_height'])
        self.TITLE_FRAME = Frame(self.SIDE_FRAME,width=self.TITLE_FRAME_WIDTH,height=self.TITLE_FRAME_HEIGHT)
        self.TITLE_FRAME.place(relx=0.5,y=50,anchor = CENTER)
        self.TITLE_FRAME.config(background = self.TITLE_FRAME_BG)
        title_label = Label(self.TITLE_FRAME,text='{}'.format(self.SELECTED_LANG_SETTINGS_DICT['lang_title']))
        title_label.config(background = self.TITLE_FRAME_BG,font=(self.FONT_NAME,20))
        title_label.place(relx=0.5,rely=0.5,anchor = CENTER)

        #search box frame
        SEARCH_FRAME_HEIGHT = self.MAIN_SETTINGS_DICT['search_box_height']
        SEARCH_FRAME_WIDTH = self.TITLE_FRAME_WIDTH
        self.SEARCH_FRAME = Frame(self.SIDE_FRAME,width=SEARCH_FRAME_WIDTH,height = SEARCH_FRAME_HEIGHT)
        self.SEARCH_FRAME.place(relx=0.5,y=140,anchor = CENTER)
        self.SEARCH_FRAME.config(background = self.SEARCH_FRAME_BG)

        #search results frame
        #this is the middle box frame that contains both the added dictionary
        #frame and the actual text frame.
        SEARCH_MAIN_FRAME_HEIGHT = self.MAIN_SETTINGS_DICT['search_main_frame_height']
        SEARCH_MAIN_FRAME_WIDTH = self.TITLE_FRAME_WIDTH
        self.SEARCH_MAIN_FRAME= Frame(self.SIDE_FRAME,height = SEARCH_MAIN_FRAME_HEIGHT,width=SEARCH_MAIN_FRAME_WIDTH)
        self.SEARCH_MAIN_FRAME.place(relx = 0.5,y=350,anchor = CENTER)
        self.SEARCH_MAIN_FRAME.config(background =self.SEARCH_RESULTS_BG,borderwidth=2)
        
        #search text frame
        #this is the frame that shows the results of the dictionaries.
        #you can scroll in this guy
        self.SEARCH_RESULTS_FRAME_HEIGHT = self.MAIN_SETTINGS_DICT['search_results_frame_height']
        self.SEARCH_RESULTS_FRAME_WIDTH = self.TITLE_FRAME_WIDTH*0.9
        self.SEARCH_RESULTS_TEXT_FRAME = Frame(self.SEARCH_MAIN_FRAME,height=self.SEARCH_RESULTS_FRAME_HEIGHT,width=self.SEARCH_RESULTS_FRAME_WIDTH)
        self.SEARCH_RESULTS_TEXT_FRAME.place(relx=0.5,y=130,anchor = CENTER)
        self.SEARCH_RESULTS_TEXT_FRAME.config(background = self.SELECTED_LANG_SETTINGS_DICT['search_results_frame_bg'])

        #added dictionaries:
        AD_HEIGHT = self.MAIN_SETTINGS_DICT['added_dicts_height']
        AD_WIDTH = self.SEARCH_RESULTS_FRAME_WIDTH
        self.ADDED_DICTS_BG = self.SELECTED_LANG_SETTINGS_DICT['added_dicts_bg']
        self.ADDED_DICTS_FRAME = Frame(self.SEARCH_MAIN_FRAME,height=AD_HEIGHT,width=AD_WIDTH)
        self.ADDED_DICTS_FRAME.place(relx=0.5,y=275,anchor = CENTER)
        self.ADDED_DICTS_FRAME.config(background = self.ADDED_DICTS_BG,borderwidth=2)

        #utility frame
        UTIL_FRAME_HEIGHT = self.MAIN_SETTINGS_DICT['util_frame_height']
        UTIL_FRAME_WIDTH = self.TITLE_FRAME_WIDTH
        self.UTIL_FRAME = Frame(self.SIDE_FRAME,height = UTIL_FRAME_HEIGHT,width = UTIL_FRAME_WIDTH)
        self.UTIL_FRAME.place(relx=0.5,y=640,anchor = CENTER)
        self.UTIL_FRAME.config(background = self.UTIL_FRAME_BG,borderwidth=15)

        #selected words list
        SELECTED_WORDS_HEIGHT = self.MAIN_SETTINGS_DICT['selected_words_height']
        SELECTED_WORDS_WIDTH = self.MAIN_SETTINGS_DICT['selected_words_width']
        self.SELECTED_WORDS = Frame(self.UTIL_FRAME,height=SELECTED_WORDS_HEIGHT,width=SELECTED_WORDS_WIDTH)
        self.SELECTED_WORDS.place(relx = 0.6, anchor=NW)
        self.SELECTED_WORDS.config(background = self.SELECTED_WORDS_BG)

    def initialize(self):

        #initiate widgets
        self.searchBox()
        self.searchButton()
        self.initializeDictsButton()
        self.addToSheetsButton()
        self.updateSheetButton()
        self.searchHistory()
        self.darkModeButton()
        self.updateCSVButton()
        self.dictStats()

        #for motion of mouse
        #self.WIN.bind('<Motion>',self.motion)

        #this has to be at the end
        self.WIN.mainloop()

    ###WIDGETS###
    ###widgets in form: widgetWidget

    def dictStats(self):
        dictionary_count = Label(self.ADDED_DICTS_FRAME,
        text='{lang_text}: {count}'.format(lang_text=self.SELECTED_LANG_SETTINGS_DICT['dict_stats_text'],count=len(self.SELECTED_DICTS)))

        dictionary_count.config(background=self.ADDED_DICTS_BG,font=(self.FONT_NAME,10),fg='white')
        dictionary_count.place(x=10,y=0)

    def searchBox(self):
        SEARCH_BOX_WIDTH = self.TITLE_FRAME_WIDTH *.78
        SEARCH_BOX_HEIGHT = self.MAIN_SETTINGS_DICT['search_box_heigth']
        SEARCH_BOX_BORDER = 2
        SEARCH_BOX_X = self.TITLE_FRAME_WIDTH-5
        SEARCH_LABEL_WIDTH = self.MAIN_SETTINGS_DICT['search_label_width']
        
        self.SEARCH_BOX = Entry(self.SEARCH_FRAME,borderwidth = SEARCH_BOX_BORDER,relief=FLAT)
        self.SEARCH_BOX.place(x=SEARCH_BOX_X,y=5, bordermode = OUTSIDE,height = SEARCH_BOX_HEIGHT, 
        width = SEARCH_BOX_WIDTH,anchor=NE)

        sb0 = self.SELECTED_LANG_SETTINGS_DICT['search_box_bg0']
        sb1 = self.SELECTED_LANG_SETTINGS_DICT['search_box_bg1']
        self.change_color_on_entry_frame(self.SEARCH_BOX,sb1,sb0)
        self.SEARCH_BOX.bind("<Return>",lambda e: self.click_search())

        search_box_txt =self.SELECTED_LANG_SETTINGS_DICT['search_box_text']
        search_label = Label(self.SEARCH_FRAME,text='{}:'.format(search_box_txt),borderwidth=2,relief=FLAT)
        search_label.place(x=5,y=5, height = SEARCH_BOX_HEIGHT,width = SEARCH_LABEL_WIDTH)
        search_label.config(font=(self.FONT_NAME,10))

    def searchHistory(self):
        ###put the selection text on the bottom right
        ###within the UTIL FRAME
        history_label_txt = self.SELECTED_LANG_SETTINGS_DICT['search_history_text']
        history_label = Label(self.SELECTED_WORDS,text=history_label_txt,width=int(self.SIDE_FRAME_WIDTH * 3/5) -10)
        history_label.place(relx=0.5,rely=0.1,anchor=CENTER)
        bg = self.SELECTED_LANG_SETTINGS_DICT['search_history_label_bg']
        history_label.config(font=(self.FONT_NAME,10),background=bg)

    def searchButton(self):
        ##TO DO:
        #connect the x pos of the button to that of the search box
        SEARCH_BUTTON_X = self.MAIN_SETTINGS_DICT['search_button_x']
        SEARCH_BUTTON_Y = self.MAIN_SETTINGS_DICT['search_button_y']

        search_button_txt = self.SELECTED_LANG_SETTINGS_DICT['search_button_text']
        self.SEARCH_BUTTON = Button(self.SEARCH_FRAME,text = search_button_txt,command = self.click_search,relief =RIDGE,cursor = 'pirate')
        self.SEARCH_BUTTON.place(x=SEARCH_BUTTON_X,y = SEARCH_BUTTON_Y)
        self.SEARCH_BUTTON.config(font=(self.FONT_NAME,8))

        bg0 = self.SELECTED_LANG_SETTINGS_DICT['search_button_bg0']
        bg1 = self.SELECTED_LANG_SETTINGS_DICT['search_button_bg1']
        self.change_color_on_entry_frame(self.SEARCH_BUTTON,bg1,bg0)

    def initializeDictsButton(self):

        def initializeDicts():
            #clear any remaining dicts
            self.SELECTED_DICTS.clear()

            for i in self.get_chosen_file(self.CSV_DICT_FOLDER):
                selected_file = os.path.split(i)[1]
                if os.path.splitext(selected_file)[1] == '.csv':
                    self.SELECTED_DICTS.append(selected_file)
                else:
                    self.SELECTED_DICTS.clear()
                    self.error_message(self.ERROR_TITLE,"An invalid file type was added. Only .csv is allowed.")
            try:
                if len(self.SELECTED_DICTS) > 0:
                    #try to initialize the new ones
                    self.master_dict = MasterDict(self.CSV_DICT_FOLDER,self.SELECTED_DICTS)
                    self.master_dict.initialize()
                    self.dictStats()
            except TypeError:
                self.error_message(self.ERROR_TITLE,"Not a .csv file extension")
            
        self.INITIALIZE_DICTS_BUTTON = Button(self.UTIL_FRAME,text='Choose dictionaries?',command=initializeDicts)
        self.INITIALIZE_DICTS_BUTTON.place(y=90,width=self.TITLE_FRAME_WIDTH/2)

    def addToSheetsButton(self):
        self.ADD_TO_SHEETS_BUTTON = Button(self.UTIL_FRAME,text='Add list to sheets?',command=lambda: self.add_to_sheets(clean=False),cursor='exchange')
        self.ADD_TO_SHEETS_BUTTON.place(width=self.TITLE_FRAME_WIDTH/2)

    def updateSheetButton(self):
        ###update the google sheets without adding words
        ###use just to clean up
        self.UPDATE_SHEET_BUTTON = Button(self.UTIL_FRAME,text='Update w/o words?',command = lambda:self.add_to_sheets(clean=True))
        self.UPDATE_SHEET_BUTTON.place(y=30,width=self.TITLE_FRAME_WIDTH/2,anchor=NW)

    def darkModeButton(self):
        ###dark mode on/off
        '''honestly this button is just to show that it can work. Idk if I would really use it'''
        self.DARK_MODE_BUTTON = Button(self.UTIL_FRAME,text='BG (Dark/Light)',command=self.dark_mode_on_off)
        self.DARK_MODE_BUTTON.place(y=60,width=self.TITLE_FRAME_WIDTH/2,anchor=NW)

    def updateCSVButton(self):
        self.UPDATE_CSV_BUTTON = Button(self.UTIL_FRAME,text='Update CSV?',command=self.update_csv)
        self.UPDATE_CSV_BUTTON.place(y=120,width=self.TITLE_FRAME_WIDTH/2,anchor=NW)

    #####ACTIONS#####
    ###all actions in form action_action

    def update_csv(self):
        new_path = '{path}\{name}.csv'.format(path=self.USER_CSV_FOLDER
        ,name='my_csv')

        CSVSort = CSVSorter(self.LAST_CSV_BACKUP,self.FREQ_LIST_CSV)
        CSVSort.create_df()
        CSVSort.add_list(self.UNKNOWNS)
        CSVSort.sort_by_freq()
        CSVSort.create_csv("{}".format(new_path))
        self.show_info('File Location','The file is located:\n\n{}.'.format(new_path))
        


    def dark_mode_on_off(self):
        
        color = ''
        if self.WIN["bg"] == self.DARK:
            color = self.WHITE
        else:
            color = self.DARK
        self.WIN.configure(background = color)

    def click_search(self):
        LAST_SEARCH_X = 125
        LAST_SEARCH_Y = 35
        WAIT_TIME = 1200

        self.user_input = self.SEARCH_BOX.get()
        ###last_search
        last_search = Label(self.SEARCH_FRAME,
        text = '{search_txt}: {query} '.format(search_txt=self.SELECTED_LANG_SETTINGS_DICT['search_box_text'],query=self.user_input),
        relief = RIDGE,anchor='w',width=20)

        last_search.place(x=LAST_SEARCH_X,y=LAST_SEARCH_Y)
        bg = self.SELECTED_LANG_SETTINGS_DICT['click_search_bg']
        last_search.config(background=bg,font=(self.FONT_NAME,10))
        #get rid of label
        last_search.after(WAIT_TIME,lambda: last_search.destroy())

        ###search result
        self.search_dictionaries(self.user_input)

    def search_dictionaries(self,query):
        #note RESULT RETURNS A LIST OF LISTS
        try:
            results_list = self.master_dict.massSearch(query)
            if len(results_list) == 0:
                self.error_message(self.ERROR_TITLE,'No results found.')
                try:
                    self.askSelectionButton.destroy()
                except:
                    pass
            else:
                self.print_dict_to_frame(results_list)
                ###add to unknowns
                self.askSelectionButton = Button(self.SEARCH_FRAME,text='Add?',command=self.add_word_to_selection)
                self.askSelectionButton.place(x=10,y=35)

        except AttributeError:
            self.error_message(self.ERROR_TITLE,'No dictionaries added.')
    
    def add_word_to_selection(self):
        ###add label 
        if self.user_input != '':
            if self.user_input not in self.UNKNOWNS:
                self.UNKNOWNS.append(self.user_input)

        ###add to bottom of screen's history
        history_txt = tk.Text(self.SELECTED_WORDS,width=300,height=20,background=self.SELECTED_WORDS_BG)
        history_txt.place(x=0,y=20,anchor='nw',relwidth=1.0,relheight=100)
        for num, word in enumerate(self.UNKNOWNS):

            history_txt.insert(tk.END,"{}:{}\n".format(num+1,word))
        
        history_txt.configure(state=DISABLED)

    def add_to_sheets(self,clean):
        file_path = '{path}\{name}{time}.csv'.format(path=self.GSPREAD_BACKUPS,name='backup',time=datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))    
        if clean == False:
                if len(self.UNKNOWNS) > 0:
                    if self.double_check(self.WARNING_TITLE,'Are you sure?'):
                        try:
                            sheet = ReturnedSheet("JWordsImmersion",'Word','Frequency',os.path.dirname(__file__),
                            self.GSPREAD_REQS,self.UNKNOWNS)
                            sheet.UpdateSheet()
                            if self.double_check('Save as CSV?','Would you like to save this as a csv backup?'):
                                sheet.saveAsCSV(file_path = file_path)
                                self.show_info('File Location','The file is located:\n\n{}.'.format(file_path))
                        except FileNotFoundError:
                            self.error_message(self.ERROR_TITLE,"Check if you have your creds.json file in {}\n\n".format(self.GSPREAD_REQS))

        
                        
                else:
                    self.error_message('Error','No words added to list.')

        elif clean==True:
            if self.double_check(self.WARNING_TITLE,'Are you sure?'):
                try:
                    sheet = ReturnedSheet("JWordsImmersion",'Word','Frequency',os.path.dirname(__file__),self.GSPREAD_REQS)
                    sheet.UpdateSheet()
                    if self.double_check('Save as CSV?','Would you like to save this as a csv backup?'):
                        sheet.saveAsCSV(file_path = file_path)
                        self.show_info('File Location','The file is located:\n\n {}.'.format(file_path))

                except: #usually a connection error
                    self.error_message(self.ERROR_TITLE,'Could not proceed. Check internet connection / check that you have the required files in:\n\n{}.'.format(self.GSPREAD_REQS))

    def print_dict_to_frame(self,results_list):
        bg=self.SELECTED_LANG_SETTINGS_DICT['search_results_frame_bg']
        txt = tk.Text(self.SEARCH_RESULTS_TEXT_FRAME,width=1,height=1,background=bg,relief=RIDGE)
        txt.place(x=0,y=0,anchor='nw',relwidth=1.0,relheight=1.0)
        txt.tag_configure('header',justify = 'center',font=(self.FONT_NAME,12,'bold'))
        txt.tag_configure('entry',font=(self.FONT_NAME,8))
        for r_list in results_list:
            header = r_list[0]
            entry = r_list[1]
            txt.insert(tk.END, "{}\n".format(header),'header')
            for single_result in entry:
                txt.insert(tk.END,single_result+"\n",'entry')
        txt.configure(state=DISABLED)

    def change_color_on_entry_frame(self,f,enter_color,leave_color):
        def on_enter(e):
            f['background'] = enter_color
        def on_leave(e):
            f['background'] = leave_color
        f.bind("<Enter>",on_enter)
        f.bind("<Leave>",on_leave)

    def get_chosen_file(self,asked_dir):
        filename = filedialog.askopenfilenames(initialdir=asked_dir,title='Choose the dictionary files.')
        return filename

    def error_message(self,title,description):
        messagebox.showerror(title,description)

    def double_check(self,title,message):
        yesNo = messagebox.askquestion(title,message,icon='warning')
        if yesNo == 'yes':
            return True

    def show_info(self,title,message):
        messagebox.showinfo(title,message)
    
    def motion(self,event):
        ##print the x,y coord of mouse
        x,y = event.x,event.y
        print('{},{}'.format(x,y))
    

##initialize
if __name__ == "__main__":
    App = App()
    App.initialize()
