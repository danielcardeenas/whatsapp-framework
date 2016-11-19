from app.utils import helper
from app.receiver.receiver import Receiver


class WAPoll(Receiver):
    def __init__(self, instance, args, creator, identifier):
        Receiver.__init__(self, identifier, creator, self.handle_answer())
        self.instance = instance
        self.args = args
        self.args_len = len(args)
        self.creator = creator

    def handle_answer(self, message_entity):
        print("Got answer")

    def send_poll(self):
        answer = "Encuesta: *" + self.title + "*" + "\n" + self.identifier + " para votar"
        self.instance.toLower(helper.make_message(answer, self.conversation))