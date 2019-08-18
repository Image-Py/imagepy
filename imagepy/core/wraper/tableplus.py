import numpy as np
import pandas as pd
from ..manager import TableManager

class TablePlus():
    def __init__(self, data, title=None):
        self.set_title(title)
        self.dirty, self.range = None, None
        self.default = [3, (0,0,0), (0,0,255), 'Text']
        self.set_data(data)
        self.snap = None

    def update(self, value=True): self.dirty=value
    
    def set_title(self, title):
        self.title = TableManager.name(title)

    def get_nbytes(self):
        return self.data.memory_usage().sum()

    def get_str(self, row, col):
        ser = self.data[self.columns[col]]

    def set_data(self, data):
        self.data, self.props = data, None
        self.rowmsk, self.colmsk = [],[]
        self.count_range()

    def get_subtab(self, mskr=True, mskc=True, num=False):
        if mskr==None:rmsk = slice(None)
        rowmsk = self.rowmsk if len(self.rowmsk)>0 else self.data.index
        if mskr==True:rmsk = rowmsk
        if mskr==False:rmsk = self.data.index.difference(rowmsk)

        if mskc==None:cmsk = slice(None)
        colmsk = self.colmsk if len(self.colmsk)>0 else self.data.columns
        if mskc==True:cmsk = colmsk
        if mskc==False:cmsk = self.data.columns.difference(colmsk)

        subtab = self.data.loc[rmsk, cmsk]
        if num: subtab = subtab.select_dtypes(include=[np.number])
        return subtab

    def snapshot(self, mskr=None, mskc=None, num=False):
        self.snap = self.get_subtab(mskr, mskc, num).copy()

    def select(self, rs=[], cs=[], byidx=False):
        if byidx: rs, cs = self.data.index[rs], self.data.columns[cs]
        self.rowmsk = pd.Index(rs).astype(self.data.index.dtype)
        self.colmsk = pd.Index(cs).astype(self.data.columns.dtype)
        # print('tps select', rs, cs, self.rowmsk, self.colmsk)

    def get_titles(self):return self.data.columns

    def get_index(self):return self.data.index

    def get_props(self):
        props, data = self.props, self.data
        if self.props is None or len(props.columns)!=len(data.columns)\
            or (props.columns != data.columns).sum()>0:
            ndata = [[i]*data.shape[1] for i in self.default]
            newprop = pd.DataFrame(ndata, ['round', 'tc', 'lc', 'ln'], data.columns)
            if not self.props is None:
                inter = self.props.columns.intersection(newprop.columns)
                newprop[inter] = self.props[inter]
            self.props = newprop
        return self.props

    def count_range(self):
        self.range = pd.DataFrame([self.data.min(), self.data.max()])

    def __del__(self):
        print(self.title, '>>> deleted tps')