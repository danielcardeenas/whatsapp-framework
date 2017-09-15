from app.mac import mac, signals

'''
Signals this module listents to:
1. When a message is received (signals.command_received)
==========================================================
'''
@signals.command_received.connect
def handle(message):
    if message.command == "hi":
        hi(message)
    elif message.command == "help": 
        help(message)

'''
Actual module code
==========================================================
'''
def hi(message):
    who_name = message.who_name
    answer = "Hi " + who_name
    mac.send_message(answer, message.conversation)
    
def help(message):
    answer = "*Bot called mac* \nWhatsapp framework made in Python \n*Version:* 1.0.0 \n*Status:* Beta \nhttps://github.com/danielcardeenas/whatsapp-framework"
    mac.send_message(answer, message.conversation)
