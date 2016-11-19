from app.mac import mac

class YesNo(object):
    def __init__(self, instance, caption, conversation):
        self.caption = caption
        self.instance = instance
        self.conversation = conversation
        self.image_path = "app/images/yes.gif"

    def send_yesno(self):
        mac.send_image(self.intance, self.conversation, self.image_path, self.caption)
