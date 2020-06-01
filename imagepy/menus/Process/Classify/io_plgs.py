from imagepy.core.engine import Filter, Simple
from sciapp import Source
# from imagepy.core import ImagePlus
import numpy as np

class BuildMark(Simple):
    """Closing: derived from imagepy.core.engine.Filter """
    title = 'Build Mark Image'
    note = ['all']
    para = {'mode':'Mask', 'cm':'16_Colors', 'n':2, 'slice':True}
    view = [(int, 'n', (0, 15), 0, 'n', 'colors'),
    		('cmap', 'cm', 'colormap'),
    		(list, 'mode', ['None', 'Max', 'Min', 'Mask', '2-8mix', \
    		'4-6mix', '5-5mix', '6-4mix', '8-2mix'], str, 'mode', 'channel'),
    		(bool, 'slice', 'slice')]

    def run(self, ips, imgs, para = None):
        shp = ips.img.shape[:2]
        imgs = [np.zeros(shp, dtype=np.uint8) for i in range([1, len(imgs)][para['slice']])]
        newips = ImagePlus(imgs, ips.title+'-mark')
        newips.back = ips
        idx = ['None', 'Max', 'Min', 'Mask', '2-8mix', '4-6mix', '5-5mix', '6-4mix', '8-2mix']
        modes = ['set', 'max', 'min', 'msk', 0.2, 0.4, 0.5, 0.6, 0.8]
        newips.lut = Source.manager('colormap').get(para['cm'])
        newips.chan_mode = modes[idx.index(para['mode'])]
        #newips.range = (0, para['n'])
        IPy.show_ips(newips)

plgs = [BuildMark]