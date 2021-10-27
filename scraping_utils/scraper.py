# Twitter Scraper for Hate Speech detection
import tweepy
import pandas as pd
import time
import configparser

# Folder Locations
OUTPUT_DIR = "data"

# Load Configs
config = configparser.ConfigParser()
config.read('config.ini')
consumer_key = config.get('dev', 'consumer_key')
consumer_secret = config.get('dev', 'consumer_secret')
access_token = config.get('dev', 'access_token')
access_token_secret = config.get('dev', 'access_token_secret')

# Grant Twitter dev account access to Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# Function to scrape twitter based on user
def get_tweets_by_user(username, count, exclude_replies=True, include_rts=False, filename=None):
    try:      
        # Creation of query method using parameters
        tweets = tweepy.Cursor(api.user_timeline,user_id=username, exclude_replies=True, include_rts=False).items(count)

        # Pulling information from tweets iterable object
        tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]

        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list,columns=['Datetime', 'Tweet Id', 'Text'])

        # Converting dataframe to CSV 
        tweets_df.to_csv('{}-tweets.csv'.format(username), sep=',', index = False)
        
        # Set default filename
        if filename == None:
            filename = text_query.replace(' ', '_')
        
        # Converting dataframe to CSV 
        tweets_df.to_csv(f'{OUTPUT_DIR}/{filename}.txt', sep=',', index = False)

    except BaseException as e:
          print('failed on_status,',str(e))
          time.sleep(3)


# Function to scrape twitter based on query
def get_tweets_by_query(text_query, count, lang='en', result_type='mixed', filename=None, filter_rt=True):
    try:
        # Filter retweets
        if filter_rt:
            text_query = text_query + " -filter:retweets"
        
        # Creation of query method using parameters
        tweets = tweepy.Cursor(api.search_tweets,q=text_query, lang=lang, result_type=result_type).items(count)
     
        # Pulling information from tweets iterable object
        tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
     
        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list,columns=['Datetime', 'Tweet Id', 'Text'])
        
        # Set default filename
        if filename == None:
            filename = text_query.replace(' ', '_')
        
        # Converting dataframe to CSV 
        tweets_df.to_csv(f'{OUTPUT_DIR}/{filename}.txt', sep=',', index = False)
     
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)


#if __name__=='__main__':
#    text_query = "Asian Hate"
#    count = 20
#    get_tweets(text_query, count, filename = "test", result_type="mixed")
