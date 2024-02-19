from sciapp.object import Table
from sciapp.action import TableTool
import wx, os
import wx.grid
import sys

import numpy as np
import pandas as pd
from ..widgets import get_para

class TableBase(wx.grid.GridTableBase):
    def __init__(self):
        wx.grid.GridTableBase.__init__(self)
        self.table = None

    def set_data(self, table):
        self.table = table
        self._rows, self._cols = table.shape

    def GetNumberCols(self):
        if self.table is None: return 0
        return self.table.shape[1]

    def GetNumberRows(self):
        if self.table is None: return 0
        return self.table.shape[0]

    def GetColLabelValue(self, col):
        return str(self.table.columns[col])

    def GetRowLabelValue(self, row):
        return str(self.table.index[row])

    def GetValue(self, row, col):
        return self.table.data.iat[row, col]

    def GetRawValue(self, row, col):
        return 'x'

    def SetValue(self, row, col, value):
        col = self.table.columns[col]
        self.table.data[col,row] = value

    def ResetView(self, grid):
        grid.BeginBatch()

        for current, new, delmsg, addmsg in [
            (self._rows, self.GetNumberRows(),
             wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
             wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED),
            (self._cols, self.GetNumberCols(),
             wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED,
             wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED)
        ]:

            if new < current:
                msg = wx.grid.GridTableMessage(self,delmsg,new,current-new)
                grid.ProcessTableMessage(msg)
            elif new > current:
                msg = wx.grid.GridTableMessage(self,addmsg,new-current)
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
        msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        grid.ProcessTableMessage(msg)

    def _updateColAttrs(self, grid):
        """
        wx.Grid -> update the column attributes to add the
        appropriate renderer given the column name.  (renderers
        are stored in the self.plugins dictionary)

        Otherwise default to the default renderer.
        """
        col = 0

        for colname in self.table.columns:
            attr = wx.grid.GridCellAttr()
            renderer = MegaFontRenderer(self.table)
            attr.SetRenderer(renderer)
            grid.SetColAttr(col, attr)
            col += 1

class MegaFontRenderer(wx.grid.GridCellRenderer):
    def __init__(self, table):
        wx.grid.GridCellRenderer.__init__(self)
        n_back = wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW )
        l_back = wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT )
        n_text = wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT )
        l_text = wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT )
        self.colors = [(n_back, n_text), (l_back, l_text)]
        #line = wx.Color((255,0,0))
        self.selectedBrush = wx.Brush("blue", wx.BRUSHSTYLE_SOLID)
        self.normalBrush = wx.Brush(wx.WHITE, wx.BRUSHSTYLE_SOLID)
        self.font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "ARIAL")
        self.table = table

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        dc.SetClippingRegion(rect)
        cn = self.table.columns[col]
        rd, tc, lc, ln = self.table.style[cn]
        bcolor, tcolor = self.colors[isSelected]
        if isSelected:tc = tcolor

        # clear the background
        dc.SetBackgroundMode(wx.SOLID)

        dc.SetBrush(wx.Brush(bcolor, wx.BRUSHSTYLE_SOLID))
        dc.SetPen(wx.Pen(bcolor, 1, wx.PENSTYLE_SOLID))
        dc.DrawRectangle(rect)

        isnum = np.issubdtype(self.table.data[cn].dtype, np.number)
        if ln!='Line':
            if isnum:
                text = str(round(self.table.data.iat[row, col], rd))
            else: text = str(self.table.data.iat[row, col])
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
            data = self.table.data
            cn = data.columns[col]
            rn = data.index[row]
            minv, maxv = self.table.rg[cn]
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

class Grid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        self.tablebase = TableBase()
        self.table = Table()
        self.tool = None

        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.on_select)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.on_label)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_cell)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_cell)
        self.Bind(wx.EVT_IDLE, self.on_idle)

    def on_label(self, evt):
        row, col = evt.GetRow(), evt.GetCol()
        if row==-1:
            props = self.table.props
            
            cur = props[self.table.columns[col]]
            print(cur)
            para = {'accu':cur[0], 'tc':cur[1], 'lc':cur[2], 'ln':cur[3]}
            view = [(int, 'accu', (0, 10), 0, 'accuracy', ''),
                    ('color', 'tc', 'text color', ''),
                    ('color', 'lc', 'line color', ''),
                    (list, 'ln', ['Text', 'Line', 'Both'], str, 'draw', '')]
            rst = get_para(para, view, 'Table Properties', self)
            if not rst :return
            print(para)
            if col!=-1:
                props[self.table.columns[col]] = [para[i] for i in ['accu', 'tc', 'lc', 'ln']]
                #print(props[self.table.columns[col]])
                #print('===========')
            if col==-1:
                for c in self.table.columns:
                    props[c] = [para[i] for i in ['accu', 'tc', 'lc', 'ln']]
        self.update()

    def on_cell(self, me):
        x, y = me.GetCol(), me.GetRow()
        obj, tol = self.table, TableTool.default
        tool = self.tool or tol
        #ld, rd, md = me.LeftIsDown(), me.RightIsDown(), me.MiddleIsDown()
        sta = [me.AltDown(), me.ControlDown(), me.ShiftDown()]
        others = {'alt':sta[0], 'ctrl':sta[1],
            'shift':sta[2], 'grid':self}
        tool.mouse_down(self.table, x, y, 0, **others)
        me.Skip()

    def set_data(self, tab):
        if isinstance(tab, Table):
            self.table = tab
        else: self.table.data = tab
        self.tablebase.set_data(self.table)
        self._rows, self._cols = tab.shape
        self.SetTable(self.tablebase)
        self.update()

    def set_style(self, name, **key):
        self.table.set_style(name, **key)
        self.update()

    def on_select(self, event):
        rs, cs = self.GetSelectedRows(), self.GetSelectedCols()
        lt, rb = self.GetSelectionBlockTopLeft(), self.GetSelectionBlockBottomRight()
        if len(lt)==1 and len(rb)==1: 
            return self.table.select(range(lt[0][0],rb[0][0]+1), range(lt[0][1],rb[0][1]+1))
        else: self.table.select(list(rs), list(cs), True)

    def update(self):
        self.tablebase.ResetView(self)

    def select(self):
        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, None)
        self.ClearSelection()
        for i in self.table.index.get_indexer(self.table.rowmsk):
            self.SelectRow(i, True)
        for i in self.table.columns.get_indexer(self.table.colmsk):
            self.SelectCol(i, True)
        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.on_select)

    def on_idle(self, event):
        if not self.IsShown() or self.table is None\
            or self.table.dirty == False: return
        
        self.tablebase.ResetView(self)
        self.table.dirty = False
        # self.select()
        print('update')

    def __del__(self):
        print('grid deleted!!!')


if __name__ == '__main__':
    dates = pd.date_range('20170220',periods=6)
    df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))

    app = wx.App(False)

    frame = wx.Frame(None)
    grid = Grid(frame)
    grid.set_data(df)
    frame.Show()
    app.MainLoop()
