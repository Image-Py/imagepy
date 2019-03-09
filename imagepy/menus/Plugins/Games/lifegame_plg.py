import numpy as np
from imagepy import IPy
from imagepy.core import ImagePlus
from imagepy.core.engine import Free, Tool
from scipy.ndimage import label
from scipy.signal import convolve2d

def generate(scr, size):
    row, col = scr.shape
    arr = np.ones((row*(size)+1, col*(size)+1), dtype=np.uint8)
    xs, ys = np.where(arr[:-1,:-1])
    arr[xs, ys] = scr[xs//size, ys//size]
    arr[::size,:] = 2; arr[:,::size] = 2
    return np.array([128,255,0], dtype=np.uint8)[arr]

def getscr(arr, size): return arr[1::size, 1::size]//255

def run(scr):
    pad = np.pad(scr, 1, 'constant')
    core = np.array([[1,1,1],[1,9,1],[1,1,1]])
    cov = convolve2d(pad, core, 'valid')
    lut = [0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0]
    return np.array(lut, dtype=np.uint8)[cov.astype(np.uint8)]

class Painter(Tool):
    def __init__(self, size): self.size = size
    title = 'Life Painter'
        
    def mouse_down(self, ips, x, y, btn, **key):
        if btn == 1:
            r, c = int(y), int(x)
            if r<0 or r>ips.img.shape[0]: return
            if c<0 or c>ips.img.shape[1]: return
            if ips.img[r,c] == 0: return
            lab, n = label(ips.img>0)
            ips.img[lab==lab[r,c]] = (128,255)[ips.img[r,c]!=255]
            ips.update()
        if btn == 3:
            img = getscr(ips.img, self.size)
            for i in range(len(ips.imgs)):
                ips.imgs[i][:] = generate(img, self.size)
                img = run(img)
            IPy.alert('Complete!')

class Plugin(Free):
    title = 'Game Of Life'
    para = {'name':'Game01','width':15, 'height':15, 'size':30,'slice':30}
    view = [(str, 'name', 'name', ''),
            (int, 'width',  (1,2048), 0,  'width', 'pix'),
            (int, 'height', (1,2048), 0,  'height', 'pix'),
            (int, 'size', (10, 50), 0, 'size', ''),
            (int, 'slice',  (1,100), 0,  'slice', '')]

    #process
    def run(self, para = None):
        first = generate(np.zeros((para['height'], para['width'])), para['size'])
        imgs = [first.copy() for i in range(para['slice'])]
        ips = ImagePlus(imgs, para['name'])
        ips.tool = Painter(para['size'])
        IPy.show_ips(ips)