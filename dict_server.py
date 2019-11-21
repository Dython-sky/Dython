import signal
from multiprocessing import Process
import sys
from socket import *
from 在线词典项目.dict_data import Database

HOST = '0.0.0.0'
PORT = 9988
ADDR = (HOST,PORT)
class DictServer(Process):
    def __init__(self, connfd):
        self.connfd = connfd
        super().__init__()
        self.db = Database(user='root', password='123456', database='dict')
    def do_register(self,name,password):
        if self.db.register(name,password):
            self.connfd.send("OK".encode())
        else:
            self.connfd.send("NO".encode())
    def verify_login(self,account,password):
        if self.db.login(account,password):
            self.connfd.send("OK".encode())
        else:
            self.connfd.send("NO".encode())

    def put_word(self,word,account):
       data = self.db.gain_word(word)
       if data:
           self.db.insert_record(word,account)
           mean = "%s : %s"%(word,data)
           self.connfd.send(mean.encode())
       else:
           self.connfd.send("没有该单词".encode())
    def gain_record(self,account):
        data = self.db.take_record(account)
        if data:
            self.connfd.send(data.encode())
        else:
            self.connfd.send("记录为空".encode())
    def run(self):
        while True:
            data = self.connfd.recv(128).decode().split(" ")
            # 打印连接服务端的地址
            print(self.connfd.getpeername(),"连接")
            if data[0] == '退出':
                return print(self.connfd.getpeername(),"断开")
            elif data[0] == '登录':
                self.verify_login(data[1],data[2])
            elif data[0] == '注册':
                self.do_register(data[1],data[2])
            elif data[0] == '查询单词':
                self.put_word(data[1],data[2])
            elif data[0] == '查询记录':
                self.gain_record(data[1])




def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 立即重用
    s.bind(ADDR)
    s.listen(3)
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    while True:
        try:
            c, addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建线程处理客户端请求
        p = DictServer(c)
        p.daemon = True
        p.start()
if __name__ == '__main__':
    main()