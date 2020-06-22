import sys, wx
sys.path.append('../../')
from sciwx.widgets import ParaDialog

if __name__ == '__main__':
    para = {'name':'yxdragon', 'age':10, 'h':1.72, 'w':70, 'sport':True, 'sys':'Mac', 'lan':['C/C++', 'Python'], 'c':(255,0,0)} 

    view = [('lab', 'lab', 'This is a questionnaire'),
            (str, 'name', 'name', 'please'), 
            (int, 'age', (0,150), 0, 'age', 'years old'),
            (float, 'h', (0.3, 2.5), 2, 'height', 'm'),
            ('slide', 'w', (1, 150), 0, 'weight','kg'),
            (bool, 'sport', 'do you like sport'),
            (list, 'sys', ['Windows','Mac','Linux'], str, 'favourite', 'system'),
            ('chos', 'lan', ['C/C++','Java','Python'], 'lanuage you like(multi)'),
            ('color', 'c', 'which', 'you like')]

    app = wx.App()
    dic = {'height':'高度', 'm':'米'}
    pd = ParaDialog(None, 'Test', dic)
    pd.init_view(view, para, preview=True, modal=False)
    pd.pack()
    pd.ShowModal()
    print(para)
    app.MainLoop()
