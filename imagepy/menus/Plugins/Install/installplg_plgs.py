# -*- coding: utf-8 -*-
from imagepy import root_dir
from sciapp.action import Free
import os, subprocess, zipfile, shutil

import zipfile, sys, urllib
path = 'https://github.com/Image-Py/imagepy/archive/master.zip'

from urllib.request import urlretrieve
import urllib
from io import BytesIO as StringIO

path_plgs = os.path.join(root_dir, 'plugins')
path_cache = os.path.join(path_plgs, 'cache')
if not os.path.exists(path_plgs):
    os.mkdir(path_plgs)
if not os.path.exists(path_cache):
    os.mkdir(path_cache)

def Schedule(a,b,c, plg):
    per = 100.0 * a * b / c
    if per > 100 : per = 100
    plg.progress(int(per), 100)
    if c==-1: plg.prgs = None

class Install(Free):
    title = 'Install Plugins'
    para = {'repo':'https://github.com/Image-Py/IBook', 'proxy': False, 'Protocol': 'https', 'IP': '127.0.0.1', 'Port': '1080'}
    view = [('lab', None, 'input a zipfile url or github url as http://github.com/username/project'),
            (str, 'repo', 'package', ''),
            (bool, 'proxy', 'Use proxy'),
            (list, 'Protocol', ['socks5', 'http', 'https'], str, 'Protocol', ''),
            (str, 'IP', 'IP Address', ''),
            (str, 'Port', 'Port', '')]

    def run(self, para=None):
        url = para['repo']
        if 'github.com' in url:
            if url[-4:] == '.git':
                url = url.replace('.git', '/archive/master.zip')
            elif url[-4:] != '.zip':
                url = url + '/archive/master.zip'
            domain, name = url.split('/')[-4:-2]
        else:
            domain, name = (url[:-4].replace('.','-')).split('/')[-2:]
        domain, name = domain.replace('_', '-'), name.replace('_', '-')

        self.app.info('downloading plugin from %s'%para['repo'])

        if True == para['proxy']:
            proxy=para['Protocol']+"://"+para['IP']+":"+para['Port']
            print("proxy = ", proxy)
            # Build ProxyHandler object by given proxy
            proxy_support=urllib.request.ProxyHandler({para['Protocol']:proxy})
            # Build opener with ProxyHandler object
            opener = urllib.request.build_opener(proxy_support)
            # Install opener to request
            urllib.request.install_opener(opener)

        urlretrieve(url, os.path.join(path_cache, domain+'_'+name+'.zip'), 
            lambda a,b,c, p=self: Schedule(a,b,c,p))
        zipf = zipfile.ZipFile(os.path.join(path_cache, domain+'_'+name+'.zip'))
        folder = zipf.namelist()[0]
        zipf.extractall(path_cache)
        destpath = os.path.join(path_plgs, domain+'_'+folder.replace('-master',''))
        if os.path.exists(destpath): shutil.rmtree(destpath)
        os.rename(os.path.join(path_cache, folder), destpath)
        zipf.close()
        self.app.info('installing requirement liberies')
        self.prgs = None
        cmds = [sys.executable, '-m', 'pip', 'install', '-r', '%s/requirements.txt'%destpath]
        subprocess.call(cmds)
        self.app.load_all()

class List(Free):
    title = 'List Plugins'

    def run(self, para=None):
        pass


plgs = [Install, List]