import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize 
import numpy
import pandas as pd
#from nltk.book import *
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
    Job_details = pd.read_csv ('C:/Users/surendra_dattatrey/Desktop/S&P Data/Gender Neutral JD/JD_detail.txt',error_bad_lines=False, header = None , encoding='cp1252', sep = "\n",names=["Job Description"])    
except Exception as e:
    print(sys.exc_info()[0])
    print(e)
    sys.exit("Please put Job Description file on desired location")

Job_details["job_desc_clean"] = Job_details.replace('[^a-zA-Z0-9 ]', '', regex=True)
Job_details['job_desc_clean']= Job_details["job_desc_clean"].str.lower()
#data = re.sub('[^A-Za-z0-9]+', ' ',interim_data)
Job_details['job_description_tokenized'] = Job_details['job_desc_clean'].apply(word_tokenize)

word_lst = Job_details['job_description_tokenized'].values.tolist()

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

len_data = len(Job_details['job_description_tokenized'])
#nw_list = []
para_location = []
for x in range(len(Job_details.index)):
    
    for a in (Job_details['job_description_tokenized'].iloc[x]):
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
