import numpy as np
from sciapp.action import Simple, Filter
from scipy.ndimage import label, generate_binary_structure
from skimage.measure import marching_cubes_lewiner, mesh_surface_area
from skimage.segmentation import find_boundaries
from skimage.measure import regionprops
from numpy.linalg import norm
import pandas as pd

class RegionLabel(Simple):
    title = 'Region Label 3D'
    note = ['8-bit', '16-bit', 'stack3d']

    para = {'con':'8-connect'}

    view = [(list, 'con', ['4-connect', '8-connect'], str, 'conection', 'pix')]

    #process
    def run(self, ips, imgs, para = None):
        buf = imgs.astype(np.int32)
        strc = generate_binary_structure(3, 1 if para['con']=='4-connect' else 2)
        label(imgs, strc, output=buf)
        IPy.show_img(buf, ips.title+'-label')

# center, area, l, extent, cov
class RegionCounter(Simple):
    title = 'Geometry Analysis 3D'
    note = ['8-bit', '16-bit', 'stack3d']

    para = {'con':'8-connect', 'center':True, 'extent':False, 'vol':True,
            'ed':False, 'holes':False, 'fa':False, 'cov':False, 'surf':True}

    view = [(list, 'con', ['4-connect', '8-connect'], str, 'conection', 'pix'),
            ('lab', None, '=========  indecate  ========='),
            (bool, 'center', 'center'),
            (bool, 'vol', 'volume'),
            (bool, 'surf', 'surface area'),
            (bool, 'extent', 'extent'),
            (bool, 'ed', 'equivalent diameter'),
            (bool, 'cov', 'eigen values')]

    #process
    def run(self, ips, imgs, para = None):
        k = ips.unit[0]

        titles = ['ID']
        if para['center']:titles.extend(['Center-X','Center-Y','Center-Z'])
        if para['surf']:titles.append('Surface')
        if para['vol']:titles.append('Volume')
        if para['extent']:titles.extend(['Min-Z','Min-Y','Min-X','Max-Z','Max-Y','Max-X'])
        if para['ed']:titles.extend(['Diameter'])
        if para['fa']:titles.extend(['FilledArea'])
        if para['cov']:titles.extend(['Axis1', 'Axis2', 'Axis3'])

        strc = generate_binary_structure(3, 1 if para['con']=='4-connect' else 2)
        buf, n = label(imgs, strc, output=np.uint32)
        ls = regionprops(buf)

        dt = [range(len(ls))]

        centroids = [i.centroid for i in ls]
        if para['center']:
            dt.append([round(i.centroid[1]*k,1) for i in ls])
            dt.append([round(i.centroid[0]*k,1) for i in ls])
            dt.append([round(i.centroid[2]*k,1) for i in ls])
        if para['surf']:
            buf[find_boundaries(buf, mode='outer')] = 0
            vts, fs, ns, cs = marching_cubes_lewiner(buf, level=0)
            lst = [[] for i in range(n+1)]
            for i in fs: lst[int(cs[i[0]])].append(i)
            dt.append([0 if len(i)==0 else mesh_surface_area(vts, np.array(i))*k**2 for i in lst][1:])
        if para['vol']:
            dt.append([i.area*k**3 for i in ls])
        if para['extent']:
            for j in (0,1,2,3,4,5):
                dt.append([i.bbox[j]*k for i in ls])
        if para['ed']:
            dt.append([round(i.equivalent_diameter*k, 1) for i in ls])
        if para['fa']:
            dt.append([i.filled_area*k**3 for i in ls])
        if para['cov']:
            ites = np.array([i.inertia_tensor_eigvals for i in ls])
            rst = np.sqrt(np.clip(ites.sum(axis=1)//2-ites.T, 0, 1e10)) * 4
            for i in rst[::-1]: dt.append(np.abs(i))
        self.app.show_table(pd.DataFrame(list(zip(*dt)), columns=titles), ips.title+'-region')

# center, area, l, extent, cov
class RegionFilter(Simple):
    title = 'Geometry Filter 3D'
    note = ['8-bit', '16-bit', 'stack3d']
    para = {'con':'4-connect', 'inv':False, 'vol':0, 'dia':0, 'front':255, 'back':100}
    view = [(list, 'con', ['4-connect', '8-connect'], str, 'conection', 'pix'),
            (bool, 'inv', 'invert'),
            ('lab', None, 'Filter: "+" means >=, "-" means <'),
            (int, 'front', (0, 255), 0, 'front color', ''),
            (int, 'back', (0, 255), 0, 'back color', ''),
            (float, 'vol', (-1e6, 1e6), 1, 'volume', 'unit^3'),
            (float, 'dia', (-1e6, 1e6), 1, 'diagonal', 'unit')]

    #process
    def run(self, ips, imgs, para = None):
        k, unit = ips.unit
        strc = generate_binary_structure(3, 1 if para['con']=='4-connect' else 2)

        lab, n = label(imgs==0 if para['inv'] else imgs, strc, output=np.uint32)
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

plgs = [RegionLabel, RegionCounter, RegionFilter]