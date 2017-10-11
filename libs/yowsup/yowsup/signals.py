from blinker import signal

'''
System signals, you probably should't use this
'''

# Reply-type message or @tag ()
node_intercepted = signal('node_intercepted')