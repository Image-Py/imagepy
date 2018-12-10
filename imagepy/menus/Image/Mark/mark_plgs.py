from imagepy.core.engine import Simple, Free
from imagepy.core.mark import GeometryMark
from imagepy.core.manager import ConfigManager
import json
from imagepy import IPy

class Clear(Simple):
    """Save: save roi as a wkt file """
    title = 'Clear Mark'
    note = ['all']

    def run(self, ips, imgs, para = None):
        ips.mark = None

class Save(Simple):
    """Save: save roi as a wkt file """
    title = 'Save Mark'
    note = ['all']
    para={'path':''}

    def load(self, ips):
        if not isinstance(ips.mark, GeometryMark):
            IPy.alert('only geometry mark could be saved!')
            return False
        return True

    def show(self):
        filt = 'MARK files (*.mrk)|*.mrk'
        return IPy.getpath('Save..', filt, 'save', self.para)

    def run(self, ips, imgs, para = None):
        f = open(para['path'], 'w')
        f.write(json.dumps(ips.mark.body))
        f.close()

class Open(Simple):
    """Save: save roi as a wkt file """
    title = 'Open Mark'
    note = ['all']
    para={'path':''}

    def show(self):
        filt = 'MARK files (*.mrk)|*.mrk'
        return IPy.getpath('Open..', filt, 'open', self.para)

    def run(self, ips, imgs, para = None):
        f = open(para['path'])
        geo = json.load(f)
        f.close()
        if geo['type'] == 'layers':
            body = geo['body']
            for i in list(body.keys()):
                body[int(i)] = body.pop(i)
        ips.mark = GeometryMark(geo)

class Setting(Free):
    title = 'Mark Setting'

    view = [('color', 'color', 'line', 'color'),
            ('color', 'fcolor', 'face', 'color'),
            ('color', 'tcolor', 'text', 'color'),
            (int, 'lw', (1,10), 0, 'width', 'pix'),
            (int, 'size', (1,30), 0, 'text', 'size'),
            (bool, 'fill', 'solid fill')]

    def load(self):
        Setting.para = para = {}
        para['color'] = ConfigManager.get('mark_color') or (255,255,0)
        para['fcolor'] = ConfigManager.get('mark_fcolor') or (255,255,255)
        para['fill'] = ConfigManager.get('mark_fill') or False
        para['lw'] = ConfigManager.get('mark_lw') or 1
        para['size'] =  ConfigManager.get('mark_tsize') or 8
        para['tcolor'] = ConfigManager.get('mark_tcolor') or (255,0,0)
        return True

    def run(self, para=None):
        ConfigManager.set('mark_color', para['color'])
        ConfigManager.set('mark_fcolor', para['fcolor'])
        ConfigManager.set('mark_tcolor', para['tcolor'])
        ConfigManager.set('mark_lw', para['lw'])
        ConfigManager.set('mark_fill', para['fill'])
        ConfigManager.set('mark_tsize', para['size'])

plgs = [Open, Save, Clear, '-', Setting]