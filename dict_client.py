import time
from socket import *
import sys

ADDR = ('127.0.0.1',9988)
class DictClient():
    def __init__(self, s):
        self.s = s
    def get_word(self,word,account):
        # 请单词响应
        msg = '查询单词'+' '+word+' '+account
        self.s.send(msg.encode())
        # 服务端给出应答
        data = self.s.recv(1024).decode()
        print(data)
    def find_record(self,account):
        msg = '查询记录'+' ' + account
        self.s.send(msg.encode())
        data = self.s.recv(1024).decode()
        print(data)
    def do_login(self):
        while True:
            # 发送登录账号跟密码给服务端
            account = input("请输入登录账号：")
            password = input("请输入登录密码：")
            msg = "登录"+" "+account+" "+password
            self.s.send(msg.encode())
            # 等待客户端验证
            data = self.s.recv(128).decode()
            if data == 'OK':
                while True:
                    print("""
                                  -----------命令菜单----------
                                  |          查询单词         |
                                  |          查询记录         |
                                  |            退出          |
                                  ----------------------------
                                  """)
                    cmd = input("输入命令：").strip()
                    if cmd == '查询单词':
                        word = input("请输入查询的单词：").strip()
                        self.get_word(word,account)
                    elif cmd =='查询记录':
                        self.find_record(account)
                    elif cmd == '退出':
                        return
                    else:
                        print("请输入正确命令")
            else:
                print("密码跟账号输入不符")
    # 注册
    def do_register(self):
        while True:
            name = input("请输入用户名：")
            password = input("请设置密码：")
            password_ = input("请再次输入密码：")
            if password != password_:
                print("两次密码不一致")
                continue
            if (" " in password_) or (" " in name):
                print("用户名或者密码不许有空格")
                continue
            msg = '注册'+" "+name+' '+password
            self.s.send(msg.encode())
            # 等待反馈
            data  = self.s.recv(128).decode()
            if data == 'OK':
                print("注册成功，欢迎",name)
                break
            else:
                print("注册失败！输入的昵称已被占用，你重新输入")
                continue

    def exit(self):
        self.s.send("退出".encode())
        sys.exit('退出程序')

# 网络搭建（和服务端建立通信，然后通过打印命令提示选择执行的功能）
def main():
    s = socket()
    s.connect(ADDR)
    dictor = DictClient(s) # 实例化对象
    #循环发送请求
    while True:
        print("""
                -----------命令菜单----------
                |            登录          |
                |            注册          |
                |            退出          |
                ----------------------------
                """)
        cmd = input("输入命令：").strip()
        if cmd == '登录':
            dictor.do_login()
        elif cmd == '注册':
            dictor.do_register()
        elif cmd == '退出':
            dictor.exit()
        else:
            print("请输入正确的命令")
if __name__ == '__main__':
    main()