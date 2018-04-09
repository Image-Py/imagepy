from imagepy import IPy
from imagepy.core.engine import Free
import sys, os
import zipfile,urllib
import shutil

if sys.version_info[0]==2:
    from urllib import urlretrieve
    from cStringIO import StringIO
else: 
    from urllib.request import urlretrieve
    from io import BytesIO as StringIO

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
        self.delete_cache()
        IPy.alert('imagepy update done!')

    def download_zip(self):
        pkg='https://github.com/Image-Py/imagepy'
        #获得前两级目录
        path=os.path.dirname(os.getcwd())
        url =pkg+'/archive/master.zip'
        name = '~'.join(pkg.split('/')[-2:])+'.zip'
        print(url, name)
        print('downloading from %s'%url)
        urlretrieve(url, os.path.join(path, name), 
            lambda a,b,c, p=self: Schedule(a,b,c,p))
        zipf = zipfile.ZipFile(os.path.join(path, name))
        zipf.extractall(path)
        destpath = os.path.join(path, name[:-4])

    def deal_file(self):
        path=os.getcwd()
        path_src=os.path.dirname(os.getcwd())
        files = os.listdir(path)
        for i in files:
            if i=='plugins' or i=='preference.cfg' or i=='__pycache__':continue
            print(i)
            if '.' in i: 
                os.remove(os.path.join(path,i))
                shutil.copyfile(os.path.join(path_src,'imagepy-master','imagepy',i),os.path.join(path,i))
            else : 
                shutil.rmtree(os.path.join(path,i))
                shutil.copytree(os.path.join(path_src,'imagepy-master','imagepy',i),os.path.join(path,i))
        files = os.listdir(os.path.join(path_src,'imagepy-master'))
        for i in files:
            if i=='imagepy' or i=='.gitignore':continue
            os.remove(os.path.join(path_src,i))
            shutil.copyfile(os.path.join(path_src,'imagepy-master',i),os.path.join(path_src,i))
    def delete_cache(self):
        path_src=os.path.dirname(os.getcwd())
        shutil.rmtree(os.path.join(path_src,'imagepy-master'))
        os.remove(os.path.join(path_src,'Image-Py~imagepy.zip'))

class Refresh(Free):
    title = 'Reload Plugins'

    def run(self, para=None):
        IPy.reload_plgs(True, True, True, True)

plgs = [Update, Refresh]
