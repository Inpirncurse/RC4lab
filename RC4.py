import fileinput
import re

def KSA(key):
    key_len = len(key)
    S = [0] * 256
    j = 0
    
    for i in range(256):
        S[i] = i

    for i in range(256):
        j = (j + S[i] + key[i % key_len]) % 256
        S[i], S[j] = S[j], S[i] 

    return S

i = 0
j = 0
def PRGA(S):
    global i
    global j

    i = (i + 1) % 256
    j = (j + S[i]) % 256

    S[i], S[j] = S[j], S[i]  
    K = S[(S[i] + S[j]) % 256]
    return K

def get_keystream(key):
    S = KSA(key)
    return PRGA(S)

def encrypt_logic(key, text):
    keystream = KSA([ord(c) for c in key])
 
    res = []
    for c in text:
        val = (c ^ PRGA((keystream)))
        val = ("%02X" %  val)
        
        res.append(val)
    return ''.join(res)

def encrypt(key, plaintext):
    plaintext = [ord(c) for c in plaintext]
    return encrypt_logic(key, plaintext)

def decrypt(key, ciphertext):
    global i 
    global j

    i = j = 0

    ciphertext = re.findall('..', ciphertext)
    
    ct = []
    for c in ciphertext:
        ct.append(int(c, 16))

    h = re.findall('..', encrypt_logic(key, ct))

    text = ""
    for c in h:
        text += chr(int(c, 16))

    return text

   


def main():
    lines = []
    for line in fileinput.input():
        #print(line)
        lines.append(line.rstrip())
    
    key = lines[0]
    plaintext = lines[1]

    
    for line in plaintext:
        lines.append(line)
            

    crypto = encrypt(key, plaintext)

    decrypted = decrypt(key, crypto)

    #print('plaintext:', plaintext)
    print(crypto)
    #print('decrypted:', decrypted)



   

if __name__ == '__main__':
    main()