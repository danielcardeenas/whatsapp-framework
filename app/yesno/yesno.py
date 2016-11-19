import requests
from app.mac import mac

api_url = "https://yesno.wtf/api/"


class YesNo(object):
    def __init__(self, instance, conversation):
        self.instance = instance
        self.conversation = conversation
        self.caption = "Si"
        self.image_path = "app/images/yes.gif"
        self.get_yes_no()

    def get_yes_no(self):
        response = requests.get(api_url)
        json = response.json()
        self.caption = translate_caption(json["answer"])
        self.image_path = get_image(json["image"], self.caption)

    def send_yesno(self):
        mac.send_image(self.instance, self.conversation, self.image_path, self.caption)


def get_image(url, caption):
    path = "app/images/" + caption + ".gif"
    file = open(path, 'wb')
    file.write(requests.get(url).content)
    file.close()
    return path


def translate_caption(caption):
    if caption == "yes":
        return "Si"
    else:
        return "No"
