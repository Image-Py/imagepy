import numpy as np
from sciapp.action import Simple
from skimage.feature import blob_dog, blob_doh, blob_log
from sciapp.object import mark2shp
import pandas as pd

class Dog(Simple):
    title = 'Blob Dog'
    note = ['all', 'preview']
    para = {'min_sigma':1, 'max_sigma':50, 'sigma_ratio':1.6, 'threshold':0.1, 
            'overlap':0.5, 'exclude_border':False, 'showid':True, 'slice':False}

    view = [(int, 'min_sigma', (1, 50), 0, 'min', 'sigma'),
            (int, 'max_sigma', (1, 50), 0, 'max', 'sigma'),
            (float, 'sigma_ratio', (1.3, 5), 1, 'ratio', '1.3~5'),
            (float, 'threshold', (0.01, 10), 2, 'threshold', '0.01~10'),
            (float, 'overlap', (0, 10), 1, 'overlap', ''),
            (bool, 'exclude_border', 'exclude border'),
            (bool, 'showid', 'show id on image'),
            (bool, 'slice', 'slice')]

    def preview(self, ips, para):
        grayimg = ips.img if ips.img.ndim==2 else ips.img.mean(axis=-1)
        grayimg /= grayimg.max()
        pts = blob_dog(grayimg,  min_sigma=para['min_sigma'], max_sigma=para['max_sigma'], 
            sigma_ratio=para['sigma_ratio'], threshold=para['threshold'], 
            overlap=para['overlap'], exclude_border=para['exclude_border'])
        pts[:,2] *= np.sqrt(2)
        ips.mark = mark2shp({'type':'circles', 'body':pts[:,[1,0,2]]})

    def cancel(self, ips): ips.mark = None

    def run(self, ips, imgs, para = None):
        if not para['slice']:imgs = [ips.img]

        data, sid, fid, mark = [], [], [], {'type':'layers', 'body':{}}

        for i in range(len(imgs)):
            grayimg = imgs[i] if imgs[i].ndim==2 else imgs[i].mean(axis=-1)
            grayimg /= grayimg.max()
            pts = blob_dog(grayimg,  min_sigma=para['min_sigma'], max_sigma=para['max_sigma'], 
                sigma_ratio=para['sigma_ratio'], threshold=para['threshold'], 
                overlap=para['overlap'], exclude_border=para['exclude_border'])
            pts[:,2] *= np.sqrt(2)
            sid.extend([i]*len(pts))
            fid.extend(range(1, len(pts)+1))
            data.append(pts)

            layer = {'type':'layer', 'body':[{'type':'circles', 'body':pts[:,[1,0,2]]}]}
            if para['showid']:
                layer['body'].append({'type':'texts', 'body':[
                    (x,y,'id=%d'%i) for (x,y),i in zip(pts[:,1::-1], fid)]})
            mark['body'][i] = layer

        ips.mark = mark2shp(mark)
        df = pd.DataFrame(np.vstack(data)*ips.unit[0], columns = ['X', 'Y', 'R'])
        df.insert(0, 'FID', fid)
        if para['slice']: df.insert(o, 'SliceID', sid)
        self.app.show_table(df, ips.title+'-dogblob')

class Doh(Simple):
    title = 'Blob Doh'
    note = ['all', 'preview']
    para = {'min_sigma':1, 'max_sigma':30, 'num_sigma':10, 'threshold':0.01, 
            'overlap':0.5, 'log_scale':False, 'showid':True, 'slice':False}

    view = [(int, 'min_sigma', (1, 50), 0, 'min', 'sigma'),
            (int, 'max_sigma', (1, 50), 0, 'max', 'sigma'),
            (int, 'num_sigma', (5, 30), 0, 'num', 'sigma'),
            (float, 'threshold', (0.01, 1), 2, 'threshold', '0.01~10'),
            (float, 'overlap', (0, 10), 1, 'overlap', ''),
            (bool, 'log_scale', 'log scale'),
            (bool, 'showid', 'show id on image'),
            (bool, 'slice', 'slice')]

    def preview(self, ips, para):
        grayimg = ips.img if ips.img.ndim==2 else ips.img.mean(axis=-1)
        grayimg /= grayimg.max()
        pts = blob_doh(grayimg,  min_sigma=para['min_sigma'], max_sigma=para['max_sigma'], 
            num_sigma=para['num_sigma'], threshold=para['threshold'], 
            overlap=para['overlap'], log_scale=para['log_scale'])
        ips.mark = mark2shp({'type':'circles', 'body':pts[:,[1,0,2]]})

    def cancel(self, ips): ips.mark = None

    def run(self, ips, imgs, para = None):
        if not para['slice']:imgs = [ips.img]

        data, sid, fid, mark = [], [], [], {'type':'layers', 'body':{}}

        for i in range(len(imgs)):
            grayimg = imgs[i] if imgs[i].ndim==2 else imgs[i].mean(axis=-1)
            grayimg /= grayimg.max()
            pts = blob_doh(grayimg,  min_sigma=para['min_sigma'], max_sigma=para['max_sigma'], 
                num_sigma=para['num_sigma'], threshold=para['threshold'], 
                overlap=para['overlap'], log_scale=para['log_scale'])

            sid.extend([i]*len(pts))
            fid.extend(range(1, len(pts)+1))
            data.append(pts)

            layer = {'type':'layer', 'body':[{'type':'circles', 'body':pts[:,[1,0,2]]}]}
            if para['showid']:
                layer['body'].append({'type':'texts', 'body':[
                    (x,y,'id=%d'%i) for (x,y),i in zip(pts[:,1::-1], fid)]})
            mark['body'][i] = layer

        ips.mark = mark2shp(mark)
        df = pd.DataFrame(np.vstack(data)*ips.unit[0], columns = ['X', 'Y', 'R'])
        df.insert(0, 'FID', fid)
        if para['slice']: df.insert(o, 'SliceID', sid)
        self.app.show_table(df, ips.title+'-dohblob')

class Log(Simple):
    title = 'Blob Log'
    note = ['all', 'preview']
    para = {'min_sigma':1, 'max_sigma':30, 'num_sigma':10, 'threshold':0.1, 'overlap':0.5, 
        'log_scale':False, 'showid':True, 'exclude_border':False, 'slice':False}

    view = [(int, 'min_sigma', (1, 50), 0, 'min', 'sigma'),
            (int, 'max_sigma', (1, 50), 0, 'max', 'sigma'),
            (int, 'num_sigma', (5, 30), 0, 'num', 'sigma'),
            (float, 'threshold', (0.02, 1), 2, 'threshold', '0.02~1'),
            (float, 'overlap', (0, 10), 1, 'overlap', ''),
            (bool, 'log_scale', 'log scale'),
            (bool, 'exclude_border', 'exclude border'),
            (bool, 'showid', 'show id on image'),
            (bool, 'slice', 'slice')]

    def preview(self, ips, para):
        grayimg = ips.img if ips.img.ndim==2 else ips.img.mean(axis=-1)
        grayimg /= grayimg.max()
        pts = blob_log(grayimg,  min_sigma=para['min_sigma'], max_sigma=para['max_sigma'], 
            num_sigma=para['num_sigma'], threshold=para['threshold'], 
            overlap=para['overlap'], log_scale=para['log_scale'], exclude_border=para['exclude_border'])
        pts[:,2] *= np.sqrt(2)
        ips.mark = mark2shp({'type':'circles', 'body':pts[:,[1,0,2]]})

    def cancel(self, ips): ips.mark = None

    def run(self, ips, imgs, para = None):
        if not para['slice']:imgs = [ips.img]

        data, sid, fid, mark = [], [], [], {'type':'layers', 'body':{}}

        for i in range(len(imgs)):
            grayimg = imgs[i] if imgs[i].ndim==2 else imgs[i].mean(axis=-1)
            grayimg /= grayimg.max()
            pts = blob_log(grayimg,  min_sigma=para['min_sigma'], max_sigma=para['max_sigma'], 
                num_sigma=para['num_sigma'], threshold=para['threshold'], 
                overlap=para['overlap'], log_scale=para['log_scale'], exclude_border=para['exclude_border'])
            pts[:,2] *= np.sqrt(2)
            sid.extend([i]*len(pts))
            fid.extend(range(1, len(pts)+1))
            data.append(pts)

            layer = {'type':'layer', 'body':[{'type':'circles', 'body':pts[:,[1,0,2]]}]}
            if para['showid']:
                layer['body'].append({'type':'texts', 'body':[
                    (x,y,'id=%d'%i) for (x,y),i in zip(pts[:,1::-1], fid)]})
            mark['body'][i] = layer

        ips.mark = mark2shp(mark)
        df = pd.DataFrame(np.vstack(data)*ips.unit[0], columns = ['X', 'Y', 'R'])
        df.insert(0, 'FID', fid)
        if para['slice']: df.insert(o, 'SliceID', sid)
        self.app.show_table(df, ips.title+'-dohblob')

plgs = [Dog, Doh, Log]