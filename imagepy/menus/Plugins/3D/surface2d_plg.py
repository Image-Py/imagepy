# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 22:33:33 2017

@author: yxl
"""
from imagepy import IPy
from imagepy.core.engine import Simple
from scipy.ndimage.filters import gaussian_filter

class Plugin(Simple):
    title = '2D Surface'
    note = ['8-bit', '16-bit']
    para = {'scale':2, 'sigma':2,'h':1}
    view = [(int, (1,5), 0, 'down scale', 'scale', 'pix'),
            (int, (0,30), 0, 'sigma', 'sigma', ''),
            (float, (0.1,10), 1, 'scale z', 'h', '')]
    
    def run(self, ips, imgs, para = None):
        '''
        from mayavi import mlab
        img = ips.img
        scale, sigma = para['scale'], para['sigma']
        imgblur = gaussian_filter(img[::scale,::scale], sigma)
        mlab.surf(imgblur, warp_scale=para['h'])
        mlab.show()
        '''
        import vtk

        cone_a=vtk.vtkConeSource()

        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInputConnection(cone_a.GetOutputPort())

        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)


        ren1= vtk.vtkRenderer()
        ren1.AddActor( coneActor )
        ren1.SetBackground( 0.1, 0.2, 0.4 )

        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer( ren1 )
        renWin.SetSize( 300, 300 )
        renWin.Render()

        iren=vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

        iren.Initialize()
        iren.Start()

if __name__ == '__main__':
    pass