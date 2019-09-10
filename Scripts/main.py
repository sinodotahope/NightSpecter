#utf-8
'''TODO：
        1.根据当天时间建立文件夹名为xx月xx日文件夹
        2.根据当天月份选择建立的文件夹路径
        3.根据输入框提示输入作业组人员名字、调度命令号、上下道位置、给点时间、上下道工机具数量，
        生成excel表和文件夹，文件夹的子文件夹有工机具、工作门、放松脱。
        4.完成后打开文件夹和excel查看
        5.pyqt5做GUI界面
        6.可选择录入重点盯人员组和其他作业组人员（用于报警提示）'''

'''大的学习框架：
                1.操作系统文件操作(见mian.py)
                2.wxpy微信信息下载(见wxpy_mode.py)
                3.图像人脸识别
'''
import datetime,os,shutil,time,calendar
from wxpy_mode import PicGet
import threading



#时间模块
dt=datetime.datetime.now()
year=dt.year
month=dt.month
day=dt.day


#判断时间模块
while 1:
    workday=int(input('记录当前日期天窗扣1，记录第二天天窗扣2。列如：今天是1月1日，需要记录的天窗为1月2日凌晨，那么扣2。请扣（1/2）：'))
    if workday==1 or workday==2:
        os.system('cls')
        break
    else:
        print('输入错误，请重试！')
        time.sleep(1)
        os.system('cls')
        continue
limitedDay=calendar.monthrange(year,month)[1]
inputday=day+workday-1
if inputday>limitedDay:
    month+=1
    day=1
else:
    day=inputday

#建立文件夹的路径

totalPath='d:\\盯控\\照片'
filePath=os.path.join(totalPath,str(year)+'年'+str(month)+'月',str(month)+'月'+str(day)+'日')

#判断输入是否以"，"分离
def spli(workGroup):
    if "," in workGroup or "、" in workGroup:
        print('人名请用逗号分开！重新输入!')
        time.sleep(1)
        return None
    else:
        return workGroup
#工作组
def worker():
    workGroup=input('请输入：')
    workGroup=spli(workGroup)
    if workGroup==None:
        return 1,None
    if workGroup.lower()=='n':
        return None,None
    if workGroup=='da':
        return 'da',None

    workerLongName=workGroup+'组'
    '''workerName=workGroup.split()
    workerLongName=''
    for name in workerName:
        if name==workerName[-1]:
            workerLongName+=name+'组'
            continue
        if name==workerName[0]:
            workerLongName+=name
        else:
            workerLongName+='，'+name
            '''
    spicifyWorkerFilePath=os.path.join(filePath,workerLongName)

    return spicifyWorkerFilePath,workGroup

def mkDir(filePathCmd,groupRepository):
    pathes = []
    toolfilePath = os.path.join(filePathCmd, '工机具')
    doorfilePath = os.path.join(filePathCmd, '工作门')
    dropfilePath = os.path.join(filePathCmd, '防松脱')
    pathes.append(toolfilePath)
    pathes.append(doorfilePath)
    pathes.append(dropfilePath)
    groupRepository.append(filePathCmd)

    for path in pathes:
        os.makedirs(path)
    return toolfilePath,doorfilePath

def detectDuplicatePath(filePathCmd,num,groupRepository):
    while 1:
        choice = input('发现相同日期相同作业组:'+filePathCmd.split(os.path.sep)[-1]+'\n'+'请确认是否为同事建立的！\n不删除将建立副本!\n是否要删除（y/n)? ')
        if choice.lower() == 'n':
            num += 1
            filePathCmd =filePathCmd.split('(')[0]+ '(' + str(num) + ')'
            if os.path.exists(filePathCmd):

                detectDuplicatePath(filePathCmd,num,groupRepository)
            else:
                mkDir(filePathCmd,groupRepository)
                os.system('cls')
                print(filePathCmd.split(os.path.sep)[-1]+'已建立！')
            break
        elif choice.lower() == 'y':
            shutil.rmtree(filePathCmd)
            break
        else:
            print("输入错误，请重新尝试！")
            time.sleep(1)

#主程序
xdTool={}   #给每个人分配了工具图保存路径
xdDoor={}   #给每个人分配了工作门图保存路径
def main():
    print('作业人员名字，以\"，\"间隔,如果没有需要录入人员请输入“N/n”以结束，\n要删除刚才建立的文件夹输入“da”，\n要删除具体名字文件夹就输入相应文件夹名字')
    n=''
    groupRepository=[]
    totalWorkerList=[]
    while n!='end':
        num=0
        filePathCmd,workerGroup=worker()
        if filePathCmd==None:
            n='end'
            return print('正在生成文件夹中...请稍等...随后打开微信登录二维码...'),totalWorkerList
        elif filePathCmd==1:
            continue
        elif os.path.exists(filePathCmd):   #检查是否存在作业组文件夹，如果有就询问
                os.system('cls')
                detectDuplicatePath(filePathCmd,num,groupRepository)
                continue

        elif filePathCmd=='da':
            for path in groupRepository:
                try:
                    shutil.rmtree(path)
                except:
                    pass
            groupRepository=[]
        else:
            # 三类盯控
            dd=mkDir(filePathCmd,groupRepository)
            for i in workerGroup.split("，"):
                xdTool[i]=dd[0]
            for j in workerGroup.split("，"):
                xdDoor[j]=dd[1]
            totalWorkerList.append( workerGroup.split("，"))








totalWorkerList=main()[1]
openDirCmd='start '+filePath
p = os.system(openDirCmd)
print(totalWorkerList)

#TODO
    #接totalWorkerList

#主函数计时
dp = PicGet(totalWorkerList,filePath,xdTool,xdDoor)
dp.begin()
kaiguan = 1
localtime=time.time()
print("\n****来自程序猿的忠告！来自程序猿的忠告！来自程序猿的忠告！****"+"\n当群内图片连续发送超过5张，请数据扫描下载后进行核对，因技术上不明原因，引起微信群内成员一次性发送图片超过5张将造成程序上接受图片概率丢失。"+"\n请认真核对，在此忠告！\n请认真核对，在此忠告！\n请认真核对，在此忠告！"+"\n**********本软件功能介绍**********：\n\t\t\t1.下载微信群内工作组员发送的图片和文字消息并分类。\n\t\t\t2.支持手动和自动两种模式（目前自动只支持上道扫描，下道扫描请移步手动。）\n\t\t\t3.程序的每一步都有提示，请勿惊慌:)")
print('目前盯控：'+str(dp.groupTools)+'和'+str(dp.groupDoor)+'两个群。')


def input_func(name=''):
    global context
    context={'data': ''}

    context[ 'data' ] = input(name)

def consumer():
    global kaiguan

    print("-----------------输入y进行自动扫描，输入n进行手动扫描---------------")
    threConstructor('请输入:')                                                                          #由于线程join（）方法无法结束线程，所以只能运行一次保证后台大环境下有input在等待输入并控制循环，实际上我这里不输入，主循环还是在运行，一旦我输入，主循环将根据我的输入情况跳至相应if里。
                                                                                                        #如果使用循环threConstructor后台将有根据join（）参数时长而定的N个线程，人为要输入N个才能一个个终结线程。例如join（3）则每隔3秒建立线程，15秒后将有5个线程，我要输入5个数才能结束所有线程。
    while 1:


        if context['data']=='y'.lower():
            os.system('cls')
            while 1:
                selfTimer=input("想每次间隔多少秒更新？建议最低300秒为最佳。")
                try:
                    int(selfTimer)
                    break
                except:
                    print("输入有误，请重新输入正确数字！")
                    pass


            print("\n设定完成：每隔"+selfTimer+"秒更新一次。")
            threConstructor("\n按q退出自动扫描！(请在等待更新时按q)")
            while 1:
                localtime = time.time()
                if localtime > dp.time + int(selfTimer):
                    os.system('cls')
                    print("\n正在扫描更新...预计更新时间20秒...")

                    dp.detectedNewMsgs()
                    print("正在将信息写入本地...请稍候...(如果信息过多将花费更多的时间，请耐心等待。）)")
                    dp.getMsgs()
                    print("写入完成！")
                    if dp.toolSRemainWorkerList:
                        print('还有' + str(dp.toolSRemainWorkerList) + '没有上传上道工具图！')

                    if dp.doorSRemainWorkerList:
                        print('还有' + str(dp.doorSRemainWorkerList) + '没有上传上道工作门图！')

                    if dp.toolSRemainWorkerList == [] and dp.doorSRemainWorkerList == []:
                        print('没有工作组拖沓不发！')
                    if dp.toolSouterWorkers:
                        print('同时请注意1：' + str(dp.toolSouterWorkers) + '上传了上道工具图，请在微信内确认实际姓名！')
                    if dp.doorSouterWorkers:
                        print('同时请注意2：' + str(dp.doorSouterWorkers) + '上传了上道工作门图，请在微信内确认实际姓名！')
                    print("更新完成，等待下一次更新中...(按q退出自动扫描！)")




                if context['data']=='q':
                    os.system('cls')
                    print("结束自动扫描")
                    threConstructor("-----------------输入y进行自动扫描，输入n进行手动扫描，输入quit退出程序---------------\n请输入：")

                    break

                # print('手动的最可靠！！！（建议当判断微信群内组员已发送完毕后再进行手动）')


        elif context['data']=='n'.lower() :
            while 1 :
                refreshCmd=input("是否现在进行更新？Y/N(输入N将退出手动扫描)")
                if refreshCmd.upper()=='Y':
                    os.system('cls')
                    print("正在扫描更新...预计更新时间为20秒...")

                    dp.detectedNewMsgs()
                    print("正在将信息写入本地...请稍候...")
                    dp.getMsgs()
                    print("写入完成！")

                    unUpdateCheckCmd = input("是否查询未完成照片上传的作业组？（y/n）:").lower()
                    if unUpdateCheckCmd.lower() == 'y' and kaiguan == 1:
                        os.system('cls')
                        if dp.toolSRemainWorkerList:
                            print('还有' + str(dp.toolSRemainWorkerList) + '没有上传上道工具图！')


                        if dp.doorSRemainWorkerList:
                            print('还有' + str(dp.doorSRemainWorkerList) + '没有上传上道工作门图！')

                        if dp.toolSRemainWorkerList == [] and dp.doorSRemainWorkerList == []:
                            print('没有工作组拖沓不发！')
                        if dp.toolSouterWorkers:
                            print('同时请注意1：' + str(dp.toolSouterWorkers) + '上传了上道工具图，请在微信内确认实际姓名！')
                        if dp.doorSouterWorkers:
                            print('同时请注意2：' + str(dp.doorSouterWorkers) + '上传了上道工作门图，请在微信内确认实际姓名！')
                    elif unUpdateCheckCmd.lower() == 'y' and kaiguan == 2:
                        if dp.toolXRemainWorkerList:
                            print('还有' + str(dp.toolXRemainWorkerList) + '没有上传下道工具图！')
                        if dp.doorXRemainWorkerList:
                            print('还有' + str(dp.doorXRemainWorkerList) + '没有上传下道工作门图！')
                        if dp.toolXRemainWorkerList == [] and dp.doorXRemainWorkerList == []:
                            print('没有工作组拖沓不发！')
                        if dp.toolXouterWorkers:
                            print('同时请注意3：' + str(dp.toolXouterWorkers) + '上传了下道工具图，请在微信内确认实际姓名！')
                        if dp.doorXouterWorkers:
                            print('同时请注意4：' + str(dp.doorXouterWorkers) + '上传了下道工作门图，请在微信内确认实际姓名！')
                    # localtime=time.time()
                    if kaiguan == 1:

                        xiadaoCmd = input("是否进入下道照片的轮询？（y/n）：")
                        if xiadaoCmd.lower() == 'y':
                            os.system('cls')
                            xiadaoCmd = input("再次确认是否进入下道照片的轮询？（y/n）：")
                            if xiadaoCmd.lower()=='y':
                                os.system('cls')
                                dp.statCmd = 2
                                kaiguan = 2
                            else:

                                print("维持上道照片检索中...")

                        else:
                            os.system('cls')
                            print("维持上道照片检索中...")
                elif refreshCmd.upper()=="N":

                    threConstructor("-----------------输入y进行自动扫描，输入n进行手动扫描，输入quit退出程序---------------\n请输入：")
                    break
        elif context['data'].lower()=='a':
            context['data']='y'
        elif context['data'].lower()=='m':
            context['data']='n'
        elif context['data'].lower()=='quit':
            os.system('cls')
            print('感谢您的使用！\n程序已退出！')
            time.sleep(5)
            break
        else:

            continue





def threConstructor(name):



        t3= threading.Thread(target=input_func,args=(name,))
        t3.start()






        t3.join(1)
        # 等待10秒






consumer()
















































