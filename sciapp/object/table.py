import numpy as np

class Table():
    def __init__(self, df=None, name='Table'):
        self.name = name
        self.df = df
        self.rg = None
        self.props = None
        self.snap = None
        self.dirty = False
        if not df is None:
            self.data = df
        
    @property
    def title(self): return self.name

    @property
    def nbytes(self):
        return self.data.memory_usage().sum()

    @property
    def columns(self):return self.data.columns

    @property
    def index(self):return self.data.index

    @property
    def shape(self): return self.data.shape

    @property
    def data(self): return self.df
    
    def update(self): self.dirty = True

    @data.setter
    def data(self, df):
        self.df, self.props = df, None
        self.rowmsk, self.colmsk = [], []
        self.count_range()

    @property
    def style(self):
        props, data = self.props, self.data
        if props is None or set(props)!=set(data.columns):
            ps = [[3, (0,0,0), (0,0,255), 'Text'] for i in data.columns]
            self.props = dict(zip(data.columns, ps))
        return self.props

    def subtab(self, mode=True, num=False):
        rs, cs = len(self.rowmsk), len(self.colmsk)
        mskr = slice(None) if rs==0 else self.rowmsk
        mskc = slice(None) if cs==0 else self.colmsk
        if mode is None: mskr = mskc = slice(None)
        mskr, mskc = self.data.index[mskr], self.data.columns[mskc]
        if mode is False and rs>0: mskr = self.data.index.difference(mskr)
        if mode is False and cs>0: mskc = self.data.columns.difference(mskc)
        subtab = self.data.loc[mskr, mskc]
        if num: subtab = subtab.select_dtypes(include=[np.number])
        return subtab

    def snapshot(self, mode=True, num=False):
        self.snap = self.subtab(mode, num).copy()

    def set_style(self, col, **key):
        for i, name in enumerate(['accu', 'tc', 'lc', 'ln']):
            if name in key: self.style[col][i] = key[name]

    def count_range(self):
        rg = list(zip(self.data.min(), self.data.max()))
        self.rg = dict(zip(self.data.columns, rg))

    def select(self, rs=[], cs=[], byidx=False):
        if byidx: rs, cs = self.df.index[rs], self.df.columns[cs]
        self.rowmsk, self.colmsk = rs, cs

    @property
    def info(self):
        return '%sx%s %.2fM'%(*self.shape, self.nbytes/1024/1024)
        
if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    df = pd.DataFrame(np.zeros((10,5)), columns=list('abcde'))
    table = Table(df)
    
