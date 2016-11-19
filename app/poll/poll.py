from ..utils import helper


class WAPoll(object):
    def __init__(self, instance, title, conversation):
        self.instance = instance
        self.title = title
        self.conversation = conversation

    def sendPoll(self):
        answer = self.title + "\n" + "Message from poll"
        self.instance.toLower(helper.make_message(answer, self.conversation))
