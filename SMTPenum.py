#!/usr/bin/env python

import time
import socket

##############################################################
# To use this script, simply open a python interpreter       #
# in the directory the script is in and use the code:        #
#                                                            # 
# import SMTPEnum                                            #
# enum = SMTPenum.RCPT($targetip, $targetport, $userlistloc) #
# print enum.run()                                           # 
#                                                            #
##############################################################

#######################
class RCPT(object):
    def __init__(self, ip, port, userlist):
        self.targetIP = ip
        self.targetPort = port
        self.listLoc = userlist
        self.HELO = 'mserver.example.com'
        self.MAIL = 'root'
        self.users = []
        self.found = []

        #Read Users From File
        inFile = open(self.listLoc, 'r')
        for each in inFile:
            self.users.append(each)
        inFile.close()

    def run(self):
        for each in self.users:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((self.targetIP, int(self.targetPort)))
                banner = sock.recv(1024)
            except socket.error:
                print ("Could not connect.")
                sys.exit()
 
            sock.send('HELO ' + self.HELO + '\r\n')
            tmpdata = sock.recv(1024)
            print tmpdata

            print ('MAIL FROM:' + self.MAIL + '\r\n')
            sock.send('MAIL FROM:' + self.MAIL + '\r\n')
            tmpdata = sock.recv(1024)

            print ('Testing: ' + each)
            sock.send('RCPT TO:' + each + '\r\n')
            tmpdata = sock.recv(3)
            if tmpdata == '250':
                self.found.append(each)

        for each in self.found:
            self.found[self.found.index(each)] = each.strip('\n')

        return self.found

#######################
class VRFY(object):
    def __init__(self, ip, port, userlist):
        #Handle Parameters
        self.targetIP = ip
        self.targetPort = port
        self.listLoc = userlist
        self.users = []
        self.found = []
        self.HELO = 'mserver.example.com'

        #Read Users From File
        inFile = open(self.listLoc, 'r')
        for each in inFile:
            self.users.append(each)
        inFile.close()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((self.targetIP, int(self.targetPort)))
            
            #Grab Banner
            banner = sock.recv(1024)
            print banner
 
            sock.send('HELO ' + self.HELO + '\r\n')
            tmpdata = sock.recv(3)
            print tmpdata
            time.sleep(0.02)

            for each in self.users:
                print 'Testing: ' + each + '\n'
                sock.send('VRFY ' + each + '\r\n')
                tmpdata = sock.recv(3)
                if tmpdata == '250':
                    self.found.append(each)
                time.sleep(0.02)
            
            return self.found

        except socket.error:
            print 'Could not connect.'

