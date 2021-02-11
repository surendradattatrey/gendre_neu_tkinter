# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 21:08:17 2019

@author: surendra_dattatrey
"""

import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize 
from nltk.corpus import stopwords
import numpy
import pandas as pd

stop_words = set(stopwords.words('english')) 

try:    
    Job_details = pd.read_csv ('C:/Users/surendra_dattatrey/Desktop/S&P Data/Gender Neutral JD/Open_req - APAC_IncludeIndia.csv', encoding='cp1252')
except Exception as e:
    print(sys.exc_info()[0])
    print(e)
    sys.exit("Please put Job Description file on desired location")

try:
    gender_score = pd.read_csv(r'C:\Users\surendra_dattatrey\Desktop\S&P Data\Gender Neutral JD\POS_gender_score.csv')
except Exception as e:
    print(sys.exc_info()[0])
    print(e)
    sys.exit("Please put Scoring file on desired location")

df = Job_details
df

for i in range(len(Job_details)):
    #print(i)
    
    data = Job_details['Job Description']
    #data = data.to_frame()
    #data['Job Description']= data['Job Description'].apply(str)
    df['Job_Description'] = pd.DataFrame(data.str.split("\n"))
    df['job_desc_clean'] = df['Job Description'].apply(str).replace('[^a-zA-Z0-9 ]', '', regex=True)
    df['job_desc_clean']= df['job_desc_clean'].str.lower()
    

#df
    

## Word Tokenization process and finding biasness
for x in range(len(Job_details)):
    df['job_description_tokenized'] = df['job_desc_clean'].apply(word_tokenize)
    df['job_description_tokenized'] = df['job_description_tokenized'].apply(lambda x: [item for item in x if item not in stop_words])
    
score_cnt=[]
for a in range(45):
    df['job_description_tokenized_tokens'] = df['job_description_tokenized'].tolist()
    word_lst = df['job_description_tokenized'][a]
    word_list=[]
    for i in range(len(word_lst)): 
      
        if word_lst[i][0].isalpha():
            word_list.append(word_lst[i])
            
    tagged_tokens=[]
    for token in word_lst:
      
        tagged_tokens.append(nltk.pos_tag([token]))
        
    import itertools
    merged = list(itertools.chain(*tagged_tokens))
    
    dfObj = pd.DataFrame(merged) 
    dfObj.columns = ['Token', 'POS']
    
    dfObj_filtered = dfObj[(dfObj.POS == 'NN')| (dfObj.POS == 'NNP')| (dfObj.POS == 'PRP') | (dfObj.POS =='PRP$')]
    df_cd = pd.merge(dfObj_filtered, gender_score, how='inner', on = 'Token')
    df_cd_filter = df_cd[df_cd['Score'] > 0]
    
    #dfToList = df_cd_filter['Token'].tolist()
    #df[''] = dfToList.tolist()
    
    biased_tokens = df_cd_filter['Token']
    #biased_tokens = list(biased_tokens)

    len_data = len(df['job_description_tokenized'])

    para_location = []
    for x in range(len(df.index)):
    
        for a in (df['job_description_tokenized'].iloc[x]):
            #print(x,a)
            for b in biased_tokens: 
                if(a == b):              
                    para_location.append(x) 
    #para_location   
    Total = df_cd['Score'].sum()
    score_cnt.append(Total)
    #df['Job_desc_biased_tokens']= list (biased_tokens)
    
    #print(df_cd)
#score_cnt_df=score_cnt.to_dataFrame()

#df

scr_cnt=pd.DataFrame(score_cnt)
scr_cnt
df['score_count']=scr_cnt

df[df['score_count']>0]