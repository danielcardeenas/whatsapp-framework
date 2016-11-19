from ..utils import helper


class WAPoll(object):
    def __init__(self, instance, args, creator):
        self.instance = instance
        self.args = args
        self.args_len = len(args)
        self.creator = creator


    def send_poll(self):
        answer = "Encuesta: *" + self.title + "*" + "\n" + self.identifier + " para votar"
        self.instance.toLower(helper.make_message(answer, self.conversation))