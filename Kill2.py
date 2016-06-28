#!/usr/bin/python2.7
#coding:utf-8


import os
import sys
import time
import ConfigParser

config = ConfigParser.ConfigParser()


def setIni(section,name,value):
    config.add_section(section)
    config.set(section, name, value)
    f = open("config.ini", "a+")
    config.write(f)
    f.close

def getIni(section,name=''):
    # a =  getIni('FILE_EXT');
    # print a[0][1]

    config.read("config.ini")
    if not name:
        return config.items(section)
    else:
        return config.get(section, name)


plusarr=[] #插件列表
backdoor_count=0


exts = getIni('FILE_EXT','ext');
fielsize = getIni('FILE_SIZE','size');
version = getIni('FILE_VER','ver');



def loadplus():
    for root,dirs,files in os.walk("plus"):
        for filespath in files:
            if filespath[-3:] == '.py':
                plusname = filespath[:-3]
                if plusname=='__init__':
                    continue
                __import__('plus.'+plusname)
                plusarr.append(plusname)


def Scan(path):
    loadplus() #动态加载插件
    global backdoor_count
    for root,dirs,files in os.walk(path):
        for filename in files:
            file_ext = filename.split('.').pop();
            if file_ext in exts.split(','):
                filepath = os.path.join(root,filename)
                if os.path.getsize(filepath)<fielsize:
                    for plus in plusarr:
                        with open(filepath,"rb") as file:
                            filestr = file.read()
                            result = sys.modules['plus.'+plus].Check(filestr,filepath)

                            if result!=None:
                                print '文件: ',
                                print filepath
                                print '后门描述: ',
                                print result[1]
                                print '后门代码: ',
                                for code in result[0]:
                                    print code[0][0:100]
                                print '最后修改时间: '+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(filepath)))+'\n\n'
                                backdoor_count= backdoor_count+1
                                break

def ScanFiletime(path,times):
    global backdoor_count
    times = time.mktime(time.strptime(times, '%Y-%m-%d %H:%M:%S'))
    print '########################################'
    print '文件路径           最后修改时间   \n'

    for root,dirs,files in os.walk(path):
        for curfile in files:
            if '.' in curfile:
                suffix = curfile[-4:].lower()
                filepath = os.path.join(root,curfile)
                if suffix=='.php' or suffix=='.jsp':
                    FileTime =os.path.getmtime(filepath)
                    if FileTime>times:
                        backdoor_count +=1
                        print filepath+'        '+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(FileTime))


if __name__ == "__main__":

    print '\n-----------------------------------------------'
    print """
    KillShell is a webshell kill tools write by jincon
    Ver     :  """+version+"""
    Author  :  Jincon
    Website :  http://www.jincon.com
    Usage   :  Kill2.py Directory
    """
    print '-----------------------------------------------\n'

    if len(sys.argv)!=3 and len(sys.argv)!=2:
        print '【参数错误】'
        print '\t按恶意代码查杀: '+sys.argv[0]+' 目录名'
        print '\t按修改时间查杀: '+sys.argv[0]+' 目录名 最后修改时间(格式:"2013-09-09 12:00:00")'
        exit()

    if os.path.lexists(sys.argv[1])==False:
        print '【错误提示】：指定的扫描目录不存在--- '
        exit()

    if len(sys.argv)==2:
        t1 = time.time();
        print '\n\n【开始查杀】'
        print sys.argv[1]+'\n'
        Scan(sys.argv[1])
        t2 = time.time();
        print '【查杀完成】\n'
        print '【查杀耗时】: '+str(t2-t1)+'s\n'
        print '【后门总数】: '+str(backdoor_count)
    else:
        print '\n\n【开始查找】'
        print sys.argv[1]+'\n'
        ScanFiletime(sys.argv[1],sys.argv[2])
        print '\n【查找完成】'
        print '文件总数: '+str(backdoor_count)