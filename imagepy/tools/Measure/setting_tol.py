from sciapp.action import ImageTool
from sciapp.action import Measure
from imagepy.core.engine import Free
from sciapp import Source

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
        Source.manager('config').add('mea_style', para)