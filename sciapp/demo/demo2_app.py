import sys
sys.path.append('../../')
from sciapp import App

def basic_test():
    app = App()
    # alert a message
    app.alert('Hello!', title='SciApp')
    # show a text, here just print it
    app.show_txt('Hello', title='SciApp')
    # show a markdown text, here just print it
    app.show_md('Hello', title='SciApp')
    # yes or no
    rst = app.yes_no('Are you ok?', 'SciApp')
    print(rst)

def para_test():
    app = App()
    para = {'name':'', 'age':5}
    view = [(str, 'name', 'your', 'name'),
            (int, 'age', (0,120), 0, 'your', 'age')]
    rst = app.show_para('Personal Information', para, view)
    # >>> your: ? name <str> yxdragon
    # >>> your: ? age <int> 32
    print(rst)
    # >>> {'name':'yxdragon', 'age':32}

def object_test():
    '''
    there is a manager for every type of object.
    such as img_manager, we can call app's:
    show_img, close_img, active_img, get_img
    '''
    from sciapp.object import Image
    from skimage.data import camera

    app = App()
    image = Image([camera()], 'camera')
    app.show_img(image, 'camera')
    # >>> UINT8  512x512  S:1/1  C:0/1  0.25M
    print(app.get_img())
    # >>> <sciapp.object.image.Image object at 0x000002076A025780>
    print(app.img_names())
    # >>> ['camera']
    app.close_img('camera')
    # >>> close image: camera
    print(app.img_names())
    # >>> []

if __name__ == '__main__':
    basic_test()
    para_test()
    object_test()
