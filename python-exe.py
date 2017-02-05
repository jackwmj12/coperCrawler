import os
import shutil
import json
#pyisntallerpath:pyinstaller.py绝对路径，r"E:\\python_64\\pyinstaller-develop\\pyinstaller.py"
# arg : -F 生成一个exe，-w，取消控制台 -i 更改exe图标
#icopath ： ico图标绝对路径
#pypath ：被打包的python文件绝对路径
#filenewname : 生成的exe文件的名字
#file_to :在哪儿生成文件
class PyIstaller:
    def __init__(self,pyinstallerpath=None,arg = "-F -w -i",icopath=None,pypath=None,filenewname=None,file_to=None):
        self.file_name = None
        self.file_path = None
        self.file_version = None
        self.update_data =None
        self.pyinstaller_path = pyinstallerpath
        self.ico_path = icopath
        self.py_path = pypath
        self.arg = arg
        self.filename=(self.py_path.split("\\")[-1]).split(".")[0] + "." + "exe"
        self.file_to = file_to
        if "exe" not in filenewname:
            self.filenewname = filenewname + '.' + "exe"
        else:
            self.filename = filenewname
        self.info_path = os.path.split(self.py_path)[0]+ r"\\" + r"update" +r"\\"
        self.version_flag = self.__get_info()

    def __get_oldname(self):
        path = self.file_to +r"\\" +r"update"+"\\"+"update_config.jason"
        if os.path.isfile(path) is True:
            with open(path, 'r') as json_file:
                data = json.load(json_file)
            return data["filename"]
        else :
            return None

    def __get_info(self):
        path = self.info_path + "update_config.jason"
        if os.path.isfile(path) is True:
            with open(path, 'r') as json_file:
                data = json.load(json_file)
            self.file_name = data["filename"]
            self.file_version = data["version"]
            self.file_path = self.file_to + r"\\"
            self.update_data ={
                "fileid"  :data["filename"],
                "filename":self.filenewname,
                "version" :data["version"],
                "file_path":self.file_to + r"\\"
            }
            return True
        else:
            return False

    def run(self):
        path =self.file_to + r"\\"
        path_new = path + 'dist' + r'\\' + self.filename #生成的exe文件地址
        old_name = self.__get_oldname()
        if old_name != None:
            path_old = path + old_name   #文件内原先exe文件地址
        else:
            path_old = None
        path_build = path + 'build'         #生成的build文件
        path_dist = path + 'dist'           #生成的dist文件，新exe存在这里
        path_newexe = path + self.filename  #新生成的exe文件将存放的地点
        path_newname = path + self.filenewname   #新生成的exe文件的新名字
        path_update = path + "update"
        # print(" path_new:{},\n path_old:{},\n path_build:{},\n path_dist:{},\n path_newexe:{},\n path_newname:{},\n path_update:{}".format(path_new,path_old,path_build,path_dist,path_newexe,path_newname,path_update))
        if os.path.isdir(path_update) is True:
            shutil.rmtree(path_update)
            print("预移除{}".format(path_update))
        if os.path.isdir(path_build) is True:
            shutil.rmtree(path_build)
            print("预移除{}".format(path_build))
        if os.path.isdir(path_dist) is True:
            shutil.rmtree(path_dist)
            print("预移除{}".format(path_dist))
        command = r"python " + self.pyinstaller_path+" " +self.arg +" "+ self.ico_path +" "+self.py_path  #编辑指令
        print("准备执行指令{}".format(command))    #执行指令
        os.system(command)
        print("创建成功")#生成成功
        if path_old is not None:
            if os.path.isfile(path_old) is True:       #移除原先的exe文件
                os.remove(path_old)
                print("移除{}".format(path_old))
        if os.path.isdir(path_build) is True:
            shutil.rmtree(path_build)
            print("移除{}".format(path_build))
        if os.path.isfile(path_new) is True:        #dist内exe文件存在
            shutil.move(path_new, path)             #移入原exe文件所在地点
            print("加载{}".format(path_new))
        if os.path.isdir(path_dist) is True:       #删除dist空文件
            shutil.rmtree(path_dist)
            print("移除{}".format(path_dist))
        if os.path.isfile(path_newexe):            #新生成文件移除成功
            if os.rename(path_newexe,path_newname):   #进行重命名
                print("文件重命名成功")
        if self.version_flag is True:
            if os.path.isdir(path_update) is False:
                os.mkdir(path_update)
            path_update_jason = path_update + r"\\" + 'update_config.jason'
            with open(path_update_jason, 'w') as json_file:
                json_file.write(json.dumps(self.update_data))
        print("exe文件生成成功")



if __name__ == "__main__":
    # path_pyinstaller = r"E:\\python_64\\pyinstaller-develop\\pyinstaller.py"
    # arg = "-F -w -i"
    # path_ico = r"E:\\OneDrive\\python\\pythonexe\\coper_crawler.ico "
    # path_py = r"E:\\OneDrive\\python\\python_program\\coper_crawler\\copercrawler_ui.py"
    # file_to = r"C:\\Users\\joe\\Desktop\\exe\\copercrawler"
    # filenewname = "copercrawler"
    # pyinstaller = PyIstaller(pyinstallerpath=path_pyinstaller,arg=arg,icopath=path_ico,pypath=path_py,filenewname =filenewname,file_to=file_to)
    # pyinstaller.run()

    path_pyinstaller = r"E:\\python_64\\pyinstaller-develop\\pyinstaller.py"
    arg = "-F -i"
    path_ico = r"E:\\OneDrive\\python\\pythonexe\\myupdate.ico "
    path_py = r"E:\\OneDrive\\python\\python_program\\coper_crawler\\myupdate.py"
    file_to = r"C:\\Users\\joe\\Desktop\\exe\\copercrawler"
    filenewname = r"myupdate"
    pyinstaller = PyIstaller(pyinstallerpath=path_pyinstaller, arg=arg, icopath=path_ico, pypath=path_py,
                             filenewname=filenewname, file_to=file_to)
    pyinstaller.run()