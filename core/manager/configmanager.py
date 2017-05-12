# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:23:30 2017
@author: yxl
"""
import pickle, os
from ... import root_dir
class ConfigManager:
    cfg = {}
    filename = os.path.join(root_dir, "preference.cfg")
    #filename = os.path.join("/home/auss/Programs/Python/ImagePy/ImagePy3", "preference.cfg")

    @classmethod
    def read(cls):
        """Read from the congigure file: preference.cfg """
        if os.path.exists(cls.filename):
            pkl_file = open(cls.filename,'r')
            cls.cfg = eval(pkl_file.read().replace("\n","").encode('utf8'))
            pkl_file.close()

    @classmethod
    def write(cls):
        pkl_file = open(cls.filename, 'w')
        pkl_file.write(str(cls.cfg))
        pkl_file.close()

    @classmethod
    def get(cls, key):
        """Get the congigure item """
        return cls.cfg[key]  if key in cls.cfg else None

    @classmethod
    def set(cls, key, value):
        """Set the congigure item """
        cls.cfg[key] = value

# call the read function so that initial the ConfigManager
ConfigManager.read()

if __name__ == '__main__':
    ConfigManager.set('b',[1,2,3])
    print(ConfigManager.cfg)
    ConfigManager.write()
