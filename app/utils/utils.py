'''
Check if bytes tring (serialized) contains the whatsapp '@' tag bytes
'''
def has_tags(serialized):
    tag_bytes = b'\x8a\x01\x1ez\x1c'
    return tag_bytes in serialized
    

'''
Returns the tags in the message
'''
def get_tags(serialized):
    if has_tags(serialized):
        return []
    else:
        return None
    

def get_conversation_from_node(node):
    pass