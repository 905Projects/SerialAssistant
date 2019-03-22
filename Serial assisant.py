#python 3.6.5
#matplotlib==3.0.3
#numpy==1.16.2
#pyserial==3.4

import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
from pylab import *
import struct
import string
import time

Color = ['red','orange','darkblue','darkslategray','deeppink','megenta'] #绘图线颜色
Baud = 115200      #波特率设置
Port_name = "COM3" # 端口名
Timeout = 0.5   #连接端口最大响应时间
Datanum = 4     #传入数据的数量
yMax = 70       #图中y轴上限
yMin = -70      #图中y轴下限
x_span = 0.5    #横轴跨度
xMax = 0.5      #图中x轴上限
#xMin = 0        #图中y轴下限
xMin = xMax - x_span
x_name = "Time"  #设置x轴名称
y_name = "multi_val"  #设置y轴名称
Title =  "pic"   #图像名称
line_name = ["Pitch","Roll","Yaw","Temp"]#线名称
class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.002):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = []
        self.line=[]
        for i in range(0,Datanum):
            self.ydata.append([0])       #创建参数个数的子列表
        for i in range(0,Datanum):
            self.ax.plot(self.tdata, self.ydata[i])
        for i in range(0,Datanum):
            self.line.append(Line2D(self.tdata, self.ydata[i],color = Color[i]))
            self.ax.add_line(self.line[i])       
        self.ax.set_ylim(yMin, yMax)        #初始化y轴上下限
        self.ax.set_xlim(0,xMax)            #初始化x轴上下限

        
    def update(self, y):
        global yMax
        global yMin
        global xMax
        global xMin
        global x_span
        #lastt = self.tdata[-1]
        #if lastt > self.tdata[0] + self.maxt:  # reset the arrays
           #self.tdata = [self.tdata[-1]]
           #self.ydata = [self.ydata[-1]]
           #self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
           #self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)              #增加数组元素
        for i in range(0,Datanum):
            try:
                yt = float(y[i])          #排除干扰信息
            except:
                yt = self.ydata[i][i-1]
            self.ydata[i].append(yt)      #增加数组元素
            self.line[i].set_data(self.tdata, self.ydata[i])
            if (yt) > yMax:
                yMax = yt + 1
                self.ax.set_ylim(yMin, yMax)        #更新y轴上下限
                self.ax.figure.canvas.draw()
            elif (yt) < yMin:
                yMin = yt + 1
                self.ax.set_ylim(yMin, yMax)        
                self.ax.figure.canvas.draw()        
            if t > xMax:                            #更新x轴上下限
                xMax = t + 0.5
                #xMin = xMax - x_span
                self.ax.set_xlim(xMin, xMax) 
                self.ax.figure.canvas.draw()

        return self.line


def emitter(p=0.03):
    time_bytes = ser.readline()     #读取端口传来的数据
    str1 = (str(time_bytes))
    print(str1)
    if len(str1)>3:                 #根据传来的干扰信息自行修改
        str1 = str1[2:-3].split()   # 切片方便处理
        print(str1)
        yield str1
    


fig, ax = plt.subplots(figsize = (7,7))  #修改图像大小，这里是700x700像素
scope = Scope(ax)
print(fig, ax)
ser = serial.Serial(Port_name,Baud,timeout = Timeout)#设置端口，波特率，响应时间
# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=0.1,
                              blit=True)
xlabel(x_name)                      
ylabel(y_name)
title (Title)
ax.legend(line_name)
plt.show()

