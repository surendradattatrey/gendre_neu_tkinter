# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 12:52:19 2019

@author: surendra_dattatrey
"""

import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize 
import numpy
import pandas as pd
import re
import sys

#nltk.download('tagsets')
#nltk.download('brown')

try:
    gender_score = pd.read_csv (r'C:/Users/surendra_dattatrey/Desktop/S&P Data/Gender Neutral JD/POS_gender_score.csv')
except Exception as e:
    print(sys.exc_info()[0])
    print(e)
    sys.exit("Please put Scoring file on desired location")
    
try:    
    Job_details = pd.read_csv ('C:/Users/surendra_dattatrey/Desktop/S&P Data/Gender Neutral JD/JD_detail.csv', encoding='cp1252')
except Exception as e:
    print(sys.exc_info()[0])
    print(e)
    sys.exit("Please put Job Description file on desired location")

#Job_details['Job Description_tokenized'] = Job_details['Job Description'].apply(word_tokenize)

interim_data = str(Job_details['Job Description']).lower()[1:]
data = re.sub('[^A-Za-z0-9]+', ' ',interim_data)
Job_details['Job Description_tokenized'] = data
Job_details['Job Description_tokenized'] = Job_details['Job Description_tokenized'].apply(word_tokenize)

word_lst = Job_details['Job Description_tokenized'].values.tolist()

word_list=[]
for i in range(len(word_lst)):
    word_list.append([])
for i in range(len(word_lst)): 
    for word in word_lst[i]:
        if word[1:].isalpha():
            word_list[i].append(word[0:]) 

tagged_tokens=[]
for token in word_list:
    tagged_tokens.append(nltk.pos_tag(token))


import itertools
merged = list(itertools.chain(*tagged_tokens))


dfObj = pd.DataFrame(merged) 
dfObj.columns = ['Token', 'POS']

dfObj_filtered = dfObj[(dfObj.POS == 'NN')| (dfObj.POS == 'NNP')| (dfObj.POS == 'PRP')]
dfObj_filtered
df_cd = pd.merge(dfObj_filtered, gender_score, how='inner', on = 'Token')

Total = df_cd['Score'].sum()
Total

if Total > 0:
    print("Job Description is Gender Biased, Please check.")
else:
    print("Job Description is Gender neutral")
