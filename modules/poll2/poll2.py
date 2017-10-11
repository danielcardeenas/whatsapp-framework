from app.utils import helper
from app.mac import mac
from app.utils import helper

numbers = ["1⃣","2⃣","3⃣","4⃣","5⃣","6⃣","7⃣","8⃣","9⃣","🔟"]
active_polls = []

class Poll2(object):
    pass

'''
Tries to interpret the message as a command
'''
def handle_command(message):
    args = [x.strip() for x in message.predicate.split(',')]
    if len(args) <= 0:
        mac.send_message("_Invalid arguments for poll_", message.conversation)
    elif len(args) == 1:
        if args[0] == "finish":
            finish_poll(message.who, message.conversation)
            return
    elif len(args) >= 2:
        title = args[0]
        options = args[1:]
        options = options_dict(options[:10])
        create_poll(title, options, message.who, message.conversation)
            

def handle_vote(message):
    if conversation_has_poll(message.conversation):
        poll = get_poll(message.conversation)
        if message.text in numbers and poll is not None:
            vote(message.text, message.who, poll)


def get_poll(conversation):
    for poll in active_polls:
        if poll.conversation == conversation:
            return poll
            
    return None

def vote(identifier, who, poll):
    for option in poll.options:
        if option['id'] == identifier:
            if who not in option['voters']:
                option['votes'] += 1
                option['voters'].append(who)


def create_poll(title, options, who, conversation):
    if conversation_has_poll(conversation):
        mac.send_message("There is alreadya  poll2 in the chat", conversation)
        return
    poll = gen_poll(title, options, who, conversation)
    send_poll(poll)


def gen_poll(title, options, who, conversation):
    poll2 = Poll2()
    poll2.title = title
    poll2.options = options
    poll2.who = who
    poll2.conversation = conversation
    return poll2
    
    
def options_dict(options):
    _options = []
    for index, option in enumerate(options):
        _option = {}
        _option['votes'] = 0
        _option['text'] = option
        _option['id'] = numbers[index]
        _option['voters'] = []
        _options.append(_option)
        
    return _options

def send_poll(poll):
    poll.text = make_poll_text(poll)
    mac.send_message(poll.text, poll.conversation)
    active_polls.append(poll)


def make_poll_text(poll):
    answer = "Poll: *" + poll.title + "*"
    answer += make_options_text(poll.options)
    return answer


def make_options_text(options):
    text = ""
    for index, option in enumerate(options):
        text += "\n"
        text += numbers[index] + " " + option['text']
        
    return text


def finish_poll(who, conversation):
    for poll in active_polls:
        if poll.who == who and poll.conversation == conversation:
            send_results(poll)
            active_polls.remove(poll)
            
            
def send_results(poll):
    answer = "Poll: *" + poll.title + "*"
    answer += make_options_results(poll.options)
    mac.send_message(answer, poll.conversation)
    
    
def make_options_results(options):
    text = ""
    for index, option in enumerate(options):
        text += "\n"
        text += option['text'] + ": " + str(option['votes']) + " votes"
        
    return text
            
            
def conversation_has_poll(conversation):
    for poll in active_polls:
        if poll.conversation == conversation:
            return True
            
    return False