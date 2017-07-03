from app.libs.deuces import Card
from app.utils import helper
from app.receiver.receiver import Receiver
from app.receiver import receiver
from app.modules.mac import mac
from app.modules.poll.voter import Voter

class Poker(Receiver):
    def __init__(self, instance, conversation, creator, identifier="#"):
        # Finish poll if user already has one in this conversation
        finish_my_game(instance, creator, conversation)
        Receiver.__init__(self, identifier, conversation, creator, self.handle_answer)
        self.instance = instance
        self.voters = []

    def handle_answer(self, message_entity=None):
        if message_entity is not None:
            voter = Voter(message_entity)
            if not any(voter.who == v.who for v in self.voters):
                self.voters.append(voter)
            print("Got vote")

    def send_poll(self):
        answer = "Texas Hold'em"
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

def finish_my_game(self, creator, conversation):
    poll = poll_from_user_conversation(creator, conversation)
    if poll:
        message = "*Terminando juego anterior:*"
        mac.send_message(self, message, poll.conversation)
        poll.destroy()


def poll_from_user_conversation(creator, conversation):
    for poll in receiver.receivers:
        if is_Poker(poll):
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

def is_Poker(obj):
    return type(obj) is Poker
