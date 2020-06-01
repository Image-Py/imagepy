import wx, sys
sys.path.append('../../')

import numpy as np
from sciwx.plot import PlotCanvas, PlotFrame, PlotNoteBook, PlotNoteFrame

x = np.linspace(0, 10, 100)
y = np.sin(x)

def plot_canvas_test():
    frame = wx.Frame(None, title='PlotCanvas')
    pcanvas = PlotCanvas(frame)
    ax = pcanvas.add_subplot()
    ax.plot(x, y)
    frame.Show()

def plot_frame_test():
    pframe = PlotFrame(None)
    ax = pframe.add_subplot()
    ax.plot(x, y)
    pframe.Show()

def plot_note_book():
    frame = wx.Frame(None)
    pnb = PlotNoteBook(frame)
    figure1 = pnb.add_figure()
    ax = figure1.add_subplot()
    ax.plot(x, y)
    figure2 = pnb.add_figure()
    ax = figure2.add_subplot()
    ax.plot(x, y, 'r-.')
    frame.Show()

def plot_note_frame():
    pnf = PlotNoteFrame(None)
    figure1 = pnf.add_figure()
    ax = figure1.add_subplot()
    ax.plot(x, y)
    ax.grid()
    ax.set_title('abc')
    figure2 = pnf.add_figure()
    ax = figure2.add_subplot()
    ax.plot(x, y)
    pnf.Show()

if __name__ == '__main__':
    app = wx.App()
    plot_canvas_test()
    plot_frame_test()
    plot_note_book()
    plot_note_frame()
    app.MainLoop()
