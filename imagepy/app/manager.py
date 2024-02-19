from sciapp import Manager
from imagepy import root_dir
import os.path as osp
from glob import glob
import numpy as np

ConfigManager = Manager().read(osp.join(root_dir, 'data/config.json'))
ShortcutManager = Manager().read(osp.join(root_dir, 'data/shortcut.json'))
ColorManager = Manager()
DictManager = Manager()
DocumentManager = Manager()

if ConfigManager.get('language') is None:
	ConfigManager.add('language', 'english')

from sciapp.object import Shape
mark_style = ConfigManager.get('mark_style')
if not mark_style is None:
	for i in mark_style: Shape.default[i] = mark_style[i]

from sciapp.object import ROI
mark_style = ConfigManager.get('roi_style')
if not mark_style is None:
	for i in mark_style: ROI.default[i] = mark_style[i]

from sciapp.action import Measure
mark_style = ConfigManager.get('mea_style')
if not mark_style is None:
	for i in mark_style: Measure.default[i] = mark_style[i]

filenames = glob(osp.join(root_dir,'data/luts/*/*.lut'))
keys = [osp.split(filename)[-1][:-4] for filename in filenames]
values = [np.fromfile(i, dtype=np.uint8).reshape((3,256)).T.copy() for i in filenames]
for k,v in zip(keys[::-1], values[::-1]): ColorManager.add(k, v, 'adv')

filenames = glob(osp.join(root_dir, 'data/luts/*.lut'))
keys = [osp.split(filename)[-1][:-4] for filename in filenames]
values = [np.fromfile(i, dtype=np.uint8).reshape((3,256)).T.copy() for i in filenames]
for k,v in zip(keys[::-1], values[::-1]): ColorManager.add(k, v, 'base')
ColorManager.add('Grays', ColorManager.get('Grays'), 'base')

from sciwx import ColorManager as ColorMap
ColorMap.remove()
ColorMap.adds(ColorManager.gets(tag='base')[::-1])
