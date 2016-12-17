from app.utils import helper
from app.receiver.receiver import Receiver
from app.receiver import receiver
from app.mac import mac
from app.poll.voter import Voter

identifiers = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
class PollKing(Receiver):
    def __init__(self, instance, conversation, creator, predicate):
        self.instance = instance
        self.predicate = predicate
        self.voters = []
        self.identifier = "__global__"
        self.title = self.make_title(predicate)
        self.candidates = self.make_candidates(predicate)
        
        # Finish poll if user already has one in this conversation
        finish_my_poll(instance, creator, conversation)
        Receiver.__init__(self, self.identifier, conversation, creator, self.handle_answer)
        
    def make_title(self, predicate):
        args = [x.strip() for x in predicate.split(',')]
        # If no args
        if len(args) <= 0:
            mac.send_message(self.instance, "_Argumentos invalidos_", self.conversation)
            return
        else:
            return args[0]
    
    def make_candidates(self, predicate):
        # args = <title>, <candidates>...
        args = [x.strip() for x in predicate.split(',')]
        
        # If no args
        if len(args) <= 0:
            mac.send_message(self.instance, "_Argumentos invalidos_", self.conversation)
            return
        
        # Valid args:
        if len(args) > 1:
            candidates = []
            for candidate in args[1:]:
                candidates.append(candidate)
                
            return candidates
        else:
            return None

    def handle_answer(self, message_entity=None):
        if message_entity is not None:
            if self.should_handle(message_entity):
                print("Got vote")
            
    def should_handle(self, message_entity):
        message = message_entity.getBody()
        if message in identifiers:
            return True
        else:
            return False
    
    def send_poll(self):
        answer = "*" + self.title + "*"
        number = 1
        for candidate in self.candidates:
            answer += "\n"
            answer += get_unicode_number(number)
            answer += " " + candidate
            number += 1
            
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
        

def get_unicode_number(number):
    return identifiers[number]

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
        if is_PollKing(poll):
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

def is_PollKing(obj):
    return type(obj) is PollKing
