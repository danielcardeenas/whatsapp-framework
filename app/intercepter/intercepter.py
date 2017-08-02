from yowsup import signals as yowsup_singals
from app.utils import utils

'''
Tuple: (node, serialized_data)
'''
@yowsup_singals.node_intercepted.connect
def handle_intercept(data_tuple):
    if utils.has_tags(data_tuple[1]):
        pass
    #print("Node:", data_tuple[0].toString())