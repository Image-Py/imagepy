from sciapp.action import Simple
import pandas as pd

class GrayStatistic(Simple):
    title = 'Gray Points Statistic'
    note = ['8-bit', '16-bit', 'int', 'float', 'req_roi']
    para = {'lst':True, 'max':True, 'sum':True, 'mean':True,'max':False, 
        'min':False,'var':False,'std':False,'skew':False,'kurt':False}
    view = [(bool, 'lst', 'list point'),
            (bool, 'sum', 'sum'),
            (bool, 'mean', 'mean'),
            (bool, 'max', 'max'),
            (bool, 'min', 'min'),
            (bool, 'var', 'var'),
            (bool, 'std', 'std'),
            (bool, 'skew', 'skew'),
            (bool, 'kurt', 'kurt')]

    def load(self, ips):
        if ips.roi is None or ips.roi.roitype != 'point':
            self.app.alert('need a point roi')
            return False
        return True

    def run(self, ips, imgs, para = None):
        ls = []
        for x,y,z in ips.roi.body:
            x,y,z = int(x), int(y), int(z)
            v = imgs[z][y,x]
            ls.append([x,y,z,v])

        data = pd.DataFrame(ls, columns=[*'XYZV'])
        rst = {}
        
        if para['sum']:rst['sum']  = data[['V']].sum()
        if para['mean']:rst['mean'] = data[['V']].mean()
        if para['max']:rst['max'] = data[['V']].max()
        if para['min']:rst['min'] = data[['V']].min()
        if para['var']:rst['var'] =  data[['V']].var()
        if para['std']:rst['std'] =  data[['V']].std()
        if para['skew']:rst['skew'] = data[['V']].skew()
        if para['kurt']:rst['kurt'] = data[['V']].kurt()

        if para['lst']:
            self.app.show_table(data, ips.title+'-pts color')
        self.app.show_table(pd.DataFrame(rst), ips.title+'-pts color statistic')

class ColorStatistic(Simple):
    title = 'Color Points Statistic'
    note = ['rgb', 'req_roi']
    para = {'lst':True, 'max':True, 'sum':True, 'mean':True,'max':False, 
        'min':False,'var':False,'std':False,'skew':False,'kurt':False}
    view = [(bool, 'lst', 'list point'),
            (bool, 'sum', 'sum'),
            (bool, 'mean', 'mean'),
            (bool, 'max', 'max'),
            (bool, 'min', 'min'),
            (bool, 'var', 'var'),
            (bool, 'std', 'std'),
            (bool, 'skew', 'skew'),
            (bool, 'kurt', 'kurt')]

    def load(self, ips):
        if ips.roi is None or ips.roi.dtype != 'point':
            IPy.alert('need a point roi')
            return False
        return True

    def run(self, ips, imgs, para = None):
        ls = []
        for x,y,z in ips.roi.body:
            x,y,z = int(x), int(y), int(z)
            r,g,b = imgs[z][y,x]
            ls.append([x,y,z,r,g,b])

        data = pd.DataFrame(ls, columns=[*'XYZRGB'])
        rst = {}
        
        if para['sum']:rst['sum'] = data[[*'RGB']].sum()
        if para['mean']:rst['mean'] =data[[*'RGB']].mean()
        if para['max']:rst['max'] = data[[*'RGB']].max()
        if para['min']:rst['min'] = data[[*'RGB']].min()
        if para['var']:rst['var'] = data[[*'RGB']].var()
        if para['std']:rst['std'] = data[[*'RGB']].std()
        if para['skew']:rst['skew'] = data[[*'RGB']].skew()
        if para['kurt']:rst['kurt'] = data[[*'RGB']].kurt()

        if para['lst']:
            IPy.show_table(data, ips.title+'-pts color')
        IPy.show_table(pd.DataFrame(rst), ips.title+'-pts color statistic')

plgs = [GrayStatistic, ColorStatistic]