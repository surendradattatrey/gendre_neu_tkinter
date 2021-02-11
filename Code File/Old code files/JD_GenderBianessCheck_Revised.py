# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 21:33:14 2019

@author: Shruti
"""

import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize 
import numpy
import pandas as pd
import re
import sys
#import sys
#reload(sys)
#sys.setdefaultencoding("ISO-8859-1")

#nltk.download('tagsets')
#nltk.download('brown')

try:
    gender_score = pd.read_csv(r'C:\Users\Shruti\Desktop\jd_bias_code\POS_gender_score.csv')
except Exception as e:
    print(sys.exc_info()[0])
    print(e)
    sys.exit("Please put Scoring file on desired location")
    
try:    
    Job_details = pd.read_csv (r'C:\Users\Shruti\Desktop\jd_bias_code\JD_detail.csv',encoding='cp1252')
except Exception as e:
    print(sys.exc_info()[0])
    print(e)
    sys.exit("Please put Job Description file on desired location")
    
    
data = Job_details['Job Description'].values[0]
df = pd.DataFrame(data.split("\n"))
df = df[df.iloc[:,0]!=""]
df.head()
df.columns = ['Job Description']
df.head()
df.reset_index(inplace=True)
del df['index']
df.head()
df["job_desc_clean"] = df.replace('[^a-zA-Z0-9 ]', '', regex=True)
df.head()
df['job_desc_clean']= df["job_desc_clean"].str.lower()
df.head()
df['job_description_tokenized'] = df['job_desc_clean'].apply(word_tokenize)
word_lst = df['job_description_tokenized'].values.tolist()
word_lst
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

dfObj_filtered = dfObj[(dfObj.POS == 'NN')| (dfObj.POS == 'NNP')| (dfObj.POS == 'PRP') | (dfObj.POS =='PRP$')]
df_cd = pd.merge(dfObj_filtered, gender_score, how='inner', on = 'Token')

df_cd_filter = df_cd[df_cd['Score'] > 0]

biased_tokens = df_cd_filter['Token']
biased_tokens = list(biased_tokens)

len_data = len(df['job_description_tokenized'])

para_location = []
for x in range(len(df.index)):
    
    for a in (df['job_description_tokenized'].iloc[x]):
        #print(x,a)
        for b in biased_tokens: 
            if(a == b):              
                para_location.append(x) 
para_location   
Total = df_cd['Score'].sum()

if Total > 0:
    print("Job Description is Gender Biased, Please check paragraph no." , set (para_location))
else:
    print("Job Description is Gender neutral")



