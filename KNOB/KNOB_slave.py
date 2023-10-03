import socket
import time
import random
import hashlib
import base64
from cryptography.fernet import Fernet

SIZE = 1024
PASSKEY = 123456
REQUEST_MESSAGE = "SECURITY_SETTING_REQUEST_KEY_LENGTH"
SECURITY_SETTING = "16"

host = 'localhost'
port = 55556

def slave():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    conn, _ = sock.accept() # マスタに接続

    time.sleep(3) # 3秒待つ
    send(REQUEST_MESSAGE, conn) # マスタにリクエストを送信
    time.sleep(1)
    send(SECURITY_SETTING, conn) # マスタにセキュリティ設定を送信
    setting = recieve(conn)
    # print(f"Received security setting: {setting}")


    random.seed(PASSKEY) # パスキーをシードに設定
    d = int(random.random() * (10 ** (int(setting)))) # setting桁の乱数を生成
    hash = hashlib.sha256(str(d).encode()) # 乱数を元にハッシュ化
    key = base64.urlsafe_b64encode(hash.digest()) # ハッシュを元にキーを生成
    f = Fernet(key)
    msg = recieve(conn) # msg = f.encrypt(b"Hello world!") 
    # print(msg)
    secret = b"flag{U_5ucceeded_in_KN0B_Att4ck!!}"
    secret = f.encrypt(secret) # シークレットを暗号化
    send_raw(secret, conn) # マスタにシークレットを送信

    sock.close()

def recieve(sock):
    try:
        msg, _ = sock.recvfrom(SIZE)
        decoded_msg = msg.decode()
        return decoded_msg
    except KeyboardInterrupt:
        sock.close()

def send(msg, sock):
    try:
        sock.sendall(msg.encode())
    except KeyboardInterrupt:
        sock.close()

def send_raw(msg, sock):
    try:
        sock.sendall(msg)
    except KeyboardInterrupt:
        sock.close()

if __name__ == "__main__":
    slave()
