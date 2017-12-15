import os
from ... import root_dir
from glob import glob
from .configmanager import ConfigManager
from codecs import open

class LanguageManager:
    plgs = []
    langs = {}
    cur = None
    filename = os.path.join(root_dir,'data/language/*.dic')

    @classmethod
    def set(cls, cur):
        cls.cur = None if cur=='English' else cls.langs[cur]
        ConfigManager.set('language', cur)

    @classmethod
    def read(cls):
        path = os.path.join(root_dir,'data/language/*.dic')
        for name in glob(path):
            pkl_file = open(name, 'r', 'utf-8')
            fp, fn = os.path.split(name)
            fn, fe = os.path.splitext(fn)
            cls.langs[fn] = {}
            for line in pkl_file.readlines():
                k,v = line.replace('\n', '').replace('\r', '').split(':')
                cls.langs[fn][k] = v
            pkl_file.close()
        
        cur = ConfigManager.get('language')
        if cur is None: return
        if cur in cls.langs: cls.cur = cls.langs[cur]
         
    @classmethod
    def write(cls):
        for key in cls.langs:
            dic = cls.langs[key]
            titles = sorted(dic.keys())
            pkl_file = open(os.path.join(root_dir,'data/language/%s.dic'%key), 'w', 'utf-8')
            for i in titles:
                pkl_file.write('%s:%s\n'%(i,dic[i]))
            pkl_file.close()
    
    @classmethod
    def add(cls, key=None):
        if not key is None and not ':' in key:
            if not key in cls.plgs:cls.plgs.append(key)
            return
        titles = cls.plgs
        for key in cls.langs:
            dic = cls.langs[key]
            for i in titles:
                if not ':' in i and not i in dic: dic[i] = '--'
        cls.write()

    @classmethod 
    def rm(cls):
        titles = cls.plgs
        for key in cls.langs:
            dic = cls.langs[key]
            for i in list(dic.keys()):
                if not i in titles: del dic[i]
        cls.write()

    @classmethod 
    def newdic(cls, key):
        cls.langs[key] = {}
        for i in cls.plgs: 
            if not ':' in i: cls.langs[key][i] = '--'
     
    @classmethod 
    def get(cls, key):
        if not cls.cur is None and key in cls.cur: 
            if cls.cur[key]!='--':
                return cls.cur[key]
        return key

LanguageManager.read()

if __name__ == '__main__':
    #ShotcutManager.set('c',[1,2,3])
    ShotcutManager.rm('c')
    print(ShotcutManager.shotcuts)
    ShotcutManager.write()
    