import socket;
import threading;
import struct;
import os;
import time;
import shutil
import json
import win32api

class Application:
    def __init__(self, remoteAddress = ("localhost", 7999)):
        self.path = os.getcwd()
        self.remoteAddress = remoteAddress   #参数赋值
        self.mutex = threading.Lock()
        data = self.__get_info()
        if data is None:
            return False
        self.filename = data["filename"]
        # self.path = data["path"]
        self.fileversion = data["version"]
        self.Src_code = "please send me new version"

    def __get_info(self):
        path = self.path + "\\"+"update"+ "\\"+ 'update_config.jason'
        if os.path.isfile(path) is False:
            print("配置文件错误，无法更新")
            return None
        with open(path, 'r') as json_file:
            data = json.load(json_file)
            return data

    def __setSocket(self):         #配置socket
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);

    def __processUpdate(self):
        Src_code = struct.pack("128s128s50s", self.Src_code.encode("utf-8"), self.filename.encode("utf-8"), self.fileversion.encode("utf-8"))
        self.socket.send(Src_code)
        buf_tmp = self.socket.recv(1024)
        if buf_tmp is not None:
            filename, filesize ,filecount = struct.unpack('128sll', buf_tmp)
            filename = str(filename.strip('\00'.encode("utf-8")),encoding = "utf-8")
            path_new = self.path +"\\"+"update"+"\\"+ filename
            print(path_new)
            recvd_size =0
        else:
            print("error")
            return
        f = open(path_new,"wb")
        while(1):
            while recvd_size != filesize:
                if filesize - recvd_size > 1024:
                    rdata = self.socket.recv(1024)
                    recvd_size += len(rdata)
                else:
                    rdata =self.socket.recv(filesize - recvd_size)
                    recvd_size = filesize
                f.write(rdata)
            f.close()
            break
        print("recv done")
        path_old = self.path + "\\"+self.filename +"." +"exe"
        if os.path.isfile(path_old) is True:
            os.remove(path_old)
            print("移除{}".format(path_old))
        shutil.move(path_new, self.path)
        print("创建{}".format(path_new))
        win32api.ShellExecute(0, 'open', path_old, '', '', 0)


    def __connect(self):  # 网络连接
        self.__setSocket();
        self.socket.connect(self.remoteAddress);

    def __init_program(self):
        path = self.path +"\\"+"update"
        if os.path.isdir(path) is False:
            os.mkdir(path)


    def run(self):
        self.__connect()
        showThread = threading.Thread(target=self.__processUpdate);
        showThread.start();


if __name__ == "__main__":
    print("创建连接...")
    app = Application();
    time.sleep(2)
    app.run();
