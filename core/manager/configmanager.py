# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:23:30 2017

@author: yxl
"""
import pickle, os, IPy
#from ..imagepy import root_dir
#print root_dir

class ConfigManager:
    cfg = {}
    @classmethod
    def read(cls):
        if os.path.exists(os.path.join(IPy.root_dir, 'preference.cfg')):
            pkl_file = open(os.path.join(IPy.root_dir, 'preference.cfg'),'rb')
            cls.cfg = pickle.load(pkl_file)
            pkl_file.close()
         
    @classmethod
    def write(cls):
        pkl_file = open(os.path.join(IPy.root_dir, 'preference.cfg'), 'wb')
        cls = pickle.dump(cls.cfg, pkl_file, 0)
        pkl_file.close()
    
    @classmethod
    def get(cls, key):
        if key in cls.cfg:
            return cls.cfg[key]
        return None
        
    @classmethod  
    def set(cls, key, value):
        cls.cfg[key] = value   
    
ConfigManager.read()

if __name__ == '__main__':
    ConfigManager.set('b',[1,2,3])
    print(ConfigManager.cfg)
    ConfigManager.write()
    