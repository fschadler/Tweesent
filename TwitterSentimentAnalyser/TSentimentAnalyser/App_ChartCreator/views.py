from wordcloud import WordCloud, STOPWORDS
from .utils import get_plot, get_wordcloud, get_hashtagcloud

"""
App to create charts which are displayed on the analysis.html page.  
"""


def pie_chart_gen(count_positive, count_neutral, count_negative):
    # Creates Pie Chart with Sentiment Score
    x = [count_positive,count_neutral,count_negative]
    chart = get_plot(x)
    return chart


def word_cloud_gen(df):
    # Creates Word Cloud based on Words in Tweets, which are cleaned and translated.
    list_of_cleaned_english_tweets = list(df["cleaned_english_tweets"])
    stopwords = set(STOPWORDS)
    all_words = ' '.join([text for text in list_of_cleaned_english_tweets])
    y = WordCloud(background_color='white', stopwords=stopwords, width=1600, height=800, random_state=21,
                          colormap='jet', max_words=50, max_font_size=200).generate(all_words)
    return get_wordcloud(y)


def hashtag_cloud_gen(df):
    # Creates Word Cloud based on Hashtags in Tweets.
    hashtag_list_tweets = list(df["tweets"].str.findall(r"#(\w+)").sum())
    stopwords = set(STOPWORDS)
    all_hashtags = ' '.join([hashtag for hashtag in hashtag_list_tweets])
    z = WordCloud(background_color='white', stopwords=stopwords, width=1600, height=800, random_state=21,
                          colormap='jet', max_words=50, max_font_size=200).generate(all_hashtags)

    return get_hashtagcloud(z)



