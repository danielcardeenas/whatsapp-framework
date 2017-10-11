from app.utils import helper
from app.mac import mac
from modules.poll.voter import Voter

active_polls = []

class WAPoll(object):
    def __init__(self, conversation, creator, title, identifier="✋"):
        # Finish poll if user already has one in this conversation
        self.finish_my_poll(creator, conversation)
        
        # Basic attributes
        self.title = title
        self.voters = []
        
        # Conversation where the poll was created
        self.conversation = conversation
        # Vote identifier
        self.identifier = identifier
        # who object
        self.creator = creator
        
    def put_vote(self, voter):
        # If haven't already voted in this poll
        if not any(voter.who == v.who for v in self.voters):
            self.voters.append(voter)

    def send(self):
        answer = "Poll: *" + self.title + "*" + "\n" + self.identifier + " to vote"
        mac.send_message(answer, self.conversation)
        
        # Add poll to active polls
        active_polls.append(self)
        
    def is_creator(self, creator):
        return self.creator == creator
        
    def is_conversation(self, conversation):
        return self.conversation == conversation
        
    def voters_print(self):
        answer = ""
        for voter in self.voters:
            answer += "\n+ " + voter.who_name
            
        return answer
        
    
    '''
    Active polls management
    ===================================================================
    '''
    
    '''
    Decides if the message should be interpreted as a vote for a poll
    Or should be interpreted as a poll command
    '''
    @classmethod
    def handle_vote(self, message):
        for poll in active_polls:
            if poll.identifier in message.text:
                if poll.is_conversation(message.conversation):
                    poll.put_vote(Voter(message))
    
    '''
    Tries to interpret the message as a command
    '''
    @classmethod
    def handle_command(self, message):
        args = [x.strip() for x in message.predicate.split(',')]
        # Case: Invalid arguments
        if len(args) <= 0:
            mac.send_message("_Invalid arguments for poll_", message.conversation)
        
        # Case: Valid arguments
        elif len(args) >= 1:
            # Case: finish poll
            if args[0] == "finish":
                WAPoll.finish_my_poll(message.who, message.conversation)
                return
            # Case: create poll (default vote identifier)
            elif len(args) == 1:
                title = args[0]
                poll = WAPoll(message.conversation, message.who, title)
                poll.send()
            
            # Case: create poll (vote identifier specified)
            elif len(args) >= 2:
                title = args[0]
                identifier = args[1]
                poll = WAPoll(message.conversation, message.who, title, identifier)
                poll.send()
                
    
    '''
    Finds the poll of this user in this conversation
    Finishes the poll
    '''
    @classmethod
    def finish_my_poll(self, creator, conversation):
        poll = poll_from_user_conversation(creator, conversation)
        if poll:
            message = "*" + poll.title + ":*\n"
            message += "Total: " + str(len(poll.voters))
            message += poll.voters_print()
            mac.send_message(message, poll.conversation)
            active_polls.remove(poll)
            
            
'''
Finds a poll by it's creator and its conversation
'''
def poll_from_user_conversation(creator, conversation):
    for poll in active_polls:
        if poll.is_creator(creator):
            if poll.is_conversation(conversation):
                return poll

    return None
    

def is_WAPoll(obj):
    return type(obj) is WAPoll
