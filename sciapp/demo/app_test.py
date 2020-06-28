import sys
sys.path.append('../../')

cmds = [
    ("Open", {'path': 'C:/Users/54631/Desktop/1.jpg'}),
    ("Gaussian", {'sigma': 5.0}),
    ("Save Image", {'path': 'C:/Users/54631/Desktop/1_blur.bmp'})]

if __name__ == '__main__':
    from sciapp import App
    from sciapp.action.plugin import OpenFile, SaveImage
    from sciapp.action.plugin.filters import Gaussian
    
    app = App(asyn=False)

    for i in [OpenFile, SaveImage, Gaussian]:
        app.add_plugin(i.title, i)
    
    '''
    app.alert('Hello, SciApp!')
    OpenFile().start(app, {'path': 'C:/Users/54631/Desktop/1.jpg'})
    Gaussian().start(app, {'sigma': 5.0})
    SaveImage().start(app,{'path': 'C:/Users/54631/Desktop/1_blur.bmp'})
    '''
    app.run_macros(cmds)
    # C:/Users/54631/Desktop/1.jpg
    
