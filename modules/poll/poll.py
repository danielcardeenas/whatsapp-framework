from app.utils import helper
from app.receiver.receiver import Receiver
from app.receiver import receiver
from app.mac import mac
from modules.poll.voter import Voter

class WAPoll(Receiver):
    def __init__(self, instance, conversation, creator, title, identifier="#"):
        # Finish poll if user already has one in this conversation
        finish_my_poll(instance, creator, conversation)
        Receiver.__init__(self, identifier, conversation, creator, self.handle_answer)
        self.instance = instance
        self.title = title
        self.voters = []

    def handle_answer(self, message_entity=None):
        if message_entity is not None:
            voter = Voter(message_entity)
            if not any(voter.who == v.who for v in self.voters):
                self.voters.append(voter)
            print("Got vote")

    def send_poll(self):
        answer = "Encuesta: *" + self.title + "*" + "\n" + self.identifier + " para votar"
        mac.send_message(self.instance, answer, self.conversation)
        
    def is_creator(self, creator):
        return self.creator == creator
        
    def is_conversation(self, conversation):
        return self.conversation == conversation
        
    def voters_string(self):
        answer = ""
        for voter in self.voters:
            answer += "\n+ " + voter.who_name
            
        return answer

def finish_my_poll(self, creator, conversation):
    poll = poll_from_user_conversation(creator, conversation)
    if poll:
        message = "*" + poll.title + ":*\n"
        message += "Total: " + str(len(poll.voters))
        message += poll.voters_string()
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
