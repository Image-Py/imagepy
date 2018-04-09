from imagepy.core.engine import Simple
import pytesseract
from imagepy import IPy

class Plugin(Simple):
    title = 'Tensseract OCR'
    note = ['8-bit']
    #process
    def run(self, ips, imgs, para = None):
        print(ips.img.dtype, ips.img.shape)
        code = pytesseract.image_to_string(ips.get_subimg())
        IPy.write(code, 'Tensseract-OCR')