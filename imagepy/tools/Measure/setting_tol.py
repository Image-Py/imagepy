import wx
import numpy as np
from imagepy.core.engine import Tool
from imagepy.tools.Measure.setting import Setting

class Plugin(Tool):
    title = 'Measure Setting'
    para = Setting
    view = [('color', 'line', 'color', 'color'),
            ('color', 'text', 'tcolor', 'color')]

    def __init__(self):
        pass

    def mouse_down(self, ips, x, y, btn, **key):
        pass