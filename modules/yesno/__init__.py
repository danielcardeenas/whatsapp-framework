from app.mac import signals
from modules.yesno.yesno import YesNo

'''
Signals this module listents to:
+ When a message is received (signals.message_received)
==========================================================
'''
@signals.message_received.connect
def handle(message):
    if message.command == "siono":
        yesno = YesNo(message.conversation)
        yesno.send_yesno()