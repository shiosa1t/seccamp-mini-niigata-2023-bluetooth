import socket
import time

SIZE = 1024
ADVERTISE_MESSAGE = "BLE_ADVERTISE_PACKET"
REQUEST_MSSAGE = "BLE_REQUEST_PACKET"
RESPONSE_MESSAGE = "BLE_RESPONSE_PACKET"

host = '127.0.0.1'
port = 8888
locaddr = (host, port)

sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)

sock.bind(locaddr)

def scan():
    try :
        print('Scanning...') #スキャン
        peri_message, addr = sock.recvfrom(SIZE) #待機
        peri_message = peri_message.decode(encoding='utf-8')
        if peri_message == ADVERTISE_MESSAGE:
            time.sleep(1)
            print('Found Bluetooth LE Device!') #アドバタイズパケットを受信
            time.sleep(3)
            request(addr)

    except KeyboardInterrupt:
        sock.close()


def request(addr):
    try:
        print('Sending request to Bluetooth LE Device...')
        sock.sendto(REQUEST_MSSAGE.encode(encoding='utf-8'), addr) #リクエストパケットを送信
        peri_message, addr = sock.recvfrom(SIZE) #待機
        peri_message = peri_message.decode(encoding='utf-8')
        if peri_message == RESPONSE_MESSAGE:
            time.sleep(1)
            print('Connected to Peripheral!') #ペリフェラルと接続
            time.sleep(1)
            central(addr)

    except KeyboardInterrupt:
        sock.close()


def central(addr):
    while True:
        cmd = input('Enter Command: ') #コマンドを入力
        if cmd == 'exit':
            time.sleep(1)
            sock.sendto(cmd.encode(encoding='utf-8'), addr)
            print('Disconnected')
            sock.close()
            break
        if cmd == 'read':
            time.sleep(1)
            sock.sendto(cmd.encode(encoding='utf-8'), addr) #サービスUUIDを入力
            service_uuid = input('Enter Service UUID: ')
            time.sleep(1)
            sock.sendto(service_uuid.encode(encoding='utf-8'), addr) #サービスUUIDを送信
            characteristic_uuid = input('Enter Characteristic UUID: ') #キャラクタリスティックUUIDを入力
            time.sleep(1)
            sock.sendto(characteristic_uuid.encode(encoding='utf-8'), addr) #キャラクタリスティックUUIDを送信
            peri_message, addr = sock.recvfrom(SIZE) #待機
            print('Value: ' + peri_message.decode(encoding='utf-8'))
        if cmd == 'write':
            time.sleep(1)
            sock.sendto(cmd.encode(encoding='utf-8'), addr) #サービスUUIDを入力
            service_uuid = input('Enter Service UUID: ')
            time.sleep(1)
            sock.sendto(service_uuid.encode(encoding='utf-8'), addr) #サービスUUIDを送信
            characteristic_uuid = input('Enter Characteristic UUID: ') #キャラクタリスティックUUIDを入力
            time.sleep(1)
            sock.sendto(characteristic_uuid.encode(encoding='utf-8'), addr) #キャラクタリスティックUUIDを送信
            value = input('Enter Value: ') #値を入力
            time.sleep(1)
            sock.sendto(value.encode(encoding='utf-8'), addr) #値を送信


if __name__ == '__main__':
    scan()