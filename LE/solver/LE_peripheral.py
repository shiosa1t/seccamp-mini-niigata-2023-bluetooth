import socket
import time

SIZE = 1024
ADVERTISE_MESSAGE = "BLE_ADVERTISE_PACKET"
REQUEST_MSSAGE = "BLE_REQUEST_PACKET"
RESPONSE_MESSAGE = "BLE_RESPONSE_PACKET"
GATT_dic = {"22B0": {"1E60": "Red", "1E61" : "0"}, "22B1" : {"15B0": "100"}}

address = ('127.0.0.1', 8888)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def advertise():
    try:
        time.sleep(5)
        print('Advertising...')
        message = ADVERTISE_MESSAGE
        sock.sendto(message.encode('utf-8'), address) #アドバタイズパケットを送信
        cent_meesage, addr = sock.recvfrom(SIZE) #待機
        cent_meesage = cent_meesage.decode(encoding='utf-8')
        if cent_meesage == REQUEST_MSSAGE:
            time.sleep(1)
            print('Found request packet!') #リクエストパケットを受信
            time.sleep(3)
            response(addr)

    except KeyboardInterrupt:
        sock.close()


def response(addr):
    try:
        print('Sending response...')
        message = RESPONSE_MESSAGE
        sock.sendto(message.encode(encoding='utf-8'), addr) #レスポンスパケットを送信
        time.sleep(1)
        print('Connected to Central!') #セントラルと接続
        time.sleep(1)
        peripheral(addr)

    except KeyboardInterrupt:
        sock.close()

def peripheral(addr):
    while True:
        try:
            cent_meesage, addr = sock.recvfrom(SIZE) #コマンドを受信
            cent_meesage = cent_meesage.decode(encoding='utf-8')
            if cent_meesage == 'exit':
                print('Disconnected')
                sock.close()
            if cent_meesage == 'read':
                time.sleep(1)
                cent_meesage, addr = sock.recvfrom(SIZE) #サービスUUIDを受信
                service_uuid = cent_meesage.decode(encoding='utf-8')
                cent_meesage, addr = sock.recvfrom(SIZE) #キャラクタリスティックUUIDを受信
                characteristic_uuid = cent_meesage.decode(encoding='utf-8')
                value = GATT_dic[service_uuid][characteristic_uuid]
                time.sleep(1)
                print("Read value: " + value)
                sock.sendto(value.encode(encoding='utf-8'), addr) #値を送信
            if cent_meesage == 'write':
                time.sleep(1)
                cent_meesage, addr = sock.recvfrom(SIZE) #サービスUUIDを受信
                service_uuid = cent_meesage.decode(encoding='utf-8')
                cent_meesage, addr = sock.recvfrom(SIZE) #キャラクタリスティックUUIDを受信
                characteristic_uuid = cent_meesage.decode(encoding='utf-8')
                cent_meesage, addr = sock.recvfrom(SIZE) #値を受信
                value = cent_meesage.decode(encoding='utf-8')
                GATT_dic[service_uuid][characteristic_uuid] = value #値を更新
                print("Updated GATT: ")
                print(GATT_dic)

        except KeyboardInterrupt:
            sock.close()
    

if __name__ == '__main__':
    advertise()