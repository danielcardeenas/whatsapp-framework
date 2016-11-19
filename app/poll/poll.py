from ..utils import helper


class WAPoll(object):
    def __init__(self, instance, title, conversation, type="normal", identifier="+"):
        self.instance = instance
        self.title = title
        self.conversation = conversation
        self.type = type.lower()
        self.identifier = identifier

    def send_poll(self):
        if type == "grupo":
            self.send_group_poll()
        else:
            self.send_default_poll()

    def send_group_poll(self):
        answer = "Encuesta: *" + self.title + "*" + "\n@Tag para votar"
        self.instance.toLower(helper.make_message(answer, self.conversation))

    def send_default_poll(self):
        answer = "Encuesta: *" + self.title + "*" + "\n" + self.identifier + " para votar"
        self.instance.toLower(helper.make_message(answer, self.conversation))