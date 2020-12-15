import re
import numpy as np
import pandas as pd
from google_trans_new import google_translator as Translator


"""
This app cleans and adds all Tweets to a dataframe.
"""


def remove_pattern(input_txt, pattern):
    # Checks for patterns stated in clean_tweets function
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
    # remove "\n" from Tweets
    lst = np.core.defchararray.replace(lst, "\n", " ")
    return lst


class TweetToDataframe:
    """
    Used for cleaning, analyzing, translating and appending the tweets in a pandas dataframe.
    """

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        translator = Translator()

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['lang'] = np.array([tweet.lang for tweet in tweets])
        df['user_id'] = np.array([tweet.user.id for tweet in tweets])
        df['user_screen_name'] = np.array([tweet.user.screen_name for tweet in tweets])
        df['follower_count'] = np.array([tweet.user.followers_count for tweet in tweets])
        df['location'] = np.array([tweet.user.location for tweet in tweets])
        df["english_tweets"] = df["tweets"].apply(lambda x: translator.translate(x, lang_tgt="en"))
        df["english_tweets"] = df["english_tweets"].astype("str")
        df["cleaned_tweets"] = df["tweets"].map(lambda x: clean_tweets(x))
        df["cleaned_english_tweets"] = df["english_tweets"].map(lambda x: clean_tweets(x))
        return df
