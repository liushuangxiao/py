from Crypto.Cipher import Blowfish


def decrypt(password) :
    c1 = Blowfish.new('5F B0 45 A2 94 17 D9 16 C6 C6 A2 FF 06 41 82 B7'.replace(' ','').decode('hex'), Blowfish.MODE_CBC, '\x00'*8)
    c2 = Blowfish.new('24 A6 3D DE 5B D3 B3 82 9C 7E 06 F4 08 16 AA 07'.replace(' ','').decode('hex'), Blowfish.MODE_CBC, '\x00'*8)
    padded = c1.decrypt(c2.decrypt(password.decode('hex'))[4:-4])
    p = ''
    while padded[:2] != '\x00\x00' :
        p += padded[:2]
        padded = padded[2:]
    return p.decode('UTF-16')

print decrypt("u013151311331277c47fcde8d41de44a5c5cf4859237af878d871ef9073115496");