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
    plt.pie(x, labels=["positve","neutral","negative"],colors=("blue","lightblue","darkblue"))

    graph = get_graph()
    return graph