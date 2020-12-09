from django.shortcuts import render
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

"""
This app is used to generate WordClouds which are displayed on the Output Page.
"""

def word_cloud(list_of_tweets):
    stopwords = set(STOPWORDS)
    all_words = ' '.join([text for text in list_of_tweets])
    wordcloud = WordCloud(background_color='white', stopwords=stopwords, width=1600, height=800, random_state=21,
                          colormap='jet', max_words=50, max_font_size=200).generate(all_words)
    plt.figure(figsize=(12, 10))
    plt.axis('off')
    plt.imshow(wordcloud, interpolation="bilinear");


def word_cloud_hashtag(df):
    #@ Florin, could you also add the Hashtag Wordcloud? Following List includes all used Hashtags in the tweets
    hashtag_list_tweets = df["tweets"].str.findall(r"#(\w+)").sum()



# Create your views here.
