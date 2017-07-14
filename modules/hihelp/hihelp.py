from app.mac import mac, signals
from app.utils import helper

'''
Signals this module listents to:
1. When a message is received (signals.message_received)
==========================================================
'''
def handle(message):
    if message.command == "hi":
        hi(message)
    elif message.command == "help":
        help(message)

signals.message_received.connect(handle)

'''
Actual module code
==========================================================
'''
def hi(message):
    who_name = helper.sender_name(message.message_entity)
    answer = "Hi *" + who_name + "*"
    mac.send_message(answer, message.conversation)
    
def help(message):
    answer = "*Bot called mac* \nWhatsapp framework made in Python \n*Version:* 0.0.9 \n*Status:* Alpha \nhttps://github.com/danielcardeenas/whatsapp-framework"
    mac.send_message(answer, message.conversation)