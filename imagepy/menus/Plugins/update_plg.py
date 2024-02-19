from sciapp.action import Free
import os, sys, os.path as osp
from imagepy import root_dir
from dulwich import porcelain
import shutil

class Update(Free):
    title = 'Update Software'

    def run(self, para=None):
        self.app.info('update now, waiting...')
        url = 'https://gitee.com/imagepy/imagepy'
        path = osp.dirname(root_dir); rpath = osp.dirname(path)
        newpath = osp.join(rpath, 'imagepy_new')
        if osp.exists(newpath): shutil.rmtree(newpath)
        porcelain.clone(url, os.path.join(rpath, 'imagepy_new'), depth=1).close()
        shutil.rmtree(os.path.join(os.path.join(rpath, 'imagepy_new'), '.git'))
        shutil.copytree(osp.join(path, 'imagepy/plugins'), 
            osp.join(rpath, 'imagepy_new/imagepy/plugins'))
        shutil.copyfile(osp.join(path, 'imagepy/data/config.json'), 
            osp.join(rpath, 'imagepy_new/imagepy/data/config.json'))
        shutil.copyfile(osp.join(path, 'imagepy/data/shortcut.json'), 
            osp.join(rpath, 'imagepy_new/imagepy/data/shortcut.json'))
        newpath = os.path.join(rpath, 'imagepy_new')
        fs = os.listdir(os.path.join(rpath, 'imagepy_new'))
        fs = [i for i in fs if osp.isdir(osp.join(newpath, i))]
        fs = [i for i in fs if osp.exists(osp.join(path, i))]
        for i in [j for j in fs if j!='imagepy']: shutil.rmtree(osp.join(path, i))
        for i in [j for j in fs if j!='imagepy']: 
            shutil.copytree(osp.join(newpath, i),  osp.join(path, i))
        for i in os.listdir(root_dir):
            if osp.isdir(osp.join(root_dir,i)): 
                shutil.rmtree(osp.join(root_dir, i))
            else : os.remove(osp.join(root_dir,i))
        newdir = os.path.join(newpath, 'imagepy')
        for i in os.listdir(newdir):
            if osp.isdir(osp.join(newdir, i)):
                shutil.copytree(osp.join(newdir, i), osp.join(root_dir, i))
            else: shutil.copyfile(osp.join(newdir, i), osp.join(root_dir, i))
        shutil.rmtree(newpath)
        self.app.alert('imagepy update done!')

class Refresh(Free):
    title = 'Reload Plugins'

    def run(self, para=None):
        self.app.load_all()

plgs = [Update, Refresh]
