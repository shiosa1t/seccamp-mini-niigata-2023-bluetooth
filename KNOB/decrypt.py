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