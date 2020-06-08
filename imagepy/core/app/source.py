from sciapp import Source
from imagepy import root_dir
import os.path as osp
from glob import glob
import numpy as np

Source.manager('plugin')
Source.manager('tool')
Source.manager('widget')
Source.manager('macros')
Source.manager('config')

Source.manager('config').read(osp.join(root_dir, 'data/config.json'))

from sciapp.object import Shape
mark_style = Source.manager('config').get('mark_style')
if not mark_style is None:
	for i in mark_style: Shape.default[i] = mark_style[i]

from sciapp.object import ROI
mark_style = Source.manager('config').get('roi_style')
if not mark_style is None:
	for i in mark_style: ROI.default[i] = mark_style[i]

from sciapp.action.meaact import Measure
mark_style = Source.manager('config').get('mea_style')
if not mark_style is None:
	for i in mark_style: Measure.default[i] = mark_style[i]

Source.manager('colormap').remove()

filenames = glob(osp.join(root_dir,'data/luts/*/*.lut'))
keys = [osp.split(filename)[-1][:-4] for filename in filenames]
values = [np.fromfile(i, dtype=np.uint8).reshape((3,256)).T.copy() for i in filenames]
for k,v in zip(keys[::-1], values[::-1]): Source.manager('colormap').add(k, v, 'adv')

filenames = glob(osp.join(root_dir, 'data/luts/*.lut'))
keys = [osp.split(filename)[-1][:-4] for filename in filenames]
values = [np.fromfile(i, dtype=np.uint8).reshape((3,256)).T.copy() for i in filenames]
for k,v in zip(keys[::-1], values[::-1]): Source.manager('colormap').add(k, v, 'base')
print(Source.manager('colormap').names)
Source.manager('colormap').add('Grays', Source.manager('colormap').get('Grays'), 'base')