from blinker import signal

'''
Life cycle
'''

initialized = signal('mac_initialized')


'''
Messages
'''

message_received = signal('message_received') # Plain message
command_received = signal('command_received') # !<command>