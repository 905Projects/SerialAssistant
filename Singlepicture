#请确认安装有以下包，本程序在python3.6.5下正常运行
import serial
from pylab import *
import struct
import string
import matplotlib
import time
Color = ['blue','tomato','deeppink','purple','red','slateblue','springgreen','midnightblue','lightskyblue']
#本文件适用于双（多）窗口实时绘图显示
#初始设置
set_map=[2,1]           #表示第一个图上有2个函数，第二个图上有1个函数
set_datanum = 3         #若需要接收3个浮点数，则输入3
set_mapform =[1,2]      #[1,2]表示生成一行两列的母图，其上可放置个数为1*2的子图
pic_name = ['P1','P2']        #设置每个图的图名
pic_xlabel = ['Time','Time']    #设置横轴标签
pic_ylabel = ['Num','Y']      #设置纵轴标签
latest_num = 30         #设置显示点的个数
labels = ['a','b','c']  #标签
fig_name = ['fig1','fig2']
data_write = 10         #向文件写入几组数据

#subplot(2,2,3)         #将绘制多图在一图上使用的函数

count = 0
x_read = []
y_read = []                #读取用列表
#连接端口
ser = serial.Serial("COM3",115200,timeout = 0.5)
print (ser.name)           #打印设备名及端口名
print (ser.port)
#ser.open()                #打开端口
fig1 = plt.figure('fig1')
fig2 = plt.figure('fig2')
#数据接收，列表创建部分
for i in range(0,set_datanum):
        y_read.append([])
time = 0
f = open("test.txt",'w',encoding='utf-8')  #打开文本


while(1):
        count = 0
        time_bytes = ser.readline() #从接口读取
    #if(time_bytes == -2):
    #   break
    #if(time_bytes != -1):
    #time = struct.unpack('<f', time_bytes)[0]  #字符数组转浮点
    #y_bytes = ser.read(4)
    #y = struct.unpack('<f', y_bytes)[0]  
        str1 = (str(time_bytes))
        if len(str1)==3:
            continue
        if time<=data_write:
            str2 = str(time)+" "+str1[2:-3]+"\n"
            f.write(str2)
        if(time==data_write):
            f.close()
        str1 = str1[2:-3].split()
        print(str1)
        for i in range(0,set_datanum):
                y_read[i].append(float(str1[i]))
        x_read.append(time)
        time+=1
        if(len(x_read)>=latest_num):
                for i in range(0,set_datanum):
                        y_read[i] = y_read[i][-latest_num:]
                x_read = x_read[-latest_num:]
        clf()
        for i in range(0,len(set_map)):
                figure(fig_name[i])
                title(pic_name[i])                         #设置标题
                xlabel(pic_xlabel[i])                      #设置横纵轴名
                ylabel(pic_ylabel[i])
                for j in range(0,set_map[i]):
                        if j==0:
                            clf()
                        plot(x_read,y_read[count],label = labels[count],linewidth ='1',color =Color[j%9], linestyle='-')
                        legend(loc='upper left')
                        count+=1
                        
        pause(0.01)                         #与数据传输间隔可以相同
        ioff()
