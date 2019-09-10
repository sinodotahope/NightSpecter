"""实现功能：
            1.自动登录
            2.监听工机具、工作门群所有人员的消息（图片，文字）
            3.将重点盯控人员发的图片下载至特定人员的文件夹
            4.将文字进行分析整理，所有人员天窗点前是否发送上（点前）下（点后）道工机具照片，是否发送上（点前）下（点后）道工作门照片。如果没有及时发送，发送报警（或消息）至机器人助手（或特定群）进行提示。


"""
'''
#检查群成员修改备注名称的情况
from wxpy import *
bot=Bot(cache_path=True)

unChangeList=[]
userName=''
displayName=''
group=bot.groups(update=True).search('工器具')[0]
for i in group.members:
    for j,x in i.raw.items():
        if j=='UserName':
            userName=x
        if j=='DisplayName':
            if x=='':
                unChangeList.append(i.raw['NickName'])



print('未改群名称人数：'+str(len(unChangeList))+"人，他们是：")
for g in unChangeList:
    print(g)
'''
from wxpy import *
import  os
import time
import datetime

class PicGet:
    def __init__(self, totalWorkerList,filepath, xdTool, xdDoor):
        self.bot = Bot()
        self.bot.messages.max_history=10000
        self.xdTool = xdTool
        self.xdDoor = xdDoor
        self.displayNameError = 1
        self.time=time.time()
        self.filepath = filepath
        self.toolSouterWorkers = []
        self.toolXouterWorkers = []
        self.doorSouterWorkers = []
        self.doorXouterWorkers = []
        self.groupTools = self.bot.groups(update=True).search('材料工器具')[0]
        self.groupDoor = self.bot.groups(update=True).search('天窗作业盯控')[0]
        self.cc = ''

        self.workers = []
        self.detect = []
        self.msgContaner = []
        self.time = time.time()
        self.statCmd = 1
        self.path = "C:\\盯控"
        self.newMsgs = []
        self.doNewMsgs()
        self.totalWorkerList=[]
        self.totalWorkerList += totalWorkerList
        self.toolSRemainWorkerList=[]
        self.toolSRemainWorkerList+= totalWorkerList                                                    #根据实验表明，原列表赋值给新列表名不能开辟出新的内存给新列表名，必须进行自我赋值（空值），然后进行+操作。如若不然操作新列表名实则对原列表进行操作，这样以来，以原列表为原型赋值给新的列表越多，造成的同时修改也越多，血的教训啊。
        self.doorSRemainWorkerList=[]
        self.doorSRemainWorkerList += totalWorkerList
        self.toolXRemainWorkerList=[]
        self.toolXRemainWorkerList+= totalWorkerList
        self.doorXRemainWorkerList=[]
        self.doorXRemainWorkerList+= totalWorkerList
        self.mid=totalWorkerList
        self.wokers_def()

    def timeStiker(self):
        return datetime.datetime.now().strftime('%H-%M-%S')

    def doNewMsgs(self):

        self.newMsgs=[]
        for i in self.bot.messages.search(sender=self.groupTools)+self.bot.messages.search(sender=self.groupDoor):
            if i not in list(self.msgContaner):
                self.newMsgs.append(i)

    def refresh(self):
        self.displayNameError=1

    def refreshsxd(self):
        self.tooltotalWorkerList =self.mid
        self.doortotalWorkerList =self.mid

    def wokers_def(self):
        for i in self.totalWorkerList:
            self.workers += i

    def detectedNewMsgs(self):

        self.detect =list(self.bot.messages.search(sender=self.groupTools))+list(self.bot.messages.search(sendr=self.groupDoor))
        time.sleep(10)
        while 1:
            if self.detect !=list(self.bot.messages.search(sender=self.groupTools))+list(self.bot.messages.search(sendr=self.groupDoor)):
                time.sleep(5)
                self.detect =list(self.bot.messages.search(sender=self.groupTools))+list(self.bot.messages.search(sendr=self.groupDoor))
                time.sleep(5)
                continue
            else:
                time.sleep(5)
                if self.detect !=list(self.bot.messages.search(sender=self.groupTools))+list(self.bot.messages.search(sendr=self.groupDoor)):
                    time.sleep(5)
                    continue
                break
        newMsgnum = len(self.bot.messages.search(sender=self.groupTools))+len(self.bot.messages.search(sender=self.groupDoor)) - len(self.msgContaner)
        print("一共收到", newMsgnum, "条讯息。")
        self.time=time.time()
        return newMsgnum

    def getMsgs(self):


        self.doNewMsgs()
        self.msgContaner = list(self.bot.messages.search(sender=self.groupTools))+list(self.bot.messages.search(sender=self.groupDoor))


        for j in self.newMsgs:

            if j.sender == self.groupTools:
                #工器具和放松脱信息下载

                if j.member.raw['DisplayName']!='':

                    p=j.member.raw['DisplayName']
                    for man in self.workers:
                    #有些人没有改群内备注，就会为空值 TODO如果为空值，用NickName提醒盯控人
                        try:
                            if man in p:
                                msgSender = man
                                if j.type == TEXT:
                                    if self.statCmd==1:                                                                               #上道文字
                                        with open(os.path.join(self.xdTool[msgSender], "文字.txt"), "a") as f:
                                            f.write("\n"+self.timeStiker()+"\t上道信息：" + j.text)
                                    else:                                                                                               #下道文字
                                        with open(os.path.join(self.xdTool[msgSender], "文字.txt"), "a") as f:
                                            f.write("\n"+self.timeStiker()+"\t下道信息：" + j.text)

                                elif j.type==PICTURE:
                                    if self.statCmd==1:                                                                                #上道图
                                        if self.statCmd==1:
                                            with open(os.path.join(self.xdTool[msgSender], "上道" + self.timeStiker() + ".png"),
                                                      "wb") as f:
                                                f.write(j.get_file())
                                            time.sleep(4)

                                            try:
                                                for i in self.toolSRemainWorkerList:
                                                    for j in i:
                                                        if j == msgSender:
                                                            self.toolSRemainWorkerList.remove(i)
                                            except:
                                                pass
                                    else:                                                                                              #下道图
                                        with open(os.path.join(self.xdTool[msgSender], "下道" + self.timeStiker() + ".png"),
                                                  "wb") as f:
                                            f.write(j.get_file())
                                        time.sleep(4)

                                        try:
                                            for i in self.toolXRemainWorkerList:
                                                for j in i:
                                                    if j == msgSender:
                                                        self.toolXRemainWorkerList.remove(i)
                                        except:
                                            pass
                                self.displayNameError = 2
                        except:
                            print("内部错误！请截图联系软件管理员！（目前不影响软件使用！）")
                    if self.displayNameError==1:
                        print("收到来自工器具群非作业组员\t"+p+"\t的一条信息，请在手机端微信群内进行查看！")
                        self.refresh()
                else:
                    g=j.member.raw['NickName']#没有改备注名的处理
                    notChangeNamePath=os.path.join(self.filepath,g,"工器具")
                    fangsongtuoPath=os.path.join(self.filepath,g,"防松脱")

                    try:
                        os.makedirs(notChangeNamePath)
                        os.makedirs(fangsongtuoPath)
                    except:
                        pass
                    if j.type==TEXT:
                        if self.statCmd==1:                                                                         #上道文字

                            with open(os.path.join(notChangeNamePath,"文字.txt"),"a") as f:
                                f.write("\n" + self.timeStiker() + "\t上道信息：" + j.text)
                        else:                                                                                       #下道文字
                            with open(os.path.join(notChangeNamePath,"文字.txt"),"a") as f:
                                f.write("\n" + self.timeStiker() + "\t下道信息：" + j.text)
                    elif j.type==PICTURE:
                        if self.statCmd==1:
                            if g not in self.toolSouterWorkers:
                                self.toolSouterWorkers.append(g)
                            with open(os.path.join(notChangeNamePath,"上道"+ self.timeStiker() + ".png"),"wb") as f:
                                f.write(j.get_file())
                            time.sleep(4)
                            print("收到一个昵称为\t"+g+"\t的---工器具---信息，请在微信群里确认工作组，并人为剔除未发图组。")
                        else:
                            if g not in self.toolXouterWorkers:
                                self.toolXouterWorkers.append(g)
                            with open(os.path.join(notChangeNamePath,"下道"+ self.timeStiker() + ".png"),"wb") as f:
                                f.write(j.get_file())
                            time.sleep(4)
                            print("收到一个昵称为\t"+g+"\t的---工器具---信息，请在微信群里确认工作组，并人为剔除未发图组。")
            elif j.sender == self.groupDoor:
                if j.member.raw['DisplayName'] != '':
                    h = j.member.raw['DisplayName']
                    for man in self.workers:

                #工作门信息下载
                        if man in h:   #有些人没有改群内备注，就会为空值 TODO如果为空值，用NickName提醒盯控人
                            msgSender = man
                            if j.type == TEXT:
                                if self.statCmd==1:
                                    with open(os.path.join(self.xdDoor[msgSender], "文字.txt"), "a") as f:
                                        f.write("\n"+self.timeStiker()+"\t上道信息：" + j.text)
                                else:
                                    with open(os.path.join(self.xdDoor[msgSender], "文字.txt"), "a") as f:
                                        f.write("\n"+self.timeStiker()+"\t下道信息：" + j.text)
                            elif j.type==PICTURE:
                                if self.statCmd==1:
                                    with open(os.path.join(self.xdDoor[msgSender], "上道" + self.timeStiker() + ".png"),
                                              "wb") as f:
                                        f.write(j.get_file())
                                    time.sleep(4)

                                    try:
                                        for i in self.doorSRemainWorkerList:
                                            for j in i:
                                                if j == msgSender:
                                                    self.doorSRemainWorkerList.remove(i)
                                    except:
                                        pass
                                else:
                                    with open(os.path.join(self.xdDoor[msgSender], "下道" + self.timeStiker() + ".png"),
                                              "wb") as f:
                                        f.write(j.get_file())
                                    time.sleep(4)

                                    try:
                                        for i in self.doorXRemainWorkerList:
                                            for j in i:
                                                if j == msgSender:
                                                    self.doorXRemainWorkerList.remove(i)
                                    except:
                                        pass
                            self.displayNameError = 2
                    if self.displayNameError == 1:
                        print("收到来自工作门非作业组员\t"+h+"\t的一条信息，请在手机端微信群内进行查看！")
                        self.refresh()
                else:
                    o=j.member.raw['NickName']#工作门未改昵人员称信息下载
                    notChangeNamePath=os.path.join(self.filepath,o,"工作门")

                    try:
                        os.makedirs(notChangeNamePath)

                    except:
                        pass
                    if j.type==TEXT:
                        if self.statCmd==1:

                            with open(os.path.join(notChangeNamePath,"文字.txt"),"a") as f:
                                f.write("\n" + self.timeStiker() + "\t上道信息：" + j.text)
                        else:
                            with open(os.path.join(notChangeNamePath,"文字.txt"),"a") as f:
                                f.write("\n" + self.timeStiker() + "\t下道信息：" + j.text)
                    elif j.type==PICTURE:
                        if self.statCmd==1:
                            if o not in self.doorSouterWorkers:
                                self.doorSouterWorkers.append(o)
                            with open(os.path.join(notChangeNamePath,"上道"+ self.timeStiker() + ".png"),"wb") as f:
                                f.write(j.get_file())
                            time.sleep(4)
                            print("收到一个昵称为\t"+o+"\t的---工作门---信息，请在微信群里确认工作组，并人为剔除未发图组。")
                        else:
                            if o not in self.doorXouterWorkers:
                                self.doorXouterWorkers.append(o)
                            with open(os.path.join(notChangeNamePath,"下道"+ self.timeStiker() + ".png"),"wb") as f:
                                f.write(j.get_file())
                            time.sleep(4)
                            print("收到一个昵称为\t"+o+"\t的---工作门---信息，请在微信群里确认工作组，并人为剔除未发图组。")







    def begin(self):
        print("联接微信成功，开始接收数据！")







