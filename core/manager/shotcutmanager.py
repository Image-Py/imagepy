# -*- coding: utf-8 -*-
import os

class ShotcutManager:
    shotcuts = {}
    @classmethod
    def read(cls):
        if os.path.exists('shotcut.cfg'):
            pkl_file = open('shotcut.cfg','rb')
            cls.shotcuts = eval(pkl_file.readline())
            pkl_file.close()
         
    @classmethod
    def write(cls):
        pkl_file = open('shotcut.cfg', 'wb')
        pkl_file.write(str(cls.shotcuts))
        pkl_file.close()
    
    @classmethod
    def get(cls, key):
        if cls.shotcuts.has_key(key):
            return cls.shotcuts[key]
        return None
        
    @classmethod  
    def set(cls, key, value):
        cls.shotcuts[key] = value   

    @classmethod
    def rm(cls, key):
        if cls.shotcuts.has_key(key):
            cls.shotcuts.pop(key)
    
ShotcutManager.read()

if __name__ == '__main__':
    #ShotcutManager.set('c',[1,2,3])
    ShotcutManager.rm('c')
    print ShotcutManager.shotcuts
    ShotcutManager.write()
    