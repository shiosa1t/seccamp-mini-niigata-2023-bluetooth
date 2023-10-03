import socket
import time
import random
import cryptography

SIZE = 1024

master_host = 'localhost'
master_port = 55555

slave_host = 'localhost'
slave_port = 55556
    
def mitm():
    master_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master_sock.bind((master_host, master_port))
    master_sock.listen(1) # マスタからの接続を待つ
    master_conn, _ = master_sock.accept() 
    time.sleep(5) # 5秒待つ
    slave_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    slave_sock.connect((slave_host, slave_port)) # スレーブに接続

###################################################################################################

    msg = recieve(slave_sock) # スレーブからのメッセージを受信
    send(msg, master_conn) # マスタにメッセージを送信

    msg = recieve(slave_sock) # スレーブからのメッセージを受信
    send(msg, master_conn) # マスタにメッセージを送信

    msg = recieve(master_conn) # マスタからのメッセージを受信
    send(msg, slave_sock) # スレーブにメッセージを送信

    msg = recieve(master_conn) # マスタからのメッセージを受信
    send(msg, slave_sock) # スレーブにメッセージを送信

    secret = recieve(slave_sock) # スレーブからのメッセージを受信
    send(secret, master_conn) # マスタにメッセージを送信

###################################################################################################

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

if __name__ == "__main__":
    mitm()
