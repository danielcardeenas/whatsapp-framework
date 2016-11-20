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


def finish_my_poll(self, creator, conversation):
    poll = get_poll_from_user_conversation(creator, conversation)
    if poll:
        message = "*" + poll.title + "*\nVotos: " + str(poll.votes)
        mac.send_message(self, message, poll.conversation)

    # Make sure to remove the poll from this creator
    remove_poll_from_receivers(creator, conversation)


def get_poll_from_user_conversation(creator, conversation):
    for poll in receiver.receivers:
        if is_poll_from_creator(poll, creator) and is_poll_from_conversation(poll, conversation):
            return poll

    return None


def remove_poll_from_receivers(creator, conversation):
    receiver.receivers[:] = [poll for poll in receiver.receivers if not is_poll_from_creator(poll, creator)
                             and not is_poll_from_conversation(poll, conversation)]


def is_poll_from_creator(poll, creator):
    return type(poll) is WAPoll and poll.creator == creator


def is_poll_from_conversation(poll, conversation):
    return poll.conversation == conversation
