"""
dict客户端
"""
from socket import *
import sys, os

# 全局变量
Host = "192.168.139.130"
Port = 8080
Server_addr = (Host, Port)


# 二级界面
def view(dc, username):
    while True:
        print("============功能界面============")
        print("=====1:查询=====2:历史=====3:注销")
        cmd = int(input("请输入对应数字"))
        if cmd == 1:
            dc.do_word_list(username)
        elif cmd == 2:
            dc.do_history(username)
        elif cmd == 3:
            break
        else:
            print("输入有误,请重新输入")


# dict客户端类
class DicrClient:
    def __init__(self, sock_tcp):
        self.sock_tcp = sock_tcp

    def do_quit(self):
        self.sock_tcp.send(b"E")
        self.sock_tcp.close()
        sys.exit("谢谢使用")

    def do_register(self, username, password):
        msg = "R " + username + " " + password
        self.sock_tcp.send(msg.encode())
        data = self.sock_tcp.recv(1024).decode()
        if data == "OK":
            print("注册成功")
        else:
            print("用户已经存在,注册失败")

    def do_login(self, username, password):
        msg = "L " + username + " " + password
        self.sock_tcp.send(msg.encode())
        data = self.sock_tcp.recv(1024).decode()
        if data == "OK":
            return True
        else:
            return False

    def do_word_list(self, username):
        word = input("请输入单词:")
        msg = "W " + word + " " + username
        self.sock_tcp.send(msg.encode())
        data = self.sock_tcp.recv(1024).decode()
        print(data)

    def do_history(self, username):
        msg = "H " + username
        self.sock_tcp.send(msg.encode())
        data = self.sock_tcp.recv(1024).decode()
        print(data)


# 客户端启动函数
def main():
    sock_tcp = socket()
    dc = DicrClient(sock_tcp)
    sock_tcp.connect(Server_addr)
    while True:
        print("============登录界面============")
        print("=====1:注册=====2:登录=====3:退出")
        cmd = int(input("请输入对应数字"))
        if cmd == 1:
            username = input("请输入用户名:")
            password = input("请输入密码:")
            dc.do_register(username, password)
        elif cmd == 2:
            username = input("请输入用户名:")
            password = input("请输入密码:")
            msg = dc.do_login(username, password)
            if msg:
                view(dc, username)
            else:
                print("用户名或密码错误,请重新登录")
                continue
        elif cmd == 3:
            dc.do_quit()
        else:
            print("输入有误请重新输入")


if __name__ == '__main__':
    main()
