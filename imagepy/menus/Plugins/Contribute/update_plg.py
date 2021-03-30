from sciapp.action import Free
import sys, re, os.path as osp
from urllib.request import urlretrieve, urlopen

class Plugin(Free):
    title = 'Update Plugins List'
    
    def run(self, para = None):
        try:
            here = osp.abspath(osp.dirname(__file__))
            url = 'https://gitee.com/imagepy/imagepy/tree/master/imagepy/menus/Plugins/Contribute'
            temp = re.compile('imagepy/imagepy/blob/master/imagepy/menus/Plugins/Contribute/Contributions/.*?md')
            rst = urlopen(url+'/Contributions').read().decode('utf-8')
            records = ['https://gitee.com/'+i.replace('blob', 'raw') for i in temp.findall(rst)]
            for i in records: urlretrieve(i, osp.join(here, 'Contributions', osp.split(i)[-1].replace('%20',' ')))
            urlretrieve(url.replace('tree', 'raw')+'/Site%20Plugins%20List.md', osp.join(here, 'Site Plugins List.md'))
            self.app.alert('site plugins list updated!')
        except Exception as e:
            self.app.alert('update failed!\tErrof:%s'%sys.exc_info()[1])