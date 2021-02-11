import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize 
import numpy
import pandas as pd
import re

nltk.download('tagsets')
nltk.download('brown')


gender_score = pd.read_csv (r'C:/Users/surendra_dattatrey/Desktop/S&P Data/Gender Neutral JD/POS_gender_score.csv')

Job_details = pd.read_csv ('C:/Users/surendra_dattatrey/Desktop/S&P Data/Gender Neutral JD/JD_detail.csv', encoding='cp1252')


#Job_details['Job_Description_tokenized'] = Job_details['Job Description'].apply(word_tokenize)

interim_data = str(Job_details['Job Description']).lower()[1:]
data = re.sub('[^A-Za-z0-9]+', ' ',interim_data)
Job_details['Job_Description_tokenized'] = data
Job_details['Job_Description_tokenized'] = Job_details['Job_Description_tokenized'].apply(word_tokenize)

word_lst = Job_details['Job_Description_tokenized'].values.tolist()

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

df_cd = pd.merge(dfObj_filtered, gender_score, how='inner', on = 'Token')
df_cd

Total = df_cd['Score'].sum()

if Total > 0:
    print("Job Description is Gender Biased, Please check.")

