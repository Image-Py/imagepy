from imagepy import IPy
import numpy as np
from imagepy.core.engine import Simple
from skimage.measure import regionprops
from imagepy.core.mark import GeometryMark
from scipy.ndimage import label, generate_binary_structure
from imagepy.ipyalg.graph.connect import connect, mapidx
import pandas as pd

# center, area, l, extent, cov
class Plugin(Simple):
    title = 'Connective Analysis'
    note = ['8-bit', '16-bit', 'int']
    para = {'con':'8-connect', 'labled':False, 'slice':False}
    view = [(list, 'con', ['4-connect', '8-connect'], str, 'conection', 'pix'),
            (bool, 'labled', 'it is a label image'),
            (bool, 'slice', 'slice')]

    #process
    def run(self, ips, imgs, para = None):
        if not para['slice']:imgs = [ips.img]
        k = ips.unit[0]

        titles = ['Slice', 'ID'][0 if para['slice'] else 1:] + ['Center-X','Center-Y', 'N', 'Neighbors']
        buf = imgs[0].astype(np.uint32)
        data, mark = [], {'type':'layers', 'body':{}}
        for i in range(len(imgs)):
            if para['labled']: buf = imgs[i]
            else: label(imgs[i], generate_binary_structure(2, 1), output=buf)
            conarr = connect(buf, 1 if para['con']=='4-connect' else 2)
            conmap = mapidx(conarr)

            ls = regionprops(buf)
            dt = [[i]*len(ls), list(range(1,1+len(ls)))]
            
            if not para['slice']:dt = dt[1:]

            layer = {'type':'layer', 'body':[]}
            texts = [(i.centroid[::-1])+('id=%d'%i.label,) for i in ls]
            lines = [(ls[i-1].centroid[::-1], ls[j-1].centroid[::-1]) for i,j in conarr]
            layer['body'].append({'type':'texts', 'body':texts})
            layer['body'].append({'type':'lines', 'body':lines})
            mark['body'][i] = layer

            dt.append([round(i.centroid[1]*k,1) for i in ls])
            dt.append([round(i.centroid[0]*k,1) for i in ls])
            neibs = [conmap[i.label] if i.label in conmap else [] for i in ls]
            dt.extend([[len(i) for i in neibs], neibs])
            data.extend(list(zip(*dt)))
        ips.mark = GeometryMark(mark)
        IPy.show_table(pd.DataFrame(data, columns=titles), ips.title+'-region')