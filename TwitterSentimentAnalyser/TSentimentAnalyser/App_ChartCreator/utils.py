import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

"""
Settings for Charts which are created in views.py.
"""


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(x):
    plt.switch_backend("AGG")
    plt.figure(figsize=(6.4, 4.8))
    plt.title("Distribution of Sentiment")
    plt.pie(x, labels=["positve","neutral","negative"],colors=("#4caf50","#2196f3","#f44336"),autopct='%1.1f%%')

    graph = get_graph()
    return graph


def get_wordcloud(y):
    plt.switch_backend("AGG")
    plt.figure(figsize=(6.4,4.8))
    plt.axis("off")
    plt.imshow(y, interpolation="bilinear")
    word_cloud = get_graph()
    return word_cloud


def get_hashtagcloud(z):
    plt.switch_backend("AGG")
    plt.figure(figsize=(6.4,4.8))
    plt.axis("off")
    plt.imshow(z, interpolation="bilinear")
    hashtag_cloud = get_graph()
    return hashtag_cloud

def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = int(203.0)
    s = int(89.1)
    l = int(53.1 * float(random_state.randint(60, 120)) / 130.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)

def get_boxplot(b):
    plt.switch_backend("AGG")
    plt.figure(figsize=(6.4,4.8))
    plt.title("Distribution of Sentiment")
    plt.boxplot(b)
    boxplot = get_graph()
    return boxplot

def get_distribution(d):
    plt.switch_backend("AGG")
    plt.figure(figsize=(6.4, 4.8))
    plt.title("Distribution of Sentiment")
    sns.displot(data=d, x="sentiment", kde=True)
    distribution = get_graph()
    return distribution
