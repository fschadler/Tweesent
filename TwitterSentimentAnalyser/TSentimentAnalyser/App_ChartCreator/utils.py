import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

"""
Functions for Chart Generation
"""


def get_graph():
    # Encoding and decoding graph to display it on html.
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(x):
    # Defines settings for Pie chart generation
    plt.switch_backend("AGG")
    plt.figure(figsize=(6.4, 4.8))
    plt.pie(x, labels=["positve","neutral","negative"],colors=("#4caf50","#2196f3","#f44336"),autopct='%1.1f%%')

    graph = get_graph()
    return graph


def get_wordcloud(y):
    # Defines settings for Wordcloud Chart generation
    plt.switch_backend("AGG")
    plt.figure(figsize=(6.4,4.8))
    plt.axis("off")
    plt.imshow(y, interpolation="bilinear")
    word_cloud = get_graph()
    return word_cloud


def get_hashtagcloud(z):
    # Defines settings for Hashtag Cloud Chart generation
    plt.switch_backend("AGG")
    plt.figure(figsize=(6.4,4.8))
    plt.axis("off")
    plt.imshow(z, interpolation="bilinear")
    hashtag_cloud = get_graph()
    return hashtag_cloud

def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    # Random text-color generation for Wordcloud and Hashtag Cloud
    h = int(203.0)
    s = int(89.1)
    l = int(53.1 * float(random_state.randint(60, 120)) / 130.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)

def get_boxplot(b):
    # Defines settings for Boxplot generation
    plt.switch_backend("AGG")
    sns.boxplot(x="sentiment", data=b, orient='v', width=0.6)
    boxplot = get_graph()
    return boxplot

def get_distribution(d):
    # Defines settings for Distribution Chart gen
    # Switching backend due to usage of seaborn
    plt.switch_backend("AGG")
    sns.histplot(data=d, x="sentiment", bins=20, kde=True)
    distribution = get_graph()
    return distribution
