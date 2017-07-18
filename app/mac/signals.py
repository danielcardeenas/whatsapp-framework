from blinker import signal

'''
Life cycle
'''

initialized = signal('mac_initialized')


'''
Messages
'''

# Simple message
message_received = signal('message_received')