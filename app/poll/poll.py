from app.utils import helper
from app.receiver.receiver import Receiver
from app.receiver import receiver
from app.mac import mac


class WAPoll(Receiver):
    def __init__(self, instance, conversation, creator, title, identifier="#"):
        Receiver.__init__(self, identifier, creator, self.handle_answer)
        self.instance = instance
        self.creator = creator
        self.title = title
        self.conversation = conversation
        self.votes = 0

    def handle_answer(self, message_entity=None):
        self.votes += 1
        print("Got vote: " + str(self.votes))

    def send_poll(self):
        answer = "Encuesta: *" + self.title + "*" + "\n" + self.identifier + " para votar"
        self.instance.toLower(helper.make_message(answer, self.conversation))


def finish_my_poll(self, creator):
    poll = get_poll_from_user(creator)
    if poll:
        message = "*" + poll.title + "*\nVotos: " + str(poll.votes)
        mac.send_message(self, message, poll.conversation)

    # Make sure to remove the poll from this creator
    remove_poll_from_receivers(creator)


def get_poll_from_user(creator):
    for poll in receiver.receivers:
        if is_poll_from_creator(poll, creator):
            return poll

    return None


def remove_poll_from_receivers(creator):
    receiver.receivers[:] = [poll for poll in receiver.receivers if is_poll_from_creator(poll, creator)]


def is_poll_from_creator(poll, creator):
    return type(poll) is WAPoll and poll.creator == creator