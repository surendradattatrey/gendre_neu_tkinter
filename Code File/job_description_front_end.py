# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 15:15:18 2020

@author: surendra_dattatrey
"""

from tkinter import *
import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import scrolledtext
import re



df = pd.read_csv(r'C:\Users\surendra_dattatrey\Desktop\S&P Data\Gender Neutral JD\POS_gender_score_v3.csv')
df['Token'] = df['Token'].str.replace(" ","")
df['Word Replacement'] = df['Word Replacement'].str.replace(" ","")
df = df.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)
list_of_words = df['Token'].to_list()

dict_replace = {}
for i in df['Token'].unique():
    dict_replace[i] = [str(df['Word Replacement'][j]).lower() for j in df[df['Token']==i].index]
df_replace = pd.DataFrame({'Replacement':dict_replace})
df_replace.reset_index(inplace=True)
df_replace.columns = ['Word','Replacement']
for i in range(len(df_replace)):
    df_replace.loc[i,'Replacement'] = str(df_replace.loc[i,'Replacement']).strip('[]').replace('nan','').replace("'', ''","No Replacement").replace("''","No Replacement").replace("'","")

root=Tk()
root.geometry("2000x1700")
root.configure(background='azure')

# Create label 
root.title("Job Description Text Search") 


l1=Label(root,text="Enter your Text",font=('Helvetica',20,'bold'),foreground='RoyalBlue1',background='azure')
l1.grid(row=0,column=1)

text_entered = Text(root,height=30, width=143,font=('Helvetica',14),background='azure')
text_entered.grid(row=1,rowspan=9,column=1,columnspan=1,padx=10,pady=10)
vsbar1 = Scrollbar(root, orient=VERTICAL, command=text_entered.yview,width=30,background='azure')
vsbar1.grid(row=1, rowspan=9,column=500, sticky=N+S+E+W,pady=10)
text_entered.configure(yscrollcommand=vsbar1.set)

def replacement_fun(temp_df,temp_list_word):
    word_replacement_list = []
    df_match_word = pd.DataFrame(columns=['Word', 'Replacement'])
    # temp_list_word = ['she', 'her', 'She', 'Her', 'Hers', 'hers', 'Herself', 'compassionate', 'emotional', 'interpersonal', 'interdependent', 'determined', 'support'] 
    for word in temp_list_word:
        data = temp_df[temp_df['Word'].isin(temp_list_word)]
        df_match_word = df_match_word.append(data)
    df_match_word = df_match_word.reset_index()
    del(df_match_word['index'])
    zz = df_match_word[~df_match_word.Replacement.str.contains("No Replacement")]
    replacement_dict = dict(zip(zz['Word'], zz['Replacement']))
    return replacement_dict

def first_word_find(str_):
    d_ = re.findall('[\n]+[A-Za-z0-9%&+^!@#$*(-_]*', str_, re.I)
    print(d_,"going crazy")
    token = []
    for c in d_:
        c= c.replace("\n\n","")
        c= c.replace("\n","")
        token.append(c)
    token = [w.lower() for w in token]    
    first_element = str_.split()[0].lower()
    print(token,"heheheheheh")
    if first_element in token:
        token.remove(first_element)
        find_first_word_list = token
        return find_first_word_list
    else:
        return token
    
def very_first_word_find(str_):
    first_word = str_.split()[0]
    print(first_word)
    return first_word
    
def end_word_find_fullstop(str_):
    end_word = []
    d_end = re.findall('[A-Za-z0-9-_]*\.', str_, re.I)    
    for result in d_end:
        end_word.append(result[:-1])
    special_character = [""," ","\n","\r",".","\t"]
    end_ = list(set(end_word) - set(special_character))
    all_end_words = end_ 
    return all_end_words

def end_word_find_blankspace(str_):
    end_ = []
    d_ = re.findall('[A-Za-z0-9-_]*[\r\n\n]', str_, re.I)
    for result in d_:
        end_.append(result[:-1])    
    special_character = [""," ","\n","\r",".","\t"]
    end_final = list(set(end_) - set(special_character))
    return end_final

def my_click():       
    text_to_display = text_entered.get(0.0,END)    
    text = Text(root, height = 30, width = 100,font=('Helvetica',14),background='azure')
    list_text_to_display = text_to_display.split()
    list_text_to_display_lower = [word.lower() for word in list_text_to_display]
    text.insert(INSERT, text_to_display)
    text.tag_remove('found', '0.0', END)
    text.configure(state="disabled")
    word_found = []
    end_word_list = []
    word_found_blankspace = []
    end_words = end_word_find_fullstop(text_to_display)
    end_words_blankspace = end_word_find_blankspace(text_to_display)
    first_words = first_word_find(text_to_display)
    very_first_word =  very_first_word_find(text_to_display)
    word_found_end=[]
    word_found_first=[]
    single_word_found_blankspace = []
    token_word = df['Token'].to_list()
    tokens = [word.lower() for word in token_word]
    # first_word_find_case_2_list = first_word_find_case_2(text_to_display)
    # first_word_find_case_2_list_found = []
    for word in list_of_words:
        if word.lower() in tokens:
            if word.lower() in list_text_to_display_lower:
                word = "[^A-Za-z_-]"+word+"[^A-Za-z_-]"
                length = IntVar()
                idx = '1.0'
                while idx:              
                    idx = text.search(word, idx, nocase=1, stopindex=END,regexp=True,count =length,exact=True)
                    if idx:
                        len_highlight = len(word.replace("[^A-Za-z_-]",""))
                        row_idx = str(int(idx.split(".")[0]))
                        col_idx = str(int(idx.split(".")[1])+1)
                        idx = row_idx+"."+col_idx
                        lastidx = '%s+%dc' % (idx, len_highlight)
                        text.tag_add('found', idx, lastidx)
                        idx = lastidx
                        replacement_word = word.replace("[^A-Za-z_-]","")
                        word_found.append(replacement_word)
    for word in end_words:        
            if word.lower() in tokens:
                len_ = IntVar()
                idx = '1.0'
                word = "^"+word+'$'
                while idx:              
                    idx = text.search(word, idx, nocase=1, stopindex=END,count =len_,exact=True,regexp=True)
                    if idx:
                        len_highlight = len(word)
                        len_highlight = len(word.replace("^","").replace('$',""))
                        row_idx = str(int(idx.split(".")[0]))
                        col_idx = str(int(idx.split(".")[1]))
                        idx = row_idx+"."+col_idx
                        lastidx = '%s+%dc' % (idx, len_highlight)
                        text.tag_add('found', idx, lastidx)
                        idx = lastidx
                        word = word.replace("^","").replace('$',"").lower()
                        word_found_end.append(word) 
    for word in end_words_blankspace:        
            if word.lower() in tokens:
                len_ = IntVar()
                idx = '1.0'
                word = "[^A-Za-z_-]"+word
                while idx:     
                    idx = text.search(word, idx, nocase=1, stopindex=END,count =len_,exact=True,regexp=True)
                    if idx:
                        len_highlight = len(word.replace("[^A-Za-z_-]",""))
                        row_idx = str(int(idx.split(".")[0]))
                        col_idx = str(int(idx.split(".")[1])+1)
                        idx = row_idx+"."+col_idx
                        lastidx = '%s+%dc' % (idx, len_highlight)
                        text.tag_add('found', idx, lastidx)
                        idx = lastidx
                        replacement_word = word.lower()
                        replacement_word = word.replace("[^A-Za-z_-]","")
                        word_found_blankspace.append(replacement_word)
#Case single word in a line      
    for word in end_words_blankspace:        
            if word.lower() in tokens:
                length_ = IntVar()
                idx = '1.0'
                word = "^"+word+"$"
                while idx:              
                    idx = text.search(word, idx, nocase=1, stopindex=END,regexp=True,count =length,exact=True)
                    if idx:
                        len_highlight = len(word.replace("^","").replace("$",""))
                        row_idx = str(int(idx.split(".")[0]))
                        col_idx = str(int(idx.split(".")[1]))
                        idx = row_idx+"."+col_idx
                        lastidx = '%s+%dc' % (idx, len_highlight)
                        text.tag_add('found', idx, lastidx)
                        idx = lastidx
                        replacement_word = word.replace("^","").replace("$","")
                        single_word_found_blankspace.append(replacement_word)
                        
    for word in first_words:        
            if word.lower() in tokens:
                length = IntVar()
                idx = '1.0'
                word = "^"+word+"[^A-Za-z_-]"
                print(word)
                # word = word+"\b"
                while idx:              
                    idx = text.search(word, idx, nocase=1, stopindex=END,count =length,exact=True,regexp=True)
                    if idx:
                        len_highlight = len(word.replace("[^A-Za-z_-]","").replace("*","").replace("^",""))
                        row_idx = str(int(idx.split(".")[0]))
                        col_idx = str(int(idx.split(".")[1])-1)
                        idx = row_idx+"."+col_idx
                        lastidx = '%s+%dc' % (idx, len_highlight)
                        text.tag_add('found', idx, lastidx)
                        idx = lastidx
                        word = word.replace("[^A-Za-z_-]","").replace("*","").lower()
                        word_found_first.append(word)          
    list_very_first_word = []
    if very_first_word.lower() in tokens:
        list_very_first_word.append(very_first_word)
        length = IntVar()
        idx = '1.0'
        word = very_first_word+"[^A-Za-z_-]*"
        while idx:
            idx = text.search(word, idx, nocase=1, stopindex=END,count =length,exact=True,regexp=True)
            print(idx)
            if idx:
                len_highlight = len(very_first_word.replace("[^A-Za-z_-]*",""))
                row_idx = str(0)
                col_idx = str(0)
                idx = row_idx+"."+col_idx
                lastidx = '%s+%dc' % (idx, len_highlight)
                text.tag_add('found', idx, lastidx)
                print(word)
                break
        
      
    total_word_found = word_found_end+word_found+word_found_first+word_found_blankspace+list_very_first_word+single_word_found_blankspace#+first_word_find_case_2_list_found
    dict_replacement = replacement_fun(df_replace,total_word_found)
    text.tag_config('found', background ="light blue")      
    l2=Label(root,text="Text Entered",font= ('Helvetica',18,'bold'),foreground='RoyalBlue1',background='azure')
    l3=Label(root,text="Replacement word",font=('Helvetica',18,'bold'),foreground='RoyalBlue1',background='azure')
    vsbar2 = Scrollbar(root, orient=VERTICAL, command=text.yview,width=30,background='azure')
    vsbar2.grid(row=1, rowspan=540,column=503, sticky=N+S+E+W,pady=10)
    text.configure(yscrollcommand=vsbar2.set)
    text.grid(row=1,column=3,columnspan=500,rowspan=540,sticky=N+S+E+W,pady=10,padx=10) 
    l2.grid(row=0,column=100,columnspan=250)
    l3.grid(row=0,column=875,columnspan=300,rowspan=1,sticky=W)   
    lstbox = Listbox(root,font=('Helvetica',12),width=48,background='azure')
    lstbox.grid(row=1,column=800,columnspan=295,sticky=W,pady=10)
    for key in dict_replacement:
        lstbox.insert(END, '{}: {}'.format(key, dict_replacement[key]))
    vsbar3 = Scrollbar(root, orient=VERTICAL, command=lstbox.yview,width=28,background='azure')
    vsbar3.grid(row=1, column=1101, sticky=N+S+E+W,pady=10)
    lstbox.configure(yscrollcommand=vsbar3.set)
    quit_button = tk.Button(root,text="Exit", bg="light blue", font=('Helvetica',14,'bold'),command=root.destroy)
    quit_button.grid(row=800,column=400)
    l1.destroy()
    b1.destroy()
    text_entered.destroy() 
    vsbar1.destroy()
    

b1 = Button(root, text = "Next", command=my_click,font=('Helvetica',14,'bold'),bg="light blue") 
b1.grid(row=10,column=1)

root.mainloop()

