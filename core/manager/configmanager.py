# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:23:30 2017

@author: yxl
"""
import pickle, os

class ConfigManager:
    cfg = {}
    @classmethod
    def read(cls):
        if os.path.exists('pref.cfg'):
            pkl_file = open('pref.cfg','rb')
            cls.cfg = pickle.load(pkl_file)
            pkl_file.close()
         
    @classmethod
    def write(cls):
        pkl_file = open('pref.cfg', 'wb')
        cls = pickle.dump(cls.cfg, pkl_file, 0)
        pkl_file.close()
    
    @classmethod
    def get(cls, key):
        print cls.cfg
        if cls.cfg.has_key(key):
            return cls.cfg[key]
        return None
        
    @classmethod  
    def set(cls, key, value):
        cls.cfg[key] = value   
        print cls.cfg
    
ConfigManager.read()

if __name__ == '__main__':
    ConfigManager.set('b',[1,2,3])
    print ConfigManager.cfg
    ConfigManager.write()
    