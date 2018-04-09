# -*- coding: utf-8 -*-
from imagepy import IPy
from imagepy.core.engine import Free
import subprocess, sys

class Install(Free):
    title = 'Install Packages'
    para = {'pkg':'', 'update':False}
    view = [(str, 'package', 'pkg', ''),
            (bool, 'update', 'update')]

    def run(self, para=None):
        cmds = '%s -m pip install '%sys.executable + para['pkg']
        if para['update']: cmds+' --update'
        subprocess.call(cmds)

class List(Free):
    title = 'List Packages'

    def run(self, para=None):
        p = subprocess.Popen('%s -m pip list'%sys.executable, 
        stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)  
        lst = str(p.stdout.read(), encoding="utf-8").split('\r\n')
        IPy.table('Packages', [[i] for i in lst], ['Packages'])


plgs = [Install, List]