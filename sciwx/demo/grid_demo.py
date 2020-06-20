import sys, wx
sys.path.append('../../')
import pandas as pd
import numpy as np

from sciwx.grid import Grid
from sciapp.object import Table
from sciwx.grid import GridFrame, GridNoteBook, GridNoteFrame

def grid_test():
    df = pd.DataFrame(np.random.randn(100,5))
    frame = wx.Frame(None, title='Grid')
    grid = Grid(frame)
    grid.set_data(df)
    frame.Show()

def grid_style_test():
    df = pd.DataFrame(np.random.randn(100,5))
    frame = wx.Frame(None, title='Grid')
    grid = Grid(frame)
    grid.set_data(df)
    grid.set_style(1, tc=(255,0,0), round=5)
    grid.set_style(2, lc=(255,0,255), ln='both')
    frame.Show()
    
def grid_frame_test():
    df = pd.DataFrame(np.random.randn(100,5))
    cf = GridFrame(None)
    cf.set_data(df)
    cf.Show()

def grid_note_book():
    df = pd.DataFrame(np.random.randn(100,5))
    frame = wx.Frame(None, title='GridNoteBook')
    gnb = GridNoteBook(frame)
    grid1 = gnb.add_grid()
    grid1.set_data(df)
    grid2 = gnb.add_grid()
    grid2.set_data(df)
    frame.Show()

def grid_note_frame():
    df = pd.DataFrame(np.random.randn(6,4))
    gnf = GridNoteFrame(None)
    grid1 = gnf.add_grid()
    grid1.set_data(df)
    grid2 = gnf.add_grid()
    grid2.set_data(df)
    gnf.Show()

def table_obj_test():
    df = pd.DataFrame(np.random.randn(100,5))
    table = Table()
    table.data = df
    table.name = 'Table Object'
    table.set_style(1, tc=(255,0,0), round=5)
    table.set_style(2, lc=(255,0,255), ln='both')
    cf = GridFrame(None)
    cf.set_data(table)
    cf.Show()
    
if __name__=='__main__':
    app = wx.App()
    grid_test()
    grid_style_test()
    grid_frame_test()
    grid_note_book()
    grid_note_frame()
    table_obj_test()
    app.MainLoop()
