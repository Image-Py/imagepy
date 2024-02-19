from setuptools import setup
import setuptools, os

descr = 'Image process framework based on plugin like imagej, it is esay to glue with scipy.ndimage, scikit-image, opencv, simpleitk, mayavi...and any libraries based on numpy'

def get_data_files():
    dic = {}
    for root, dirs, files in os.walk('imagepy', True):
        root = root.replace('/', '.').replace('\\', '.')
        files = [i for i in files if not '.py' in i]
        if len(files)==0:continue
        dic[root] = files
    return dic

if __name__ == '__main__':
    setup(name='imagepy',
        version='0.22',
        url='https://github.com/Image-Py/imagepy',
        description='interactive python image-processing plugin framework',
        long_description=descr,
        author='YXDragon',
        author_email='yxdragon@imagepy.org',
        license='BSD 3-clause',
        packages=setuptools.find_packages(),
        entry_points={
        'console_scripts': [
            'imagepy = imagepy:show',
        ],
    },
        package_data=get_data_files(),
        install_requires=[
            'scikit-image',
            'scikit-learn',
            'shapely',
            'pypubsub',
            'wxpython',
            'read_roi',
            'numpy-stl',
            'pydicom',
            'pystackreg',
            'pandas',
            'xlrd',
            'xlwt',
            'openpyxl',
            'markdown',
            'python-markdown-math',
            'numba',
            'dulwich'
        ],
    )
