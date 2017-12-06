import sys, logging, config

from yowsup.layers.auth import AuthError
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST
from yowsup.stacks import YowStackBuilder
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer

from app.mac.layer import MacLayer

# Uncomment to log
#logging.basicConfig(level=logging.DEBUG)

# Config
credentials = (config.credentials['phone'], config.credentials['password'])
encryption = True


class MacStack(object):
    def __init__(self):
        builder = YowStackBuilder()

        self.stack = builder\
            .pushDefaultLayers(encryption)\
            .push(MacLayer)\
            .build()

        self.stack.setCredentials(credentials)
        self.stack.setProp(MacLayer.PROP_CONTACTS,  list(config.contacts.keys()))
        self.stack.setProp(PROP_IDENTITY_AUTOTRUST, True)

    def start(self):
        print("[Whatsapp] Mac started\n")

        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))

        try:
            self.stack.loop(timeout=0.5, discrete=0.5)
        except AuthError as e:
            print("Auth Error, reason %s" % e)
        except KeyboardInterrupt:
            print("\nYowsdown")
            sys.exit(0)
        
def instance():
    return MacStack()

if __name__ == "__main__":
    c = MacStack()
    c.start()