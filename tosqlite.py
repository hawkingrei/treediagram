#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import feedparser
import os
import sys
import sqlite3
import urllib2
import time
import socket

#request = urllib2.Request("http://blog.csdn.net/rss.html?type=Home&channel=")
#request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:24.0) Gecko/20130619 Firefox/24.0')
#print urllib2.urlopen(request).read()
#f = feedparser.parse('http://cnbeta.feedsportal.com/c/34306/f/624776/index.rss')
#f = feedparser.parse('http://blog.csdn.net/rss.html?type=Home&channel=')
def isextist(title,link,description,publisher):
    text=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    text=text+"/db/reader.db"
    con = sqlite3.connect(text)
    cur = con.cursor()
    cur.execute("select * from reader where title=(?) and link=(?) and publisherid=(?)",(title,link,publisher))
    if (len(cur.fetchall())==0):
        cur.close()
        con.close()
        return 1
    else:
        cur.close()
        con.close()
        return 0
    
def add(http,publisherid):
    total=0
    timeout = 20    
    socket.setdefaulttimeout(timeout)
    try:
        request = urllib2.Request(http)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')
        print "head"
        fp= feedparser.parse(http)
        print "fp"
    except:
        return 0
    text=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    text=text+"/db/reader.db"
    con = sqlite3.connect(text)
    con.text_factory=str
    cur = con.cursor()
    print u"链接数据库"
    try:
        cur.execute('CREATE TABLE reader(id integer primary key autoincrement,title,link,description,time,publisherid)')
        
    except:
        {}
    for entry in fp.entries:
            try:
                title=entry.title
                link=entry.link
                try:
                    description=entry.description
                except:
                    try:
                        description=entry.content
                    except:
                        description=''
                t=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                
                if (isextist(title,link,description,publisherid)) :
                    con.execute('insert into reader(title,link,description,time,publisherid) values(?,?,?,?,?)',(title,link,description,t,publisherid))
                    print entry.title
                    total=total+1
                    con.commit()
            except:
                0

    cur.close()
    con.close()
    return total

def compact_sqlite3_db():
    try:
        text=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
        text=text+"/db/reader.db"
        conN = sqlite3.connect(text)
        conn.execute("VACUUM")
        conn.close()
        return True
    except:
        return False
    
