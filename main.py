def run():
    import wx
    import os,sys
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    from imagepy3.ui.imagepy import ImagePy
    app = wx.App(False)
    mainFrame = ImagePy(None)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__"  :
    run()
