# -*- coding: utf-8 -*-
from imagepy import IPy, root_dir
from imagepy.core.engine import Free
import os, subprocess, zipfile, shutil

import zipfile, sys, urllib
path = 'https://github.com/Image-Py/imagepy/archive/master.zip'

if sys.version_info[0]==2:
    from urllib import urlretrieve
    from cStringIO import StringIO
else: 
    from urllib.request import urlretrieve
    from io import BytesIO as StringIO

if not os.path.exists('./plugins'):
    os.mkdir('plugins')
if not os.path.exists('./plugins/cache'):
    os.mkdir('plugins/cache')

def Schedule(a,b,c, plg):
    per = 100.0 * a * b / c
    if per > 100 : per = 100
    print('%-3d%%'%per)
    plg.progress(int(per), 100)

class Install(Free):
    title = 'Install Plugins'
    para = {'pkg':''}
    prgs = (0, 100)
    view = [('lab', 'input a zipfile url or github url as http://github.com/username/project'),
            (str, 'package', 'pkg', '')]

    def run(self, para=None):
        url = para['pkg']
        if 'github.com' in url:
            if url[-4:] == '.git':
                url = url.replace('.git', '/archive/master.zip')
            elif url[-4:] != '.zip':
                url = url + '/archive/master.zip'
            domain, name = url.split('/')[-4:-2]
        else:
            domain, name = (url[:-4].replace('.','-')).split('/')[-2:]
        domain, name = domain.replace('_', '-'), name.replace('_', '-')

        IPy.set_info('downloading plugin from %s'%para['pkg'])
        urlretrieve(url, os.path.join('./plugins/cache', domain+'_'+name+'.zip'), 
            lambda a,b,c, p=self: Schedule(a,b,c,p))
        zipf = zipfile.ZipFile(os.path.join('./plugins/cache', domain+'_'+name+'.zip'))
        folder = zipf.namelist()[0]
        zipf.extractall('./plugins/cache')
        destpath = os.path.join('./plugins/', domain+'_'+folder).replace('-master','')
        if os.path.exists(destpath): shutil.rmtree(destpath)
        os.rename(os.path.join('./plugins/cache/', folder), destpath)
        zipf.close()
        IPy.set_info('installing requirement liberies')
        self.prgs = (None, 1)
        cmds = [sys.executable, '-m', 'pip', 'install', '-r', '%s/requirements.txt'%destpath]
        subprocess.call(cmds)
        IPy.reload_plgs(True, True, True, True)

class List(Free):
    title = 'List Plugins'

    def run(self, para=None):
        pass


plgs = [Install, List]