#!/usr/bin/env python
# coding:utf-8
import socket
import threading, time
from Tkinter import *

class Application(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        # while True:
        self.createWidgets()
            # time.sleep(1)

    def createWidgets(self):
        self.romInfLabel = Label(self, text='内存信息',fg='black').grid(row=0, column=0,sticky = W)
        self.romInfInput = Message(self,text = buf1,bg='white',width = 500).grid(row=1,sticky = W)
        self.CPUInfLabel = Label(self, text='CPU信息', fg='black').grid(row=2, column=0,sticky = W)
        self.CPUInfInput = Message(self,text = buf2,bg='white',width = 500).grid(row=3, sticky = W)
        self.timeInfLabel = Label(self, text='运转时间',fg='black').grid(row=4, column=0,sticky = W)
        self.timeInfInput = Message(self,text = buf3,bg='white',width = 500).grid(row=5,sticky = W)
        self.flowInfLabel = Label(self, text='网卡流量信息',fg='black').grid(row=6, column=0,sticky = W)
        self.flowInfInput = Message(self,text = buf4,bg='white',width = 500).grid(row=7, sticky = W)
        self.diskInfLabel = Label(self, text='磁盘空间使用', fg='black').grid(row=8, column=0,sticky = W)
        self.diskInfInput = Message(self,text = buf5,bg='white',width = 500).grid(row=9, sticky = W)
        # self.closeButton = Button(self, text='关闭', command=self.quit ).grid(row=10, column=0)

def main_window():
    def callback(event):
        window.createWidgets()


    root=Tk()
    root.geometry('500x700+500+200')
    root.title('路由器数据')
    root.bind("<ButtonPress-1>", callback)
    window = Application(root)
    window.mainloop()



def get_info():
    # global server_list
    server = '192.168.1.1'
    connPort = 9999
    # readtarget()
    connserver(server, connPort)

def connserver(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while True:
        buf = s.recv(4096)
        if not len(buf):
            break

        def netstat_proc(info):
            resu = ''
            for di in info:
                resu = resu+str(di['interface'])+':\n接收:\n'+str(di['ReceiveBytes']/1048576)+'MB\t\t'+str(di['ReceivePackets'])+'Packets\n发送:\n'+str(di['TransmitBytes']/1048576)+'MB\t\t'+str(di['TransmitPackets'])+'Packets\n\n'
            return resu
        info = eval(str(buf).strip('\n'))
        # with open('text', 'a') as f:
        #     f.write(buf)
        global buf1
        global buf2
        global buf3
        global buf4
        global buf5
        buf1 = '总内存:\t\t'+str(info['mem_stat']['MemTotal']/1048576)+'MB\n剩余内存:\t\t'+str(info['mem_stat']['MemFree']/1048576)+'MB'
        # buf2 = str(info['cpu_stat']['vendor_id']+' '+info['cpu_stat']['model name']+'\n核心数'+info['cpu_stat'][vender_id])
        # buf2 = info['cpu_stat']['model name']+'核心数:'+info['cpu_stat']['cpu cores']+'实时频率(MHz)'+info['cpu_stat']['cpu MHz']
        cst = info['cpu_stat']
        buf2 = 'Hardware:\t'+cst['Hardware']+'Model name:\t'+cst['model name']+'CPU implementer:\t'+cst['CPU implementer']+'CPU architecture:\t'+cst['CPU architecture']+'Features:\t'+cst['Features']
        buf3 = str(info['runtime_stat']['day'])+'天'+str(info['runtime_stat']['hour'])+'时'+str(info['runtime_stat']['minute'])+'分'+str(info['runtime_stat']['second'])+'秒'#).strip('\n')
        buf4 = netstat_proc(info['net_stat'])
        buf5 = 'Available:\t\t'+str(info['disk_stat']['available']/1048576)+'GB\nUsed:\t\t'+str(info['disk_stat']['used']/1048576)+'GB\nCapacity:\t\t'+str(info['disk_stat']['capacity']/1048576)+'GB'
#info['cpu_stat']['vendor_id'] + 

if __name__ == "__main__":
    # server_list = []
    buf1 = ""
    buf2 = ""
    buf3 = ""
    buf4 = ""
    buf5 = ""
    t1 = threading.Thread(target = main_window, args = ())
    t2 = threading.Thread(target = get_info, args = ())
    t1.start()
    t2.start()
    t1.join()
    t2.join()

