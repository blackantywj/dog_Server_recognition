#coding=utf-8

import socket
import os
import time
import re
import xlrd
import threading
import socket

table_accz = [0,0,0,0,0,0,0]
table_Cta = [0,0,0,0,0,0,0]
pre = []
def Get_data(n):
    return  table.col_values(n)
def judgeFunc(flag,flag1,flag2):
    if flag == 0:
        print("坐！！！")
#    if flag1 == 1:
#        print("站到坐！！！！")
    if flag == 1 and flag1 == 1:
        print("趴！！！")
    if flag == 1 and flag1 == 0:
        print("站！！！")
    if flag == 1 and flag2 == 0:
        print("站！！！")
    if flag == 1 and flag2 == 1:
        print("趴！！！")
#=-(2*HEX2DEC(R3)-1)*(HEX2DEC(P3)*256+HEX2DEC(Q3))/100
#=-(2*HEX2DEC(AG436)-1)*(HEX2DEC(AE436)*256+HEX2DEC(AF436))/100
def slice_data(data):
    P = int(eval(hex(data[19])))
    Q = int(eval(hex(data[20])))
    R = int(eval(hex(data[21])))
    AE = int(eval(hex(data[34])))
    AF = int(eval(hex(data[35])))
    AG = int(eval(hex(data[36])))
    z_data = -(2 * R -1) * (P*256 + Q) /100
    C_data = -(2 * AG -1) * (AE * 256 + AF) /100
    return C_data,z_data
def prediction(table_Cta, table_accz):
    if(len(table_accz)>=5):
            flag = -2
            flag1 = -2
            flag2 = -2
            pre1 = table_Cta[0:5]
#            print(pre1)
            #        pre2 = table_accz[i+1, i+10]
            if (sum(pre1) / 5) > 35:
                flag = 0
                judgeFunc(flag, flag1, flag2)
            elif (sum(table_accz[0:4]) < 0):
                flag = 1
                flag1 = 1
                judgeFunc(flag, flag1, flag2)
            elif (sum(table_accz[0:4]) >= 0):
                flag = 1
                flag1 = 0
                judgeFunc(flag, flag1, flag2)
#  以下使用的是俯仰角大于20并accz小于/大于0.1来判断是否处于稳定状态下的站/趴
# while(table_accz[i] <= -0.1)
            if ((sum(pre1) / 5) > 20 and abs(table_accz[5]) < 0.1):
                flag = 1
                flag2 = 1
                judgeFunc(flag, flag1, flag2)
            if ((sum(pre1) / 5) < 20 and abs(table_accz[5]) < 0.1):
                flag = 1
                flag2 = 0
                judgeFunc(flag, flag1, flag2)

def tcp_server():
    s = socket.socket()
    host = '0.0.0.0'
    port = 12346
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    while True:
        sock, addr = s.accept()
        print('tcp client addr: ', addr)
        tcplink(sock, addr)
        t.start()

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    # in order to initial system every time, when a new connection is constructed, so set flag = 0
    while True:
        i=0
        clientData = sock.recv(1024)
#        print(clientData)
        if not clientData:
            print('disconnect')
            # set predictions_data = 5, represent disconnect
            break
 #       try:
 #           pickle_data = pickle.loads(client_data)
 #           print(pickle_data)
 #       except:
 #           print('pickle.loads error')
 #           break
            ## return sensor_data(3 kinds of data) and all_sensors_data(7 kinds of data)
 #           client_data = pickle.loads(clientData)
        Table_Cta, Table_accz = slice_data(clientData)
        while i<6:
            table_Cta[i] = Table_Cta
            table_accz[i] = Table_accz
            i+=1
        print(table_Cta)
        print(table_accz)
        prediction(table_Cta, table_accz)
    sock.close()
    print('Connection from %s:%s closed.' % addr)

def main():
    try:
        t1 = threading.Thread(target=web_server)
        t2 = threading.Thread(target=tcp_server)
        t1.start()
        t2.start()
    except:
        print('error:unable to start thread')
    while 1:
        pass

if __name__ == '__main__':
#    main()
    tcp_server()
