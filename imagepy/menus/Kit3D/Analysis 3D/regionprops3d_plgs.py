from imagepy import IPy
import numpy as np
from imagepy.core.engine import Simple, Filter
from scipy.ndimage import label, generate_binary_structure
from skimage.measure import regionprops
from numpy.linalg import norm

# center, area, l, extent, cov
class RegionCounter(Simple):
    title = 'Geometry Analysis 3D'
    note = ['8-bit', '16-bit', 'stack3d']

    para = {'con':'8-connect', 'center':True, 'extent':False, 'vol':True,
            'ed':False, 'holes':False, 'fa':False}

    view = [(list, ['4-connect', '8-connect'], str, 'conection', 'con', 'pix'),
            ('lab','=========  indecate  ========='),
            (bool, 'center', 'center'),
            (bool, 'volume', 'vol'),
            (bool, 'extent', 'extent'),
            (bool, 'equivalent diameter', 'ed')]

    #process
    def run(self, ips, imgs, para = None):
        k = ips.unit[0]

        titles = ['ID']
        if para['center']:titles.extend(['Center-X','Center-Y','Center-Z'])
        if para['vol']:titles.append('Volume')
        if para['extent']:titles.extend(['Min-Z','Min-Y','Min-X','Max-Z','Max-Y','Max-X'])
        if para['ed']:titles.extend(['Diameter'])
        if para['fa']:titles.extend(['FilledArea'])

        buf = imgs.astype(np.uint16)
        strc = generate_binary_structure(3, 1 if para['con']=='4-connect' else 2)
        label(imgs, strc, output=buf)
        ls = regionprops(buf)

        dt = [range(len(ls))]

        centroids = [i.centroid for i in ls]
        if para['center']:
            dt.append([round(i.centroid[1]*k,1) for i in ls])
            dt.append([round(i.centroid[0]*k,1) for i in ls])
            dt.append([round(i.centroid[2]*k,1) for i in ls])
        if para['vol']:
            dt.append([i.area*k**3 for i in ls])
        if para['extent']:
            for j in (0,1,2,3,4,5):
                dt.append([i.bbox[j]*k for i in ls])
        if para['ed']:
            dt.append([round(i.equivalent_diameter*k, 1) for i in ls])
        if para['fa']:
            dt.append([i.filled_area*k**3 for i in ls])
        IPy.table(ips.title+'-region', list(zip(*dt)), titles)

# center, area, l, extent, cov
class RegionFilter(Simple):
    title = 'Geometry Filter 3D'
    note = ['8-bit', '16-bit', 'stack3d']
    para = {'con':'4-connect', 'inv':False, 'vol':0, 'dia':0, 'front':255, 'back':100}
    view = [(list, ['4-connect', '8-connect'], str, 'conection', 'con', 'pix'),
            (bool, 'invert', 'inv'),
            ('lab','Filter: "+" means >=, "-" means <'),
            (int, (0, 255), 0, 'front color', 'front', ''),
            (int, (0, 255), 0, 'back color', 'back', ''),
            (float, (-1e6, 1e6), 1, 'volume', 'vol', 'unit^3'),
            (float, (-1e6, 1e6), 1, 'diagonal', 'dia', 'unit')]

    #process
    def run(self, ips, imgs, para = None):
        k, unit = ips.unit
        strc = generate_binary_structure(3, 1 if para['con']=='4-connect' else 2)

        lab, n = label(imgs==0 if para['inv'] else imgs, strc, output=np.uint16)
        idx = (np.ones(n+1)*(0 if para['inv'] else para['front'])).astype(np.uint8)
        ls = regionprops(lab)

        for i in ls:
            if para['vol'] == 0: break
            if para['vol']>0:
                if i.area*k**3 < para['vol']: idx[i.label] = para['back']
            if para['vol']<0:
                if i.area*k**3 >= -para['vol']: idx[i.label] = para['back']

        for i in ls:
            if para['dia'] == 0: break
            d = norm(np.array(i.bbox[:3]) - np.array(i.bbox[3:]))
            if para['dia']>0:
                if d*k < para['dia']: idx[i.label] = para['back']
            if para['dia']<0:
                if d*k >= -para['dia']: idx[i.label] = para['back']

        idx[0] = para['front'] if para['inv'] else 0
        imgs[:] = idx[lab]

plgs = [RegionCounter, RegionFilter]