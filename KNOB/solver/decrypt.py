import random
import hashlib
import base64
from cryptography.fernet import Fernet

# 暗号化処理
# random.seed(PASSKEY) #PASSKEYを元に乱数を生成
# d = int(random.random() * (10 ** (int(setting)))) #setting桁の乱数を生成
# hash = hashlib.sha256(str(d).encode()) #乱数を元にハッシュを生成
# key = base64.urlsafe_b64encode(hash.digest()) #ハッシュを元にキーを生成
# cipher = f.encrypt(b"Hello world!") #暗号化

cipher = b"gAAAAABk_VSIX9HeVHOnE5qwSm1ZON-voBt5jyCUCRAlbrhyXwfO-M8HrQQVXaaou0-fk14EpshUefCMhAFwL7xXHUPtZYKlfCTyI9GUADxJCOEkwra80dmvGvr2GS7yT1XN3dLP2LzX"

d = 8
hash = hashlib.sha256(str(d).encode())
key = base64.urlsafe_b64encode(hash.digest())
f = Fernet(key)
plain = f.decrypt(cipher)
print(plain)