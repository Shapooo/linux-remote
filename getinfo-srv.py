#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
from collections import OrderedDict
from collections import namedtuple
import os
import socket
import threading
import time


def tcplink(sock, addr):

    def memory_stat(): 
        mem = {} 
        f = open("/proc/meminfo") 
        lines = f.readlines() 
        f.close() 
        for line in lines: 
            if len(line) < 2: continue 
            name = line.split(':')[0] 
            var = line.split(':')[1].split()[0] 
            mem[name] = long(var) * 1024.0 
        mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached'] 
        memreturn = {'MemTotal':mem['MemTotal'], 'MemFree':mem['MemFree']}
        return memreturn

    def cpu_stat(): 
        cpu = [] 
        cpuinfo = {} 
        f = open("/proc/cpuinfo") 
        lines = f.readlines() 
        f.close() 
        for line in lines: 
            if line == 'n': 
                cpu.append(cpuinfo) 
                cpuinfo = {} 
            if len(line) < 2: continue 
            name = line.split(':')[0].rstrip() 
            var = line.split(':')[1] 
            cpuinfo[name] = var 
        return  cpuinfo
     

    def net_stat(): 
        net = [] 
        f = open("/proc/net/dev") 
        lines = f.readlines() 
        f.close() 
        for line in lines[2:]: 
            con = line.split() 
            """ 
            intf = {} 
            intf['interface'] = con[0].lstrip(":") 
            intf['ReceiveBytes'] = int(con[1]) 
            intf['ReceivePackets'] = int(con[2]) 
            intf['ReceiveErrs'] = int(con[3]) 
            intf['ReceiveDrop'] = int(con[4]) 
            intf['ReceiveFifo'] = int(con[5]) 
            intf['ReceiveFrames'] = int(con[6]) 
            intf['ReceiveCompressed'] = int(con[7]) 
            intf['ReceiveMulticast'] = int(con[8]) 
            intf['TransmitBytes'] = int(con[9]) 
            intf['TransmitPackets'] = int(con[10]) 
            intf['TransmitErrs'] = int(con[11]) 
            intf['TransmitDrop'] = int(con[12]) 
            intf['TransmitFifo'] = int(con[13]) 
            intf['TransmitFrames'] = int(con[14]) 
            intf['TransmitCompressed'] = int(con[15]) 
            intf['TransmitMulticast'] = int(con[16]) 
            """ 
            intf = dict( 
                zip(
                    ( 'interface','ReceiveBytes','ReceivePackets', 
                      'ReceiveErrs','ReceiveDrop','ReceiveFifo', 
                      'ReceiveFrames','ReceiveCompressed','ReceiveMulticast', 
                      'TransmitBytes','TransmitPackets','TransmitErrs', 
                      'TransmitDrop', 'TransmitFifo','TransmitFrames', 
                      'TransmitCompressed','TransmitMulticast' ), 
                    ( con[0].rstrip(":"),int(con[1]),int(con[2]), 
                      int(con[3]),int(con[4]),int(con[5]), 
                      int(con[6]),int(con[7]),int(con[8]), 
                      int(con[9]),int(con[10]),int(con[11]), 
                      int(con[12]),int(con[13]),int(con[14]), 
                      int(con[15]),int(con[16]), ) 
                ) 
            ) 
     
            net.append(intf) 
        return net 

    def uptime_stat(): 
        uptime = {} 
        f = open("/proc/uptime") 
        con = f.read().split() 
        f.close() 
        all_sec = float(con[0]) 
        MINUTE,HOUR,DAY = 60,3600,86400 
        uptime['day'] = int(all_sec / DAY ) 
        uptime['hour'] = int((all_sec % DAY) / HOUR) 
        uptime['minute'] = int((all_sec % HOUR) / MINUTE) 
        uptime['second'] = int(all_sec % MINUTE) 
        uptime['Free rate'] = float(con[1]) / float(con[0]) 
        return uptime 

    def disk_stat():  #磁盘使用空间,单位Byte
        import os 
        hd={} 
        disk = os.statvfs("/") 
        hd['available'] = disk.f_bsize * disk.f_bavail 
        hd['capacity'] = disk.f_bsize * disk.f_blocks 
        hd['used'] = disk.f_bsize * disk.f_bfree 
        return hd

    sendpacket = {'cpu_stat':cpu_stat(), 'mem_stat':memory_stat(), 'net_stat':net_stat(), 'runtime_stat':uptime_stat(), 'disk_stat':disk_stat()}
    
    sock.send(str(sendpacket))
    time.sleep(1)

#socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 9999))
s.listen(5)
print('Waiting for connection...')

while True:
    sock, addr = s.accept()
    
    while True:
        tcplink(sock, addr)
