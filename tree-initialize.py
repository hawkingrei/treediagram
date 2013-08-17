#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import sqlite3
import sys
import os
import xml.dom.minidom as minidom
import tosqlite
import time
#性能测试
import profile


def add(): 
    text=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    print text
    text=text+"/db/subscriptions.db"
    con = sqlite3.connect(text)
    con.text_factory=str
    cur = con.cursor()
    try:
        cur.execute('CREATE TABLE subs(id integer primary key autoincrement,title,htmlurl,xmlurl,type,text)')
        con.commit()
    except:
        pass
    doc = minidom.parse("subscriptions.xml")
    root = doc.documentElement
    employees=root.getElementsByTagName("body")
    for employee in employees:
        cnodes=employee.getElementsByTagName("outline")
        for cnode in cnodes:
                RssTitle=cnode.getAttribute("title")
                RssHtmlurl=cnode.getAttribute("htmlUrl")
                RssXmlurl=cnode.getAttribute("xmlUrl")
                RssType=cnode.getAttribute("type")
                RssText=cnode.getAttribute("text")
                print RssTitle
                con.execute('insert into subs(title,htmlurl,xmlurl,type,text) values(?,?,?,?,?)',(RssTitle,RssHtmlurl,RssXmlurl,RssType,RssText))
                con.commit()
    cur.close()
    con.close()
def find():
    total=0
    ttotal=0
    text=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    text=text+"/db/subscriptions.db"
    con = sqlite3.connect(text)
    cur = con.cursor()
    cur.execute("select * from subs")
    for d in cur.fetchall():        
        print d[0]
        total=tosqlite.add(d[3],d[0])
        if (total):
            print "total:"+str(total)
            ttotal=ttotal+total
    return ttotal

ttotal=0
while (1):
	total=0
	total=total+find()
	ttotal=ttotal+total
	print "total        :"+str(total)
	print "t:             "+str(ttotal)
	time.sleep(300)
    
    
        

#获取脚本运行目录  
#print os.getcwd() 

