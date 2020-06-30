from sciapp.action import Measure
from sciapp.action import Free
from imagepy.app import ConfigManager

class Plugin(Free):
    title = 'Measure Setting'
    para = Measure.default.copy()
    view = [('color', 'color', 'line', 'color'),
            ('color', 'fcolor', 'face', 'color'),
            ('color', 'tcolor', 'text', 'color'),
            (int, 'lw', (1,10), 0, 'width', 'pix'),
            (int, 'size', (1,30), 0, 'text', 'size'),
            (bool, 'fill', 'solid fill')]

    def run(self, para=None):
        for i in para: Measure.default[i] = para[i]
        ConfigManager.set('mea_style', para)