#!/usr/bin/env python
#coding: utf-8

#Script zum schnellen sharen einer Datei via Own- oder NextCloud. 
#benötigt eine config-datei in $HOME/.config/nextshare/ 
#dort bitte config.conf: mit folgenden Zeilen anlegen:
#login = max
#passwort = geheim
#url = Next- oder OwnCloud-URL ohne remote.php
#folder = Verzeichnis zum Sharen auf der Cloud
#mit chmod 700 $HOME/.config/nextshare/ das Verzeichnis nur für dich lesbar machen


import owncloud
import sys,getopt
import os


def main():
    cnf = ''
    for i in range(len(sys.argv)):
        if i == 1:
           upload = (sys.argv[i])
        if i == 2: 
           cnf = (sys.argv[i])
    upfile = upload
    print (upload + cnf)
    up = os.path.basename(upfile)
    if cnf <> '':
       config = ('/home/' + os.getlogin() + '/.config/nextshare/' + cnf + '.conf')
    else:
       path = ('/home/' + os.getlogin() + '/.config/nextshare/')
       files=sorted(os.listdir(path)) 
       for fname in files: 
           config = (path + fname) 
           if config == '':
              print('Keine Konfiguration in ' + '/home/' + os.getlogin() + '/.config/nextshare/ gefunden!')
              print('dort bitte config.conf: mit folgenden Zeilen anlegen:')
              print('login = max')
              print('passwort = geheim')
              print('url = Next- oder OwnCloud-URL ohne remote.php')
              print('folder = Verzeichnis zum Sharen') 
              sys.exit()
    print ('Benutze: ' + config)
    configstring = getconfig(config)
    url = (configstring.rstrip().split(' '))[0] 
    folder = (configstring.rstrip().split(' '))[1] 
    login = (configstring.rstrip().split(' '))[2] 
    passwort = (configstring.rstrip().split(' '))[3] 
    

    oc = owncloud.Client(url)

    oc.login(login, passwort)

    #oc.mkdir('testdir')
    
    print(upfile + ' -> ' + folder+'/'+up)

    oc.put_file(folder+'/'+up, upfile)

    link_info = oc.share_file_with_link(folder+'/'+up)

    print "Link: " + link_info.get_link()

def getconfig(config):
    
        c = open(config,'r')
        for line in c:
            line = line.replace(' ', '')
            variable = (line.rstrip().split('='))[0] 
            wert = (line.rstrip().split('='))[1] 
            if variable == 'login':
               login = wert
            elif variable == 'passwort':
               passwort = wert
            elif variable == 'url':
               url = wert
            elif variable == 'folder':
               folder = wert
            else:
               print('Hu? "' + line + '" ????')

        return(url + ' ' + folder + ' ' + login + ' ' + passwort)



if __name__ == '__main__':
       
       main()
