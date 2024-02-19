import sys, wx
sys.path.append('../../')

from sciwx.text import MDPad, MDNoteBook, MDFrame, MDNoteFrame

mdstr ='''## Markdown Test
### Title
1. paragraph 1
2. paragraph 2
'''

def md_pad_test():
    frame = wx.Frame(None, title='Text Pad')
    mdpad = MDPad(frame)
    mdpad.set_cont(mdstr)
    frame.Show()

def md_frame_test():
    mdframe = MDFrame(None)
    mdframe.set_cont(mdstr)
    mdframe.Show()

def md_note_book():
    frame = wx.Frame(None, title='Text Note Book')
    mnb = MDNoteBook(frame)
    md1 = mnb.add_page()
    md1.set_cont(mdstr)
    md2 = mnb.add_page()
    md2.set_cont(mdstr)
    frame.Show()
    
def md_note_frame():
    mnf = MDNoteFrame(None)
    md1 = mnf.add_page()
    md1.set_cont(mdstr)
    md2 = mnf.add_page()
    md2.set_cont(mdstr)
    mnf.Show()

if __name__ == '__main__':
    app = wx.App()
    md_pad_test()
    md_frame_test()
    md_note_book()
    md_note_frame()
    app.MainLoop()
