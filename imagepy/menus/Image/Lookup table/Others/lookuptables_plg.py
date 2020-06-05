from ..lookuptables_plg import LUT
from sciapp import Source

plgs = [LUT(i, j) for i, j, _ in Source.manager('colormap').gets(tag='adv')]