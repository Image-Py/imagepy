from setuptools import setup
import setuptools

descr = 'Image process framework based on plugin like imagej, it is esay to glue with scipy.ndimage, scikit-image, opencv, simpleitk, mayavi...and any libraries based on numpy'

if __name__ == '__main__':
    setup(name='imagepy',
        version='0.1',
        url='https://github.com/Image-Py/imagepy',
        description='interactive python image-processing plugin framework',
        long_description=descr,
        author='YXDragon',
        author_email='yxdragon@imagepy.org',
        license='BSD 3-clause',
        packages=setuptools.find_packages(),
        include_package_data=True,
        data_files=[('123', ['imagepy/data/123.dat'])],
        install_requires=[
            'scikit-image',
            'shapely',
            'wxpython',
            'numba',
            'dicom'
        ],
    )
