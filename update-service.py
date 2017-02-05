import socket;
import threading;
import struct;
import time
import os
import shutil
import json

class Application:
    def __init__(self, host = ("localhost", 7999)):
        self.path = None
        self.host = host
        self.__setSocket(self.host)
        self.Src_code = "please send me new version"
        self.filename =None
        self.fileversion =None
        self.newversion =None
        self.newfilename = None
        self.newpath =None

    def __setSocket(self, host):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        self.socket.bind(self.host);
        self.socket.listen(5);
        print("Server running on port:%d" % host[1]);

    def __Src_check(self,Src):
        head,filename,fileversion = struct.unpack("128s128s50s",Src)
        head = str(head.strip('\00'.encode("utf-8")),encoding = "utf-8")
        filename = str(filename.strip('\00'.encode("utf-8")),encoding = "utf-8")
        fileversion = str(fileversion.strip('\00'.encode("utf-8")),encoding = "utf-8")
        if head != self.Src_code :
            return  False
        self.filename = filename
        self.fileversion = fileversion

    def __update_config_init(self):
        path = os.getcwd()
        path = path +"\\"+"update" +"update_config.jason"
        with open(path, 'r') as json_file:
            data = json.load(json_file)
        self.newfilename = data["filename"]
        self.newpath = data["path"]
        self.newversion = data["version"]


    def __build_the_path(self):
        path =os.getcwd()
        path = path +"\\"
        self.path = path + self.filename + ".exe"

    def __processConnection(self, client,addr):
        tmp_date=client.recv(1024)
        # print(tmp_date)
        if self.__Src_check(tmp_date) is False:
            return False
        self.__build_the_path()
        if os.path.isfile(self.path) is False:
            print("文件不存在")
            return
        size = os.path.getsize(self.path)
        size_count =self.__size_count_math(size)
        fhead = struct.pack('128sll', os.path.basename(self.path).encode("utf-8"),size,size_count)
        client.send(fhead)
        print("size is {}".format(size))
        print("count is {}".format(size_count))
        with open(self.path, "rb")as f:
            count = 0
            while True:
                filedate = f.read(1024)
                count = count + 1
                if not filedate:
                    print("传输完毕")
                    print("%s:%d disconnected!");
                    print("连接结束时间:%s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                    print("****************************************")
                    return;
                client.send(filedate)

    def run(self):
        while(1):
            client,addr = self.socket.accept();
            clientThread = threading.Thread(target = self.__processConnection, args = (client, addr));  #有客户端连接时产生新的线程进行处理
            clientThread.start();

    def __size_count_math(self,size):
        size_count = size / 1024
        if size_count > int(size_count):
            return int(size_count) + 1
        else:
            return print(size_count)



if __name__ == "__main__":
    app = Application();
    app.run();

