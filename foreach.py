import sys,os,PyQt5,shutil
from tkinter import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


class MainForm(QWidget):
    def __init__(self,name='MainForm'):
        super(MainForm,self).__init__()
        self.setWindowTitle('Framework7更新工具')
        self.cwd = os.getcwd()
        self.resize(300,200)
        self.dirPath = QLineEdit(self)
        self.dirPath.setObjectName("dirPath")
        self.dirSavePath = QLineEdit(self)
        self.dirSavePath.setObjectName("dirSavePath")
        self.btn_chooseDir = QPushButton(self)
        self.btn_chooseDir.setObjectName("btn_chooseDir")
        self.btn_chooseDir.setText("选择Framework7项目目录")
        self.btn_chooseSavePath = QPushButton(self)
        self.btn_chooseSavePath.setObjectName("btn_chooseSavePath")
        self.btn_chooseSavePath.setText("选择Framework7新版本项目保存目录")
        self.btn_f7update = QPushButton(self)
        self.btn_f7update.setObjectName("btn_f7update")
        self.btn_f7update.setText("开始更新")
        layout=QVBoxLayout()
        layout.addWidget(self.btn_chooseDir)
        layout.addWidget(self.dirPath)
        layout.addWidget(self.btn_chooseSavePath)
        layout.addWidget(self.dirSavePath)
        layout.addWidget(self.btn_f7update)
        self.setLayout(layout)
        self.btn_chooseDir.clicked.connect(self.slot_btn_chooseDir)
        self.btn_chooseSavePath.clicked.connect(self.slot_btn_chooseSavePath)
        self.btn_f7update.clicked.connect(self.f7update)
    def slot_btn_chooseDir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,"选择Framework7项目目录","F:/HBuilderProject/f7test2")
        if dir_choose == "":
            return
        self.dirPath.setText(dir_choose)
    def slot_btn_chooseSavePath(self):
        savePath = QFileDialog.getExistingDirectory(self,"选择Framework7项目目录","C:/Users/Administrator/Documents/f7output")
        if savePath == "":
            return
        self.dirSavePath.setText(savePath)
    def f7update(self):
        p=self.dirSavePath.text()
        p2=self.dirPath.text()
        if p.strip()=="":
            if p2=="":
                p=self.cwd+"\\backup"
            else:
                p=p2
        self.dirSavePath.setText(p)
        for root, dirs, files in os.walk(p2):
            mdir=root.replace(p2,p)
            mdir=mdir.replace("\\","/")
            mdir2=root.replace(p2,self.cwd+"\\backup")
            mdir2=mdir2.replace("\\","/")
            if not os.path.exists(mdir):
                os.makedirs(mdir)
            if not os.path.exists(mdir2):
                os.makedirs(mdir2)
            for fn in files:
                backupPath=root.replace(p2,self.cwd+"\\backup")
                spath = root.replace(p2, p)
                oldname = root+"\\" +fn
                newname = spath+"\\"+fn
                newname2= backupPath+"\\"+fn
                shutil.copyfile(oldname, newname)
                shutil.copyfile(oldname,newname2)
if __name__=="__main__":
    app = QApplication(sys.argv)
    mainForm=MainForm("Framework7更新工具v1->v2")
    mainForm.show()
    sys.exit(app.exec_())


"""
root = Tk()
def main():
    root.title('Framework7更新工具')
    Label(root,text='请选择1.65版本的Framework7项目目录').grid(row=0,column=0)
    enter = Entry(root)
    enter.grid(row=1,column=0,padx=20,pady=20)
    enter.delete(0,END)
    running=1
    def getdir():
        dir_path = QFileDialog.getExistingDirectory(self, "选取文件夹","C:/")
        f7dir=enter.get()
    Button(root,text="浏览",width=10,command=getdir)\
        .grid(row=1,column=1,sticky=E,padx=10,pady=5)
    if running==1:
        root.mainloop()
if __name__== '__main__':
    main()
rootdir = 'F:\\HBuilderProject\\f7test2'
for i in os.walk(rootdir):
    print(i)

list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
for i in range(0,len(list)):
    path = os.path.join(rootdir,list[i])
    s1=""
    if os.path.isfile(path):
        fr=open(path,"r",encoding="utf-8")
        s1=fr.read()
        s1=s1.replace("data-page","data-name")
        s1=s1.replace("list-block","list")
        s1=s1.replace("content-block","block")
        s1=s1.replace("href=\"index.html\" class=\"back link\"","href=\"index.html\" class=\"back link external\"")
        fr.close()
        """