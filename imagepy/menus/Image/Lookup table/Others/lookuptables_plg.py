from ..lookuptables_plg import LUT
from imagepy.app import ColorManager

plgs = [LUT(i, j) for i, j, _ in ColorManager.gets(tag='adv')]