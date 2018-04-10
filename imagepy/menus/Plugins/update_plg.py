from imagepy import IPy, root_dir
from imagepy.core.engine import Free
import os, sys, os.path as osp
import zipfile, urllib
from io import BytesIO
import shutil

if sys.version_info[0]==2:
    from urllib import urlretrieve
else: 
    from urllib.request import urlretrieve

def Schedule(a,b,c, plg):
    per = 100.0 * a * b / c
    if per > 100 : per = 100
    print('%-3d%%'%per)
    plg.prgs = (int(per), 100)

class Update(Free):
    title = 'Update Software'

    def run(self, para=None):
        IPy.set_info('update now, waiting...')
        self.download_zip()
        self.deal_file()
        #self.delete_cache()
        IPy.alert('imagepy update done!')

    def download_zip(self):
        url='https://github.com/Image-Py/imagepy/archive/master.zip'
        path=osp.dirname(root_dir)
        zipname = osp.join(path, 'imagepy_cache.zip')
        print('downloading from %s'%url)
        urlretrieve(url, zipname, 
            lambda a,b,c, p=self: Schedule(a,b,c,p))

    def deal_file(self):
        path = osp.dirname(root_dir)
        #remove 
        for i in os.listdir(root_dir):
            if i in ['plugins', 'preference.cfg', '.gitignore']: continue
            if osp.isdir(osp.join(root_dir,i)): shutil.rmtree(osp.join(root_dir, i))
            else : os.remove(osp.join(root_dir,i))

        source = zipfile.ZipFile(osp.join(path, 'imagepy_cache.zip'), 'r')
        target = zipfile.ZipFile(BytesIO(), 'w')
        for i in source.namelist()[1:]: target.writestr(i[15:], source.read(i))
        target.extractall(path)
        target.close()
        source.close()
        os.remove(osp.join(path,'imagepy_cache.zip'))

class Refresh(Free):
    title = 'Reload Plugins'

    def run(self, para=None):
        IPy.reload_plgs(True, True, True, True)

plgs = [Update, Refresh]
