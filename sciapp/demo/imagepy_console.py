from imagepy.app import Console

con = Console()
con.load_plugins()

cmds = [('coins',None),
        ('Up And Down Watershed',{'thr1': 29, 'thr2': 178, 'type': 'up area'}),
        ('Fill Holes',None),
        ('Geometry Filter',{'con': '4-connect', 'inv': False, 'area': 10.0, 'l': 0.0, 'holes': 0, 'solid': 0.0, 'e': 0.0, 'front': 255, 'back': 0}),
        ('Geometry Analysis',{'con': '8-connect', 'center': True, 'area': True, 'l': True, 'extent': False, 'cov': True, 'slice': False, 'ed': False, 'holes': False, 'ca': False, 'fa': False, 'solid': False}),
        ('PNG Save',{'path': 'C:/Users/54631/Desktop/conis.png'}),
        ('CSV Save',{'path': 'C:/Users/54631/Desktop/coins.csv'})]
