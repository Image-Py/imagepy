#!/usr/bin/env python

import wx, os
import wx.grid as Grid
import sys

from imagepy import IPy, root_dir
import numpy as np
import pandas as pd
from imagepy.core.manager import TableManager, WTableManager

class TableBase(Grid.GridTableBase):
    """
    A custom wx.Grid Table using user supplied data
    """
    def __init__(self):
        Grid.GridTableBase.__init__(self)
        self.tps = None

    def set_tps(self, tps):
        self.tps = tps
        self._rows = tps.data.shape[0]
        self._cols = tps.data.shape[1]

    def GetNumberCols(self):
        if self.tps is None: return 0
        return self.tps.data.shape[1]

    def GetNumberRows(self):
        if self.tps is None: return 0
        return self.tps.data.shape[0]

    def GetColLabelValue(self, col):
        return str(self.tps.data.columns[col])

    def GetRowLabelValue(self, row):
        return str(self.tps.data.index[row])

    def GetValue(self, row, col):
        return self.tps.data.iat[row, col]

    def GetRawValue(self, row, col):
        return 'x'

    def SetValue(self, row, col, value):
        col = self.tps.data.columns[col]
        self.tps.data[col][row] = value

    def ResetView(self, grid):
        grid.BeginBatch()

        for current, new, delmsg, addmsg in [
            (self._rows, self.GetNumberRows(), Grid.GRIDTABLE_NOTIFY_ROWS_DELETED, Grid.GRIDTABLE_NOTIFY_ROWS_APPENDED),
            (self._cols, self.GetNumberCols(), Grid.GRIDTABLE_NOTIFY_COLS_DELETED, Grid.GRIDTABLE_NOTIFY_COLS_APPENDED),
        ]:

            if new < current:
                msg = Grid.GridTableMessage(self,delmsg,new,current-new)
                grid.ProcessTableMessage(msg)
            elif new > current:
                msg = Grid.GridTableMessage(self,addmsg,new-current)
                grid.ProcessTableMessage(msg)
                self.UpdateValues(grid)

        grid.EndBatch()

        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()
        # update the column rendering plugins
        self._updateColAttrs(grid)

        # update the scrollbars and the displayed part of the grid
        grid.AdjustScrollbars()
        grid.ForceRefresh()


    def UpdateValues(self, grid):
        """Update all displayed values"""
        # This sends an event to the grid table to update all of the values
        msg = Grid.GridTableMessage(self, Grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        grid.ProcessTableMessage(msg)

    def _updateColAttrs(self, grid):
        """
        wx.Grid -> update the column attributes to add the
        appropriate renderer given the column name.  (renderers
        are stored in the self.plugins dictionary)

        Otherwise default to the default renderer.
        """
        col = 0

        for colname in self.tps.data.columns:
            attr = Grid.GridCellAttr()
            renderer = MegaFontRenderer(self.tps)
            attr.SetRenderer(renderer)
            grid.SetColAttr(col, attr)
            col += 1



    # end table manipulation code
    # ----------------------------------------------------------


# --------------------------------------------------------------------
# Sample wx.Grid renderers



class MegaFontRenderer(Grid.GridCellRenderer):
    def __init__(self, tps):
        Grid.GridCellRenderer.__init__(self)
        n_back = wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW )
        l_back = wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT )
        n_text = wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT )
        l_text = wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT )
        self.colors = [(n_back, n_text), (l_back, l_text)]
        #line = wx.Color((255,0,0))
        self.selectedBrush = wx.Brush("blue", wx.BRUSHSTYLE_SOLID)
        self.normalBrush = wx.Brush(wx.WHITE, wx.BRUSHSTYLE_SOLID)
        self.font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "ARIAL")
        self.tps = tps

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        dc.SetClippingRegion(rect)
        cn = self.tps.data.columns[col]
        rd, tc, lc, ln = self.tps.get_props()[cn]
        bcolor, tcolor = self.colors[isSelected]
        if isSelected:tc = tcolor

        # clear the background
        dc.SetBackgroundMode(wx.SOLID)

        dc.SetBrush(wx.Brush(bcolor, wx.BRUSHSTYLE_SOLID))
        dc.SetPen(wx.Pen(bcolor, 1, wx.PENSTYLE_SOLID))
        dc.DrawRectangle(rect)

        isnum = np.issubdtype(self.tps.data[cn].dtype, np.number)
        if ln!='Line':
            if isnum:
                text = str(round(self.tps.data.iat[row, col], rd))
            else: text = str(self.tps.data.iat[row, col])
            dc.SetBackgroundMode(wx.SOLID)

            # change the text background based on whether the grid is selected
            dc.SetBrush(wx.Brush(wx.Colour(tc), wx.BRUSHSTYLE_SOLID))
            dc.SetTextBackground(bcolor)


            dc.SetTextForeground(wx.Colour(tc))
            dc.SetFont(self.font)
            dc.DrawText(text, rect.x+1, rect.y+1)


            width, height = dc.GetTextExtent(text)
            if width > rect.width-2:
                width, height = dc.GetTextExtent("...")
                x = rect.x+1 + rect.width-2 - width
                dc.DrawRectangle(x, rect.y+1, width+1, height)
                dc.DrawText("...", x, rect.y+1)

        if isnum and ln!='Text':
            data = self.tps.data
            cn = data.columns[col]
            rn = data.index[row]
            minv, maxv = self.tps.range[cn]
            dc.SetPen(wx.Pen(wx.Colour(lc), 1, wx.PENSTYLE_SOLID))
            dc.SetBrush(wx.Brush(wx.Colour(lc), wx.BRUSHSTYLE_SOLID))
            v = rect.x + (data[cn][rn]-minv)/(maxv-minv)*rect.width
            dc.DrawCircle(v, rect.y+rect.height/2, 2)
            if row>0:
                v1 = rect.x + (data[cn][data.index[row-1]] - minv)/(maxv-minv)*rect.width
                dc.DrawLine(v1, rect.y-rect.height/2, v, rect.y+rect.height/2)
            if row<data.shape[0]-1:
                v2 = rect.x + (data[cn][data.index[row+1]] - minv)/(maxv-minv)*rect.width
                dc.DrawLine(v, rect.y+rect.height/2, v2, rect.y+rect.height/2*3)

        dc.DestroyClippingRegion()

# --------------------------------------------------------------------
# Sample Grid using a specialized table and renderers that can
# be plugged in based on column names

class GridBase(Grid.Grid):
    def __init__(self, parent):
        Grid.Grid.__init__(self, parent, -1)
        self.table = TableBase()
        self.Bind(Grid.EVT_GRID_RANGE_SELECT, self.on_select)
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.tps = None
        self.handle = None
        self.Bind(Grid.EVT_GRID_LABEL_RIGHT_CLICK, self.on_label)

    def on_label(self, evt):
        # Did we click on a row or a column?
        row, col = evt.GetRow(), evt.GetCol()
        if row==-1:
            props = self.tps.props
            
            cur = props.iloc[:,col]
            para = {'accu':cur[0], 'tc':cur[1], 'lc':cur[2], 'ln':cur[3]}
            view = [(int, 'accu', (0, 10), 0, 'accuracy', ''),
                    ('color', 'tc', 'text color', ''),
                    ('color', 'lc', 'line color', ''),
                    (list, 'ln', ['Text', 'Line', 'Both'], str, 'draw', '')]
            rst = IPy.get_para('Table Properties', view, para)
            if not rst :return
            if col!=-1:
                props.iloc[:,col] = [para[i] for i in ['accu', 'tc', 'lc', 'ln']]
            if col==-1:
                for c in range(props.shape[1]):
                    props.iloc[:,c] = [para[i] for i in ['accu', 'tc', 'lc', 'ln']]
        '''
        if row==-1 and col>-1:
            props.ix['ln',col] = (props.ix['ln',col]+1)%3
        if row==-1 and col==-1:
            cn = self.tps.data.columns[col]
            props.ix['ln'] = (props.ix['ln'].min()+1)%3
        '''
        self.tps.update()


    def set_handler(self, handle=None):
        self.handle = handle

    def set_tps(self, tps):
        self.tps = tps
        self.table.set_tps(tps)
        self._rows, self._cols = tps.data.shape
        self.SetTable(self.table)
        self.Reset()

    def on_select(self, event):
        rs, cs = self.GetSelectedRows(), self.GetSelectedCols()
        lt, rb = self.GetSelectionBlockTopLeft(), self.GetSelectionBlockBottomRight()
        if len(lt)==1 and len(rb)==1: 
            return self.tps.select(range(lt[0][0],rb[0][0]+1), range(lt[0][1],rb[0][1]+1))
        else: self.tps.select(rs, cs, True)
        #self.tps.select()

    def Reset(self):
        """reset the view based on the data in the table.  Call
        this when rows are added or destroyed"""
        self.table.ResetView(self)
        if not self.handle is None:
            self.handle(self.tps)

    def select(self):
        self.Bind(Grid.EVT_GRID_RANGE_SELECT, None)
        self.ClearSelection()
        for i in self.tps.data.index.get_indexer(self.tps.rowmsk):
            self.SelectRow(i, True)
        for i in self.tps.data.columns.get_indexer(self.tps.colmsk):
            self.SelectCol(i, True)
        self.Bind(Grid.EVT_GRID_RANGE_SELECT, self.on_select)

    def __del__(self):
        print('grid deleted!!!')

    def on_idle(self, event):
        if not self.IsShown() or self.tps is None\
            or self.tps.dirty == False: return
        if self.tps.dirty == 'shp':
            self.select()
            self.Reset()
        if self.tps.dirty == True:
            self.select()
            self.ForceRefresh()
        self.tps.dirty = False
        print('update')


#---------------------------------------------------------------------------



if __name__ == '__main__':
    dates = pd.date_range('20170220',periods=6)
    data = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))

    app = wx.App(False)

    tf = TableFrame()
    from imagepy import TablePlus
    tps = TablePlus('table1', data)
    tf.set_tps(tps)
    tf.Show()

    app.MainLoop()
