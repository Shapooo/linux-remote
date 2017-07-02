#!/usr/bin/env python
# coding:utf-8

import time
import socket


# def readtarget():
#     global server_list
#     with open(r"servers.txt") as f:
#         for line in f.readlines():
#             if line[0:1] != "#" and len(line.split(".")) == 4:
#                 server_list.append(line)


def connserver(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while True:
        print "\n[*] Please input command:"
        data = raw_input()
        if not data:
            break
        s.sendall(data)
        recvdata = s.recv(1024)
        print "[+] Send %s:%s -> %s" % (host, str(connPort), data)
        time.sleep(0)
        if recvdata:
            print "[+] Receive :%s" % recvdata
        if data == "close session":
            s.close()
            break


if __name__ == "__main__":
    host = '192.168.1.201'
    connPort = 47091

    # readtarget()
    # if server_list != []:
    #     for host in server_list:
    connserver(host, connPort)
