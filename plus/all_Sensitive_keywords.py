#!/usr/bin/python2.7
#coding:utf-8

import re

keywords=[
            'serv-u',
            'wscript.shell',
            'phpspy',
            'jspspy',
            'webshell','shell.application',
            'documents and settings/all users',
            '挂马',
            '大马'
            'getruntime().exec',
            '$_[+""]=\'\'',
            'chr(99).chr(104).chr(114)',
            'chr($a[79]).chr($a[78])',
            '"ass"."ert"'
        ]

heiyekeywords=[
            'sohu999.com',
            '8y10086.com',
        ]

knownshell=[
            '%74%68%36%73%62%65%68%71%6c%61%34%63%6f%5f%73%61%64%66%70%6e%72',
            'ixcixreaixteix_ixfixuixnixctixioixn',
            'r57shell',

        ]

rulelist=[
    '[\'"]e[\'"]\.[\'"]v[\'"]\.[\'"]a[\'"]\.[\'"]l[\'"]',
    '[\'"]a[\'"]\.[\'"]s[\'"]\.[\'"]s[\'"]\.[\'"]e[\'"]\.[\'"]r[\'"]\.[\'"]t[\'"]'
]



#此插件白名单列表 (['文件路径'],['误报特征码'])
whitefilter=[
                (['spellchecker.cfm'],['Program Files']),
]

whitefilter1=['spellchecker.cfm']

def Check(filestr,filepath):

    filestr = filestr.lower()

    #纯关键词查找-暂不确定后门
    for key in keywords:
        if key in filestr:
            isok=1
            for white in whitefilter:
                if white[0][0] in filepath.replace('\\','/') and white[1][0] in key:
                    isok=0
            if isok:
                return ((key,),),'后门敏感关键字'

    #纯黑网址、非法网址关键词查找
    for key in heiyekeywords:
        if key in filestr:
                return ((key,),),'非法网址（如博彩）关键字'


    #纯关键词查找-确定后门
    for key in knownshell:
        if key in filestr:
            isok=1
            for white in whitefilter:
                if white[0][0] in filepath.replace('\\','/') and white[1][0] in key:
                    isok=0
            if isok:
                return ((key,),),'已知后门特征'

    #按正则查找
    for rule in rulelist:
        result = re.search(rule,filestr)
        try:

            if result.group():
                return ((result.group(),),),'已知后门特征'
        except:
            pass

    #组合特征查找
    if 'cmd.exe' in filestr and 'program files' in filestr:
        isok=1
        for white in whitefilter1:
            if white in filepath.replace('\\','/'):
                isok=0
        if isok:
            return (('cmd.exe和Program Files',),),'敏感后门关键字'

    #敏感关键字，已知后门类型
    if 'www.phpdp.org' in filestr:
        return (('www.phpdp.org',),),'PHP神盾加密后门敏感关键字'

    if 'www.phpjm.net' in filestr:
        return (('www.phpjm.net',),),'PHP加密后门敏感关键字'

    return None
