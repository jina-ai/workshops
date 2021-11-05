import ipywidgets as widgets
import IPython.display as display
import requests
import os


def show_images(docs, max_images=5):
    image_list = []
    for doc in docs[:max_images]:
        url = doc.tags["uri_absolute"]
        filename = url.split("/")[-1]
        # !wget {url} -q
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)

        image = open(filename, "rb").read()
        widget = widgets.Image(value=image, format="jpg", width=300, height=400)
        image_list.append(widget)
    box = widgets.HBox(image_list)
    display.display(box)

def cleanup():
    os.rmdir("workspace")
    for item in os.listdir():
        if item.endswith(".jpg"):
            os.remove(item)
