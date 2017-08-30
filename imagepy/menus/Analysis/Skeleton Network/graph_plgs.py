from imagepy.core.engine import Filter
from imagepy.ipyalg.graph import sknw

class Graph(Filter):
    title = 'build graph'
    note = ['8-bit', 'not_slice', 'not_channel']

    #process
    def run(self, ips, snap, img, para = None):
        ips.data = sknw.build_sknw(img)
        img[:] = img * 120 

plgs = [Graph]