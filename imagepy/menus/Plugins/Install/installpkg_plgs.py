# -*- coding: utf-8 -*-
from sciapp.action import Free
import subprocess, sys
import pandas as pd

class Install(Free):
    title = 'Install Packages'
    para = {'pkg':'', 'update':False}
    view = [(str, 'pkg', 'package', ''),
            (bool, 'update', 'update')]

    def run(self, para=None):
        cmds = [sys.executable, '-m', 'pip', 'install', para['pkg']]
        if para['update']: cmds.append('--upgrade')
        subprocess.call(cmds)

class List(Free):
    title = 'List Packages'

    def run(self, para=None):
        p = subprocess.Popen('%s -m pip list'%sys.executable, 
        stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)  
        lst = str(p.stdout.read(), encoding='utf-8').replace('\r\n', '\n').split('\n')
        self.app.show_table(pd.DataFrame([[i] for i in lst], columns=['Packages']), 'Packages')


plgs = [Install, List]