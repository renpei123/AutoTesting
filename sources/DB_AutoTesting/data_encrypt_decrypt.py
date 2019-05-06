from cryptography.fernet import Fernet

def generateKey():
    cipher_key = Fernet.generate_key()
    return cipher_key

def strEncrypt(str,cipher):
    cipherText=cipher.encrypt(str)
    return cipherText

def strDecrypt(cipherText,cipher):
    str=cipher.decrypt(cipherText)
    return str

def main():
    #cipher_key=generateKey()
    cipher_key=b'nkr_hFoPzlhB4XPegNMRubCar3bezyNcxVqx116Avao='
    cipher = Fernet(cipher_key)
    #print(cipher)
    cipherText = strEncrypt(b'aug18aug',cipher)

    #cipherText=conf.get('db2', 'password')
    print(cipherText)
    str=strDecrypt(cipherText.encode('utf-8'),cipher).decode('utf-8')
    print(str)


if __name__ == "__main__":
    main()