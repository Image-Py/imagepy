# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:22:53 2017

@author: yxl
"""

class WindowsManager:
    windows = []
    
    @classmethod
    def add(cls, win):
        if win in cls.windows: 
            cls.windows.remove(win)
        cls.windows.insert(0, win)
        
    @classmethod
    def remove(cls, win):
        if win in cls.windows: 
            cls.windows.remove(win)
            
    @classmethod
    def get(cls, title=None):
        if len(cls.windows)==0:return None
        if title==None:return cls.windows[0]
        titles = [i.canvas.ips.title for i in cls.windows]
        if not title in titles:return None
        return cls.windows[titles.index(title)]
          
    @classmethod
    def get_titles(cls):
        return [i.canvas.ips.title for i in cls.windows]
        
    @classmethod
    def name(cls, name):
        if name==None:name='Undefined'
        titles = [i.canvas.ips.title for i in cls.windows]
        if not name in titles : return name
        for i in range(1, 100) : 
            if not name+'-%s'%i in titles:
                return name+'-%s'%i
                
    @classmethod
    def close(cls, name):
        win = cls.get(name)
        if win==None:return
        cls.remove(win)
        win.Close()
        
class TextLogManager:
    windows = {}
    
    @classmethod
    def name(cls, name):
        print(list(cls.windows.keys()), name)
        if name==None:name='Log'
        if name not in cls.windows:
            return name
        for i in range(1, 100) : 
            if name+'-%s'%i not in cls.windows:
                return name+'-%s'%i
                
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
        
class TableLogManager:
    windows = {}
    
    @classmethod
    def name(cls, name):
        if name==None:name='Table'
        if name not in cls.windows:
            return name
        for i in range(1, 100) : 
            if (not name+'-%s'%i) not in cls.windows:
                return name+'-%s'%i
                
    @classmethod
    def add(cls, title, win):
        cls.windows[title] = win
        
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

class PlotManager:
    windows = {}
    @classmethod
    def get(cls, title):
        if title in cls.windows:
            return cls.windows[title]
        return None

    @classmethod
    def add(cls, title, win):
        cls.windows[title] = win

    @classmethod
    def remove(cls, name):
        if name in cls.windows: 
            cls.windows.pop(name)

    @classmethod
    def close(cls, name):
        win = cls.get(name)
        if win==None:return
        cls.remove(name)
        win.Close()