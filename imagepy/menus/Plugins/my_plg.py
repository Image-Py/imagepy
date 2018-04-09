from imagepy.core.engine import Filter

class Plugin(Filter):
    """Gaussian: derived from imagepy.core.engine.Filter """
    title = 'My Filter'
    note = ['8-bit', 'auto_msk', '2int', 'auto_snap', 'preview']
    para = {'v':2}
    view = [(int, (0,100), 0,  'add', 'v', 'value')]
    
    def run(self, ips, snap, img, para = None):
        img[:] = snap + para['v']
