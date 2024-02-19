# -*- coding: utf-8 -*-
from imagepy import root_dir
from sciapp.action import Free
import os, shutil, sys, subprocess
from dulwich import porcelain

path_plgs = os.path.join(root_dir, 'plugins')
if not os.path.exists(path_plgs): os.mkdir(path_plgs)

def Schedule(a,b,c, plg):
    per = 100.0 * a * b / c
    if per > 100 : per = 100
    plg.progress(int(per), 100)
    if c==-1: plg.prgs = None

class Install(Free):
    title = 'Install Plugins'
    para = {'repo':'https://github.com/Image-Py/IBook'}
    view = [('lab', None, 'input git url as http://github.com/username/project'),
            (str, 'repo', 'package', '')]

    def run(self, para=None):
        path = os.path.join(path_plgs, os.path.split(para['repo'])[-1])
        porcelain.clone(para['repo'], path, depth=1).close()
        shutil.rmtree(os.path.join(path, '.git'))
        self.app.info('installing requirement liberies')
        cmds = [sys.executable, '-m', 'pip', 'install', '-r', '%s/requirements.txt'%path]
        subprocess.call(cmds)
        self.app.load_all()

class List(Free):
    title = 'List Plugins'

    def run(self, para=None):
        pass


plgs = [Install, List]