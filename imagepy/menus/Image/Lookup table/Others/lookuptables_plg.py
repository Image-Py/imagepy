# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:13:42 2016
@author: yxl
"""
from imagepy import IPy, root_dir
import os, glob
from ..lookuptables_plg import Plugin

fs = glob.glob(os.path.join(root_dir,'data/luts/Others/*.lut'))
plgs = [Plugin(i) for i in [os.path.split(f)[-1][:-4] for f in fs]]