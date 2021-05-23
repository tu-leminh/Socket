from tkinter import *
import socket
import ipaddress
from tkinter import messagebox
def CheckServerIsOn():
    try:
        s.settimeout(3)
        s.sendall(b'PING')
        data = s.recv(1024)
        #print(data)
        s.settimeout(60)
    except socket.error or TimeoutError or BrokenPipeError:
        messagebox.showerror("Server dang offline", "Thoat chuong trinh")
        global exitflag
        exitflag=1
        root.destroy()
        return False
        s.settimeout(60)
    s.settimeout(60)
    return True
class ConnectForm:
    def on_closing(self):
        root.deiconify()
        self.master.destroy()
        global exitflag
        exitflag=1
    def GetHost(self):
        global HOST,exitflag
        HOST=self.entry.get()
        try:
            socket.inet_pton(socket.AF_INET,HOST)
            s.settimeout(1)
            #print("Connect to: ",HOST)
            s.connect((HOST, PORT))
            data = s.recv(1024)
            #print(data)
            s.sendall(b'NEW CLIENT CONNECTED')
            data = s.recv(1024)
            #print(data)
            s.settimeout(60)
        except socket.error or TimeoutError:
            messagebox.showerror("Chuong trinh se thoat", "IP server khong dung hoac khong hop le")
            global exitflag
            exitflag=1
            self.entry.delete(0, 'end')
            exitflag=1
            root.destroy()
        else:
            root.destroy()
        
    def __init__(self, master):
        self.master = master
        master.title("Connect")
        
        self.label = Label(master, text="Please connect to a server:")
        self.label.pack()

        self.entry = Entry(master)
        self.entry.pack()

        self.connect_button = Button(master, text="Connect",command=self.GetHost)
        self.connect_button.pack()
    
class RegisterForm:
    def on_closing(self):
        root.deiconify()
        self.master.destroy()
        global exitflag
        exitflag=1
    def Register_click(self):
        if not(CheckServerIsOn()):
            return
        global ACT
        global PSW
        ACT=self.account_entry.get()
        PSW=self.password_entry.get()
        if (PSW==self.repassword_entry.get()):
            messagebox.showinfo("Xin hay cho","Qua trinh dang ky co the mat den 30s")
            s.settimeout(60)
            s.sendall(bytes(f"REQUEST REGISTER {ACT} {PSW}", encoding='utf-8'))
            data = s.recv(2048)
            data = data.decode('utf-8')
            #print(data)
            data=data.split()
            if (data[0]=="DENIED" and data[2]=="EXITED"):
                messagebox.showerror("Tai khoan da ton tai","Vui long chon tai khoan khac" )
            if (data[0]=="ACCEPTED"):
                messagebox.showinfo("Dang ky thanh cong","Chuan bi login bang tai khoan dang ky")
                root.deiconify()
                self.master.destroy()
        else:
            messagebox.showerror("Xin nhap lai","Mat khau khong trung khop" )
            
        
    def __init__(self,master):
        self.master=master
        master.title("Register")
        def on_click_account(event):
            self.account_entry.configure(state=NORMAL)
            self.account_entry.delete(0, END)
            self.account_entry.unbind('<Button-1>', on_click_id_account)
        def on_click_password(event):
            self.password_entry.configure(state=NORMAL)
            self.password_entry.delete(0, END)
            self.password_entry.unbind('<Button-1>', on_click_id_password)
            self.password_entry.config(show="*")
        def on_click_repassword(event):
            self.repassword_entry.configure(state=NORMAL)
            self.repassword_entry.delete(0, END)
            self.repassword_entry.unbind('<Button-1>', on_click_id_repassword)
            self.repassword_entry.config(show="*")
            
        self.account_entry = Entry(master)
        self.account_entry.pack()
        self.account_entry.insert(0, "Account")
        #self.account_entry.configure(state=DISABLED)
        on_click_id_account = self.account_entry.bind('<Button-1>', on_click_account)
        
        self.password_entry = Entry(master)
        self.password_entry.pack()
        self.password_entry.insert(0, "Password")
        #self.password_entry.configure(state=DISABLED)
        on_click_id_password = self.password_entry.bind('<Button-1>', on_click_password)
        
        self.repassword_entry = Entry(master)
        self.repassword_entry.pack()
        self.repassword_entry.insert(0, "rePassword")
        #self.password_entry.configure(state=DISABLED)
        on_click_id_repassword = self.repassword_entry.bind('<Button-1>', on_click_repassword)

        self.register_button = Button(master, text="Register",width=10,command=self.Register_click)
        self.register_button.pack()
class LoginForm:
    def on_closing(self):
        root.deiconify()
        self.master.destroy()
        global exitflag
        exitflag=1
    def Login_click(self):
        if not(CheckServerIsOn()):
            return
        global PSW,ACT
        PSW=self.password_entry.get()
        ACT=self.account_entry.get()
        #print(f"REQUEST LOGIN {ACT} {PSW}")
        s.sendall(bytes(f"REQUEST LOGIN {ACT} {PSW}", encoding='utf-8'))
        data = s.recv(1024)
        #print(data)
        data=data.decode('utf-8').split()
        if (data[0]=='DENIED'):
            messagebox.showerror("Sai thong tin","Vui long nhap lai tai khoan va mat khau" )
        else:
            root.destroy()
    def Register_click(self):
        global PSW,ACT
        root.withdraw()
        sub= Tk()
        RF=RegisterForm(sub)
        sub.protocol("WM_DELETE_WINDOW", RF.on_closing)
        sub.mainloop()
        
        
    def __init__(self,master):
        def on_click_account(event):
            self.account_entry.configure(state=NORMAL)
            self.account_entry.delete(0, END)
            self.account_entry.unbind('<Button-1>', on_click_id_account)
        def on_click_password(event):
            self.password_entry.configure(state=NORMAL)
            self.password_entry.delete(0, END)
            self.password_entry.unbind('<Button-1>', on_click_id_password)
            self.password_entry.config(show="*")
            
        self.master = master
        master.title("Login")
        
        self.label = Label(master, text="Please login the account:")
        self.label.pack()

        self.account_entry = Entry(master)
        self.account_entry.pack()
        self.account_entry.insert(0, "Account")
        #self.account_entry.configure(state=DISABLED)
        on_click_id_account = self.account_entry.bind('<Button-1>', on_click_account)
        
        self.password_entry = Entry(master)
        self.password_entry.pack()
        self.password_entry.insert(0, "Password")
        #self.password_entry.configure(state=DISABLED)
        on_click_id_password = self.password_entry.bind('<Button-1>', on_click_password)

        self.login_button = Button(master, text="Login",width=10,command=self.Login_click)
        self.login_button.pack()
        
        self.register_button = Button(master, text="Register",width=10,command=self.Register_click)
        self.register_button.pack()
    
class MainForm:
    def on_closing(self):
        root.deiconify()
        self.master.destroy()
        global exitflag
        exitflag=1
    def Loading(self):
        self.eula.delete('1.0', END)
        self.eula.insert("1.0", 'Loading...')
        self.eula.update()
        self.Command_click()
    def recvall(self,sock):
        BUFF_SIZE = 4096
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data
    
    def Getfile(self,name):
        with open(name, 'wb') as f:
            data=self.recvall(s)
            #print(data)
            if data==b"FileError":
                return 0
            f.write(data)
        return 1
    def Command_click(self):
        if self.command_entry.get()=="":
            return
        data=f"QUERY {self.command_entry.get()}".split()
        if data[1] not in ["F_ID", "F_NAME" ,"F_TYPE", "F_AUTHOR" ,"ALL" ,"SELECT"] or (data[1]!="ALL" and len(data)==2):
            self.eula.delete("1.0",END)
            self.eula.insert("1.0", "Lenh khong hop le!!")
            return
        if not(CheckServerIsOn()):
            return
        try:
            s.sendall(bytes(f"QUERY {self.command_entry.get()}", encoding='utf-8'))
        except BrokenPipeError:
            CheckServerIsOn()
        if data[1]=='SELECT':

            FileExist=self.Getfile("D_"+" ".join(data[2:]))
            #print(self.command_entry.get()[-3:-1])
            if FileExist==0:
                self.eula.delete("1.0",END)
                self.eula.insert("1.0", "Sach khong ton tai hoac bi loi!!")
            else:
                if self.command_entry.get()[-3:]=='txt':
                    with open("D_"+" ".join(data[2:]), 'r') as f:
                        data=f.read()
                        self.eula.delete('1.0', END)
                        self.eula.insert("1.0", data)
                else:
                    self.eula.delete("1.0",END)
                    self.eula.insert("1.0", "File da tai nhung khong ho tro de doc truc tiep!!")
        else:
            data = s.recv(2048)
            data = data.decode('utf-8')
            #print(data)
            self.eula.delete('1.0', END)
            self.eula.insert("1.0", data)

    def __init__(self,master):
        self.master = master
        master.title("Library")
                
        self.scroll = Scrollbar(master)
        self.scroll.pack(side=LEFT,fill=Y)
        self.eula = Text(master, wrap=NONE, yscrollcommand=self.scroll.set)
        self.eula.insert("1.0", "Hello")
        self.eula.pack(anchor = "n",fill=X)
        self.scroll.config(command=self.eula.yview)
        
        self.label = Label(master,justify=LEFT, text="Commands: F_ID, F_NAME ,F_TYPE, F_AUTHOR ,ALL ,SELECT.")
        self.label.pack(side=LEFT)
        self.command_entry = Entry(master)
        self.command_entry.pack(side=BOTTOM,fill=X)
        
        self.command_button = Button(master, text="Enter",width=50,command=self.Loading)
        self.command_button.pack(side=BOTTOM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    PORT = 20044
    HOST = ""
    ACT=""
    PSW=""
    exitflag=0
    root = Tk()
    my_gui = ConnectForm(root)
    root.protocol("WM_DELETE_WINDOW", my_gui.on_closing)
    root.mainloop()
    while exitflag==0:
        root = Tk()
        my_gui = LoginForm(root)
        root.protocol("WM_DELETE_WINDOW", my_gui.on_closing)
        root.mainloop()
        if exitflag==1:
            break
        break
    if exitflag==0:
        root = Tk()
        my_gui = MainForm(root)
        root.protocol("WM_DELETE_WINDOW", my_gui.on_closing)
        root.mainloop()