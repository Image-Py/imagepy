import sys, wx
sys.path.append('../../')

from sciwx.text import TextPad, TextNoteBook, TextFrame, TextNoteFrame

def text_pad_test():
    frame = wx.Frame(None, title='Text Pad')
    textpad = TextPad(frame)
    textpad.append('abcdefg')
    frame.Show()

def text_frame_test():
    textframe = TextFrame(None)
    textframe.append('abcdefg')
    textframe.Show()

def text_note_book():
    frame = wx.Frame(None, title='Text Note Book')
    tnb = TextNoteBook(frame)
    note1 = tnb.add_notepad()
    note1.append('abc')
    note1 = tnb.add_notepad()
    note1.append('def')
    frame.Show()

def text_note_frame():
    npbf = TextNoteFrame(None)
    note1 = npbf.add_notepad()
    note1.append('abc')
    note1 = npbf.add_notepad()
    note1.append('def')
    npbf.Show()
    
if __name__ == '__main__':
    app = wx.App()
    text_pad_test()
    text_frame_test()
    text_note_book()
    text_note_frame()
    app.MainLoop()
