from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia
from googletrans import Translator
import tweepy
import wordcloud
import numpy as np
import pandas as pd

consumer_key = "LEZ6shUvjCPx12e9DwMtPw1uR"      #keys Florin
consumer_secret = "TAVTA300b55zdzHdf9qGSw8xEMqHHELZuTjVOdfQnCO6Kof6yH"
access_token = "807738825988575232-eHZC9kiBGOcI8g6CIf5rVvuDZr4bNC0"
access_token_secret = "Pa90jR4QtIogqm3GWWT7riK0UoDi8SHJFGr4yIXbBfLs4"

auth = tweepy.0AuthHandler(consumer_key, consumer_scret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

translator = Translator()
analyser = sia()

def sentiment_scores(text, engl=True):
    if engl:   #Wenn Tweet Englisch dann direkt Analyse
        trans = text
    else:      #Alle anderen Sprachen erst translaten
        trans = translator.translate(text).text
        
    sentiment_score = analyser.polarity_scores(trans)
    compound = sentiment_score["compound"]
    if compound >= 0.05:
        return 1
    elif (compound > -0.05) and (compound < 0.05):
        return 0
    else:
        return -1

def list_tweets(user_id, count, prt=False):
    tweets = api.user_timeline(
        "@" + user_id, count, tweet_mode="extended")
    tw = []
    for t in tweets:
        tw.append(t.full_text)
        if prt:
            print(t.full_text)
            print()
        return tw

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, "", input_txt)
    return input_txt

def clean_tweets(lst):
    # remove twitter Return handles (RT @xxx:)
    lst = np.vectorize(remove_pattern)(lst, "RT @[\w]*:")
    # remove twitter handles (@xxx)
    lst = np.vectorize(remove_pattern)(lst, "@[\w]*")
    # remove URL links (httpxxx)
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    # remove special characters, numbers, punctuations (except for #)
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
return lst


def word_cloud(wd_list):
    stopwords = set(STOPWORDS)
    all_words = ' '.join([text for text in wd_list])
    wordcloud = WordCloud(background_color='white',stopwords=stopwords,width=1600,height=800,random_state=21,colormap='jet',max_words=50,max_font_size=200).generate(all_words)
    plt.figure(figsize=(12, 10))
    plt.axis('off')
    plt.imshow(wordcloud, interpolation="bilinear");
    
#stream listener

def twitter_stream_listener(file_name,filter_track,follow=None,locations=None,languages=None,time_limit=20):
    class CustomStreamListener(tweepy.StreamListener):
        def __init__(self, time_limit):
            self.start_time = time.time()
            self.limit = time_limit
            # self.saveFile = open('abcd.json', 'a')
            super(CustomStreamListener, self).__init__()
        def on_status(self, status):
            if (time.time() - self.start_time) < self.limit:
                print(".", end="")
                # Writing status data
                with open(file_name, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        status.author.screen_name, status.created_at,
                        status.text
                    ])
            else:
                print("\n\n[INFO] Closing file and ending streaming")
                return False
         def on_error(self, status_code):
            if status_code == 420:
                print('Encountered error code 420. Disconnecting the stream')
                # returning False in on_data disconnects the stream
                return False
            else:
                print('Encountered error with status code: {}'.format(
                    status_code))
                return True  # Don't kill the stream
        def on_timeout(self):
            print('Timeout...')
            return True  # Don't kill the stream
    # Writing csv titles
    print('\n[INFO] Open file: [{}] and starting {} seconds of streaming for {}\n'.format(file_name, time_limit, filter_track))
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['author', 'date', 'text'])
    streamingAPI = tweepy.streaming.Stream(
        auth, CustomStreamListener(time_limit=time_limit))
    streamingAPI.filter(track=filter_track,follow=follow,locations=locations,languages=languages)
    f.close()
