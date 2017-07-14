from blinker import signal

# Main signals
initialized = signal('mac_initialized')
message_received = signal('message_received')