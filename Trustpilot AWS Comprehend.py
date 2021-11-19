import boto3
import json
import pandas as pd
import sys

#Initiate AWS comprehend (you need to have installed the AWS command line and have a AWS account)
#Please note that there are cost implications
comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')
                
#List here the files to scrape
files_input = ['trustpilot_scraper_export_full.csv']
#Select what the start date for the analysis
starting_date =  ['2019-11-09']

#%%
df_out = pd.DataFrame(columns=['source_file','link', 'page_num', 'name', 'date', 'invited_flag',
           'title', 'review', 'stars', 'polarity_score_neg', 'polarity_score_neu',
           'polarity_score_pos', 'polarity_score_mixed'])


for file_name in files_input:
    df_in = pd.read_csv(file_name)
    
    #filted for starting date
    df_in = df_in[df_in['date']>starting_date]
    
    #Print current execution
    print(file_name)
    
    for idx, row in df_in.iterrows():
        
        review_text = row['review']
       
        #shorten text if too long (>500 bytes)
        if len(review_text.encode('utf-8'))>5000:
            review_text=review_text[0:int(len(review_text)/2)]
          
        try:
            json_file = json.dumps(comprehend.detect_sentiment(Text=review_text, LanguageCode='en'), sort_keys=True, indent=4)
            dict_json=json.loads(json_file)
            
            df_out = df_out.append({"source_file":file_name,
                                     "link":row['link'],
                                     "page_num":row['page_num'],
                                     "name":row['name'],
                                      "date":row['date'], 
                                      "invited_flag": row['invited_flag'],
                                      "title": row['title'],
                                      "review": row['review'],
                                      "stars":row['stars'],
                                      'aws_sentiment':dict_json['Sentiment'],
                                       'polarity_score_neg':dict_json['SentimentScore']['Negative'],
                                       'polarity_score_neu':dict_json['SentimentScore']['Neutral'],
                                       'polarity_score_pos':dict_json['SentimentScore']['Positive'], 
                                       'polarity_score_mixed':dict_json['SentimentScore']['Mixed']
                                     }
                                    , ignore_index=True) 
        except:
            print('row failed')
        
        
#export file
df_out.to_csv('trustpilot_sentiment_analysis_AWS_comprehend.csv')
