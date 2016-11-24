from app.utils import helper
from app.receiver.receiver import Receiver
from app.receiver import receiver
from app.mac import mac


class WAPoll(Receiver):
    def __init__(self, instance, conversation, creator, title, identifier="#"):
        # Allow only one poll per user-conversation
        if user_has_poll(creator, conversation):
            mac.send_message(self.instance, "_Tienes una poll activa_", conversation)
            return
        
        Receiver.__init__(self, identifier, conversation, creator, self.handle_answer)
        self.instance = instance
        self.title = title
        self.votes = 0

    def handle_answer(self, message_entity=None):
        print(self)
        if self is not None:
            self.votes += 1
            print("Got vote: " + str(self.votes))

    def send_poll(self):
        answer = "Encuesta: *" + self.title + "*" + "\n" + self.identifier + " para votar"
        mac.send_message(self.instance, answer, self.conversation)
        
    def is_creator(self, creator):
        return self.creator == creator
        
    def is_conversation(self, conversation):
        return self.conversation == conversation


def finish_my_poll(self, creator, conversation):
    poll = poll_from_user_conversation(creator, conversation)
    if poll:
        message = "*" + poll.title + "*\nVotos: " + str(poll.votes)
        mac.send_message(self, message, poll.conversation)
        poll.destroy()


def poll_from_user_conversation(creator, conversation):
    for poll in receiver.receivers:
        if is_WAPoll(poll):
            if poll.is_creator(creator):
                if poll.is_conversation(conversation):
                    return poll

    return None
    
    
def user_has_poll(creator, conversation):
    for poll in receiver.receivers:
        if poll.is_creator(creator):
            if poll.is_conversation(conversation):
                return True
                
    return False

def is_WAPoll(obj):
    return type(obj) is WAPoll
