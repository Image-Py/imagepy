# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:22:53 2017
@author: yxl
"""
import weakref

class WindowsManager:
    wins = []

    @classmethod
    def add(cls, win):
        if win in cls.wins: cls.remove(win)
        cls.wins.insert(0, win)

    @classmethod
    def get(cls, title=None):
        if len(cls.wins)==0:return None
        if title==None:return cls.wins[0]
        titles = [i.ips.title for i in cls.wins]
        if not title in titles:return None
        return cls.wins[titles.index(title)]

    @classmethod
    def remove(cls, win):
        for i in cls.wins:
            if i == win: 
                cls.wins.remove(i)

class ImageManager:
    imgs = []

    @classmethod
    def add(cls, ips):
        print(ips)
        cls.remove(ips)
        callback = lambda a: cls.remove(a())
        def callback(a):
            print('image removed')
            cls.remove(a())
        print('image add!')
        cls.imgs.insert(0, weakref.ref(ips, callback))
        
    @classmethod
    def remove(cls, ips):
        for i in cls.imgs:
            if i() == ips: cls.imgs.remove(i)
            
    @classmethod
    def get(cls, title=None):
        if len(cls.imgs)==0:return None
        if title==None:return cls.imgs[0]()
        titles = [i().title for i in cls.imgs]
        if not title in titles:return None
        return cls.imgs[titles.index(title)]()
          
    @classmethod
    def get_titles(cls):
        return [i().title for i in cls.imgs]
        
    @classmethod
    def name(cls, name):
        if name==None:name='Undefined'
        titles = [i().title for i in cls.imgs]
        if not name in titles :
            return name
        for i in range(1, 100) : 
            title = "{}-{}".format(name,i)
            if not title in titles:
                return title
        
class TextLogManager:
    windows = {}
    
    @classmethod
    def name(cls, name):
        if name==None:name='Log'
        if name not in cls.windows:
            return name
        for i in range(1, 100) : 
            title = "{}-{}".format(name,i)
            if title not in cls.windows:
                return title
                
    @classmethod
    def add(cls, title, win):
        cls.windows[title] = win
        print(list(cls.windows.keys()))
        
    @classmethod
    def remove(cls, name):
        if name in cls.windows: 
            cls.windows.pop(name)
            
    @classmethod
    def get(cls, title):
        if title in cls.windows:
            return cls.windows[title]
        return None
          
    @classmethod
    def get_titles(cls):
        return list(cls.windows.keys())
                
    @classmethod
    def close(cls, name):
        win = cls.get(name)
        if win==None:return
        cls.remove(name)
        win.Close()
        
class WTableManager:
    wins = []

    @classmethod
    def add(cls, win):
        if not win in cls.wins:cls.wins.append(win)

    @classmethod
    def get(cls, title=None):
        if len(cls.wins)==0:return None
        if title==None:return cls.wins[0]
        titles = [i.grid.tps.title for i in cls.wins]
        if not title in titles:return None
        return cls.wins[titles.index(title)]

    @classmethod
    def remove(cls, win):
        for i in cls.wins:
            if i == win: 
                cls.wins.remove(i)
                print('remove', i.grid.tps.title)

class TableManager:
    tabs = []

    @classmethod
    def add(cls, tps):
        print(tps)
        cls.remove(tps)
        callback = lambda a: cls.remove(a())
        def callback(a):
            print('table removed')
            cls.remove(a())
        print('table add!')
        cls.tabs.insert(0, weakref.ref(tps, callback))
        
    @classmethod
    def remove(cls, tps):
        for i in cls.tabs:
            if i() == tps: cls.tabs.remove(i)
            
    @classmethod
    def get(cls, title=None):
        if len(cls.tabs)==0:return None
        if title==None:return cls.tabs[0]()
        titles = [i().title for i in cls.tabs]
        if not title in titles:return None
        return cls.tabs[titles.index(title)]()
          
    @classmethod
    def get_titles(cls):
        return [i().title for i in cls.tabs]
        
    @classmethod
    def name(cls, name):
        if name is None: name='Table'
        titles = [i().title for i in cls.tabs]
        if not name in titles :
            return name
        for i in range(1, 100) : 
            title = "{}-{}".format(name,i)
            if not title in titles:
                return title

class PlotManager:
    windows = []

    @classmethod
    def add(cls, win):
        cls.remove(win)
        callback = lambda a: cls.remove(a())
        cls.windows.insert(0, weakref.ref(win, callback))
        
    @classmethod
    def remove(cls, win):
        for i in cls.windows:
            if i() == win: cls.windows.remove(i)
            
    @classmethod
    def get(cls, title=None):
        if len(cls.windows)==0:return None
        if title==None:return cls.windows[0]()
        titles = [i().title for i in cls.windows]
        if not title in titles:return None
        return cls.windows[titles.index(title)]()
          
    @classmethod
    def get_titles(cls):
        return [i().title for i in cls.windows]
        
    @classmethod
    def name(cls, name):
        if name==None:name='Table'
        titles = [i().title for i in cls.windows]
        if not name in titles :
            return name
        for i in range(1, 100) : 
            title = "{}-{}".format(name,i)
            if not title in titles:
                return title
                
    @classmethod
    def close(cls, name):
        win = cls.get(name)
        if win==None:return
        cls.remove(win)
        win.close()