"""
dict服务端
"""
from socket import *
from multiprocessing import Process
from dict_database import DictDatabase
import sys, signal, time

# 全局变量
Host = "192.168.139.130"
Port = 8080
Server_addr = (Host, Port)

# 实例化dict数据模块对象
db = DictDatabase()


# dict自定义进程类
class DictServe(Process):
    def __init__(self, conn_tcp):
        super().__init__()
        self.conn_tcp = conn_tcp

    def register(self, username, password):
        msg = db.add_user(username, password)
        if msg:
            self.conn_tcp.send(b"OK")
        else:
            self.conn_tcp.send(b"FAIL")

    def login(self, username, password):
        msg = db.dict_login(username, password)
        if msg:
            self.conn_tcp.send(b"OK")
        else:
            self.conn_tcp.send(b"FAIL")

    def list_word(self, word, username):
        msg = db.dict_list_word(word, username)
        if msg:
            self.conn_tcp.send(msg[0].encode())
        else:
            self.conn_tcp.send("没有这个单词".encode())

    def history(self, username):
        history_list = []
        msg = db.dict_list_history(username)
        if msg:
            for item in msg:
                msg = str(item[0]) + " " + str(item[-1])
                history_list.append(msg)
            data = "\n".join(history_list)
            self.conn_tcp.send(data.encode())
        else:
            self.conn_tcp.send("历史记录为空".encode())

    def run(self):
        db.create_cur()
        while True:
            data = self.conn_tcp.recv(1024).decode()
            tmp = data.split(" ")
            if not data or data == "E":
                return
            elif data[0] == "R":
                self.register(tmp[1], tmp[-1])
            elif data[0] == "L":
                self.login(tmp[1], tmp[-1])
            elif data[0] == "W":
                self.list_word(tmp[1], tmp[-1])
            elif data[0] == "H":
                self.history(tmp[-1])


# dict客户端启动函数
def main():
    sock_tcp = socket()
    sock_tcp.bind(Server_addr)
    sock_tcp.listen(5)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        conn_tcp, addr = sock_tcp.accept()
        print("From", addr)
        p = DictServe(conn_tcp)
        p.start()


if __name__ == '__main__':
    main()
