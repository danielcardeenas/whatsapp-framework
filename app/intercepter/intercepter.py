from yowsup import signals as yowsup_singals

# Tuple: (node, serialized_data)
@yowsup_singals.node_intercepted.connect
def handle_intercept(data_tuple):
    pass
    #print("Node:", data_tuple[0].toString())
    #print("Tuple", data_tuple)