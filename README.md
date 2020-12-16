![Tweesent](TwitterSentimentAnalyser/TSentimentAnalyser/static/images/Banner.png)
#### Tweesent

> This Django web application is used to generate a sentiment-score of tweets, descriptive statistics and data visualisations based on user input.

![build-img]

On the homepage the user is able to get the top 10 latest Twitter trends based on the submitted location as well as the possibility to input a desired search-term or #hashtag and the number of tweets one would like to fetch. A maximum of 500 tweets is accepted to search per request. 

(Screenshot maybe)

Once submitted, the desired amount of tweets is streamed from twitter in real-time. The fetched tweets are then cleaned, translated to English and analysed through VADER to appoint them a sentiment-score.
In a next step the most used words and hashtags are displayed in a word cloud and the data gets visualized with graphs.

(screenshot)

The sentiment-score lies in between -1 and +1 and is classified as follows:

* A tweet in between +1 and +0.05 is positive.

* A tweet in between +0.05 and -0.05 is neutral.

* A tweet in between -0.05 and -1 is negative.

Check the [vaderSentiment] Github page for more information how the score is calculated.

#### To run on your local machine:

1. Create a Virtual environment and install all necessary packages via  `pip install -r requirements.txt`
2. Fill in your Twitter API keys in `twitter_credentials.py`
3. Run django server `python manage.py runserver`
4. Get started!

<!-- Markdown link & img dfn's -->
[build-img]: https://img.shields.io/badge/build-passing-brightgreen
[vaderSentiment]: https://github.com/cjhutto/vaderSentiment
