import os
from ... import root_dir

class ShotcutManager:
    shotcuts = {}
    filename = os.path.join(root_dir,'data/shotcut.cfg')
    @classmethod
    def read(cls):
        if os.path.exists(cls.filename):
            pkl_file = open(cls.filename,'r')
            cls.shotcuts = eval(pkl_file.read().replace("\n","").encode('utf8'))
            pkl_file.close()
         
    @classmethod
    def write(cls):
        pkl_file = open(cls.filename, 'w')
        pkl_file.write(str(cls.shotcuts))
        pkl_file.close()
    
    @classmethod
    def get(cls, key):
        if key in cls.shotcuts:
            return cls.shotcuts[key]
        return None
        
    @classmethod  
    def set(cls, key, value):
        cls.shotcuts[key] = value   

    @classmethod
    def rm(cls, key):
        if key in cls.shotcuts:
            cls.shotcuts.pop(key)
    
ShotcutManager.read()

if __name__ == '__main__':
    #ShotcutManager.set('c',[1,2,3])
    ShotcutManager.rm('c')
    print(ShotcutManager.shotcuts)
    ShotcutManager.write()
    