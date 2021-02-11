rm(list=ls())

library(openNLP)
library(stringi)
library(stringr)
library(NLP)
library(magrittr)
library(tm)

x <- "The Team: The team is responsible for executing Data Science projects end to end. The project list includes (but is not limited to) Recommendation Engines, NLP Based Classifiers, Ratings Prediction, Bond Scoring, Bond Issuance etc
The Impact of her: This is a key position in the team that would ensure data readiness for some of our key projects in Markets Intelligence division that would have substantial impact on an upcoming product.
What's in it for him: You will further fortify your skills as a Data Engineer while gaining perspective in Predictive Analytics. The role shall help you grow in following areas:
.Big Data/Cloud Technology based Analytics
.Introduce you to and guide you on cutting edge Machine Learning techniques
.Encourage you to bring in new ideas and provide you means to learn/implement them to fulfill project needs
Responsibilities: The key responsibility of the data engineer is to ingest structured, semi structured and unstructured data from across the whole organization within planned timeframes for the team of data scientists to analyze, build models and solutions for the different S&P businesses. As such, the data engineer will work with Stakeholders, Business Users and Data Scientists to understand the business goals and requirements and translate them into data requirements. The engineer will design and build efficient data extraction/processing/storage logic from/to Databases, cloud systems, Big Data, Restful APIs etc. The role also involves architecting and developing end to end data pipelines to help solve data science problems while also engaging in overall project development activities.
What We're Looking For: 
Basic Qualifications:
.Bachelor's degree in engineering.
.Minimum of 7 years of experience in Data Engineering
.Experience in dealing with servers, production systems, multiple environments and varied software engineering aspects
.Knowledge of Data Profiling and Data Quality concepts and techniques
.Ability to work independently and achieve expected results with general/broad level requirements
.Strong written & verbal communication
.Python and/or R
.SQL
.Operability in Unix/Linux
.ETL Tools and Data Warehousing
.Big Data (atleast 3) - Hive, HDFS, Flume, Kafka, NoSQL(HBase/MongoDB etc), Spark/PySpark, Cloud Technologies
Preferred Qualifications:
.Familiarity with RESTful APIs
.Initial exposure to machine learning is good to have"
x <- as.String(x)    # from NLP package
x <- tolower(x)

##### Function for Text Cleaning
text.clean = function(x)                    # text data
{ 
  x  =  gsub("<.*?>", " ", x)               # regex for removing HTML tags
  x  =  iconv(x, "latin1", "ASCII", sub="") # Keep only ASCII characters
  x  =  gsub("[^[:alnum:]]", " ", x)        # keep only alpha numeric 
  x  =  tolower(x)                          # convert to lower case characters
  #x  =  removeNumbers(x)                    # removing numbers
  #x  =  stripWhitespace(x)                  # removing white space
  x  =  gsub("^\\s+|\\s+$", "", x)          # remove leading and trailing white space
  return(x)
}

x_pros  = text.clean(x)  

extractChunks <- function(x) {
  
  x <- as.String(x)
  
  wordAnnotation <- annotate(x, list(Maxent_Sent_Token_Annotator(), Maxent_Word_Token_Annotator()))
  POSAnnotation <- annotate(x, Maxent_POS_Tag_Annotator(), wordAnnotation)
  POSwords <- subset(POSAnnotation, type == "word")
  #POSwords <- subset(POSAnnotation)
  tags <- sapply(POSwords$features, '[[', "POS")
  
  tagged_df <- data.frame(Tokens = x[POSwords], Tags = tags)
  tagged_df$Tags_mod = grepl("NN|PRP", tagged_df$Tags)
  tagged_df <- tagged_df[tagged_df$Tags_mod == "TRUE",]
  
  return(tagged_df)

  gc()
  
} # func ends 

extractChunks (x_pros)

