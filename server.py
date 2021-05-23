from tkinter import *
import socket
import os
from _thread import *
import mysql.connector
def updateAccountMap():
    mydb = mysql.connector.connect(
        host='remotemysql.com',
        user="CoJ5g2XnKq",
        password="L6QhRYcFVP",
        database="CoJ5g2XnKq"
    )
    SQL = mydb.cursor()
    SQL.execute("select * from TaiKhoan")
    data=SQL.fetchall()
    global AccountMap
    AccountMap={x:y for x,y in data}
def registerAccount(ACT,PSW):
    mydb = mysql.connector.connect(
        host='remotemysql.com',
        user="CoJ5g2XnKq",
        password="L6QhRYcFVP",
        database="CoJ5g2XnKq"
    )
    SQL = mydb.cursor()
    SQL.execute(f"insert into TaiKhoan values ('{ACT}','{PSW}')")
    mydb.commit()
def ALL():
    mydb = mysql.connector.connect(
        host='remotemysql.com',
        user="CoJ5g2XnKq",
        password="L6QhRYcFVP",
        database="CoJ5g2XnKq"
    )
    SQL = mydb.cursor()
    SQL.execute("select * from Sach")
    data=SQL.fetchall()
    global QUERY
    QUERY=[[x,y,z,t] for x,y,z,t in data]
def QR(a,b):
    mydb = mysql.connector.connect(
        host='remotemysql.com',
        user="CoJ5g2XnKq",
        password="L6QhRYcFVP",
        database="CoJ5g2XnKq"
    )
    SQL = mydb.cursor()
    SQL.execute(f"select * from Sach where {a} like '%{b}%'")
    data=SQL.fetchall()
    global QUERY
    QUERY=[[x,y,z,t] for x,y,z,t in data]
class ServerForm:
        def on_closing(self):
            root.deiconify()
            self.master.destroy()
            global Flag
            Flag=False
        def Turnoff(self):
            global Flag
            Flag=False
            root.destroy()
            return
        def __init__(self, master):
            master.geometry("200x25")
            self.master = master
            master.title("Server")
            self.Turnoff_button = Button(master, text="Turnoff",command=self.Turnoff)
            self.Turnoff_button.pack()
ServerSideSocket = socket.socket()
host = ''
port = 20044
ClientCount = 0
AccountMap={}
QUERY={}
updateAccountMap()
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    #print(str(e))
    pass

#print('The server is on.....')
ServerSideSocket.listen(5)
ServerSideSocket.settimeout(0.2)

def multi_threaded_sever(connection,stt):
    connection.sendall(str.encode('SERVER IS RUNNING'))
    global Flag
    while Flag:
        try:
            data = connection.recv(2048)
        except ConnectionResetError:
            #print(f"CLIENT {stt} DISCONNECTED: (ConnectionResetError)")
            break
        if not data:
            break
        data=data.decode('utf-8')
        #print(f'Server received from client {stt}: {data}')
        response = ""
        if data=='NEW CLIENT CONNECTED':
            response = f'HELLO CLIENT {stt}'
        data=data.split()
        if data[0]=='PING':
            response="OK"
        if data[0]=='QUERY':
            if data[1]=='ALL':
                ALL()
            if data[1]=='SELECT':
                try:
                    response==""
                    f = open(" ".join(data[2:]),'rb')
                    #print(f'Server sent to client {stt}: ' + " ".join(data[2:]))
                    l = f.read()
                    while (l):
                        connection.sendall(l)
                        l = f.read()
                        f.close()
                except FileNotFoundError:
                    response="FileError"
                    connection.sendall(str.encode(response))
                    continue
            if data[1][0]=='F':
                QR(data[1],data[2])
            response=""
            for i in QUERY:
                for j in i:
                    response+=j+','
                response+='\n'
                pass
        if data[0]=='REQUEST':
            if data[1]=='REGISTER':
                if data[2] in AccountMap.keys():
                    response="DENIED REGISTER EXITED"
                else:
                    response="ACCEPTED REGISTER"
                    registerAccount(data[2],data[3])
                updateAccountMap()
            if data[1]=='LOGIN':
                while len(data)<4:
                    data.append("")
                if data[2] in AccountMap.keys() and data[3] == AccountMap[data[2]]:
                    response = "ACCEPTED LOGIN"
                else:
                    response = "DENIED LOGIN"
        if response=="":
            continue
        connection.sendall(str.encode(response))
        #print(f'Server sent to client {stt}: ' + response)

        global ClientCount
    ClientCount=ClientCount-1
    connection.close()
    #print(f"CLIENT {stt} DISCONNECTED")
def Server():
    stt=0
    global Flag,ClientCount
    while Flag:
        try:
            Client, address = ServerSideSocket.accept()
        except socket.timeout:
            pass
        else:
            #print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(multi_threaded_sever, (Client,stt,))
            stt+=1
            ClientCount += 1
            #print('Thread Number: ' + str(ClientCount))
    ServerSideSocket.close()
Flag=True
root = Tk()
my_gui = ServerForm(root)
start_new_thread(Server,())
root.protocol("WM_DELETE_WINDOW", my_gui.on_closing)
root.mainloop()
#print("svh")