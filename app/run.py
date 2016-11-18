import sys, logging

from yowsup.layers.auth import AuthError
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST
from yowsup.stacks import YowStackBuilder
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer

from layer import MacLayer

# Uncomment to log
# logging.basicConfig(level=logging.DEBUG)

# Config
#################################################################

# Phone, password (Replace with your own, there ones are fake as fck)
credentials = ("5218111287273", "5Fq+tw5f4y782DCAUdA3X//TJKx=")
encryptionEnabled = True

# Add contacts here
contacts = {
    "5218114140740": "Daniel Cardenas",
    "5218115112713": "Otniel"
}


class MacStack(object):
    def __init__(self):
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(MacLayer)\
            .build()

        self.stack.setCredentials(credentials)
        self.stack.setProp(MacLayer.PROP_CONTACTS, contacts.keys())
        self.stack.setProp(PROP_IDENTITY_AUTOTRUST, True)

    def start(self):
        print("[Whatsapp] Mac started\n")

        # Idk what is this
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))

        try:
            self.stack.loop(timeout=0.5, discrete=0.5)
        except AuthError as e:
            print("Auth Error, reason %s" % e)
        except KeyboardInterrupt:
            print("\nYowsdown")
            sys.exit(0)

if __name__ == "__main__":
    c = MacStack()
    c.start()
