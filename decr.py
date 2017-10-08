import os, hashlib
import hmac
import binascii

from Crypto.Cipher import AES
from axolotl.kdf.hkdfv3 import HKDFv3
from axolotl.util.byteutil import ByteUtil

def decryptImg(img, refkey):
    derivative = HKDFv3().deriveSecrets(binascii.unhexlify(refkey),
                                        binascii.unhexlify("576861747341707020496d616765204b657973"), 112)
                                        
    parts = ByteUtil.split(derivative, 16, 32)
    iv = parts[0]
    cipherKey = parts[1]
    macKey = derivative[48:80]

    #mac = hmac.new(macKey,digestmod=hashlib.sha256)
    #mac.update(iv)

    cipher = AES.new(key=cipherKey, mode=AES.MODE_CBC, IV=iv)
    
    chunk_size = 4096 * 10
    with open(img, "rb") as in_file:
        with open("app/assets/images/boujee.jpeg", "wb") as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                try:
                    piece = cipher.decrypt(chunk)
                except:
                    piece = cipher.decrypt(pad(chunk))
                    
                if len(chunk) == 0:
                    break # end of file
        
                out_file.write(piece)
    
def pad(s):
    # return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    y = (16 - len(s) % 16) * chr(16 - len(s) % 16)
    a = s + y.encode()
    return a

if __name__ == "__main__":
    mediaKey = b'\x1b\x9d7\xda(zR\x07\xf9z\xb1\x01\xa57\x94?\xb9\xf5\xff_\x9fd}\xf6\xef\xd6\xdcT\x8b\x90/Q'
    
    #f = open("app/assets/images/tmpru4axiie.enc", 'rb')
    #stream = f.read()
    #f.close()
    f = "app/assets/images/tmpru4axiie.enc"
    
    refkey = binascii.hexlify(mediaKey)
    decryptImg(f, refkey)