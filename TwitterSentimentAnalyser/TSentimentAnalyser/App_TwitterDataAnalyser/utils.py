import matplotlib.pyplot as plt
import base64
from io import BytesIO

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
    plt.pie(x, labels=["positve","neutral","negative"],colors=("#4caf50","#2196f3","#f44336"))

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