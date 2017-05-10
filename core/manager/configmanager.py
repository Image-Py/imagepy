# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:23:30 2017
@author: yxl
"""
import pickle, os
import IPyGL
class ConfigManager:
    cfg = {}
    filename = os.path.join(IPyGL.root_dir, "preference.cfg")
    #filename = os.path.join("/home/auss/Programs/Python/ImagePy/ImagePy3", "preference.cfg")

    @classmethod
    def read(cls):
        """Read from the congigure file: preference.cfg """
        if os.path.exists(cls.filename):
            with open(cls.filename,"rb") as pkg_file:
                cls.cfg = pickle.load(pkg_file)

    @classmethod
    def write(cls):
        """Write to the congigure file """
        with open(cls.filename,"wb") as pkg_file:
            cls = pickle.dump(cls.cfg, pkg_file, 0)

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
