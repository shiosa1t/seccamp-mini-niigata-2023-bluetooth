import socket
import time
import random
import hashlib
import base64
from cryptography.fernet import Fernet

SIZE = 1024
PASSKEY = 123456
REQUEST_MESSAGE = "SECURITY_SETTING_REQUEST_KEY_LENGTH"

host = 'localhost'
port = 55555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port)) # スレーブに接続 (MITM)

def master():
    req_msg = recieve()
    if req_msg == REQUEST_MESSAGE:
        # print("Received security request")
        setting = recieve() # セキュリティ設定を受信
        # print(f"Received security setting: {setting}")
        time.sleep(1)
        send(setting) # セキュリティ設定を送信

        random.seed(PASSKEY) # パスキーをシードに設定
        d = int(random.random() * (10 ** (int(setting)))) # setting桁の乱数を生成
        hash = hashlib.sha256(str(d).encode()) # 乱数を元にハッシュ化
        key = base64.urlsafe_b64encode(hash.digest()) # ハッシュを元にキーを生成
        f = Fernet(key)
        msg = f.encrypt(b"Hello world!") # メッセージを暗号化
        send_raw(msg) # スレーブにメッセージを送信
        secret = recieve() # シークレットを受信
        # print(secret) # シークレットを出力

        sock.close()

def recieve():
    try:
        msg, _ = sock.recvfrom(SIZE)
        decoded_msg = msg.decode()
        return decoded_msg
    except KeyboardInterrupt:
        sock.close()

def send(msg):
    try:
        sock.sendall(msg.encode())
    except KeyboardInterrupt:
        sock.close()

def send_raw(msg):
    try:
        sock.sendall(msg)
    except KeyboardInterrupt:
        sock.close()

if __name__ == "__main__":
    master()
