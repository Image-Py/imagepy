from sciapp.action import PolygonROI as Plugin

if __name__ == '__main__':
    from skimage.data import camera, astronaut
    from sciwx.app import ImageApp

    ImageApp.start(
        imgs = [('astronaut', astronaut())], 
        plgs=[('P', Plugin)])