# -*- coding: utf-8 -*-
from core.engine import Free
import IPy

class Plugin(Free):
    # the title on the menu
    title = 'Demo Free'

    # do what you want lere
    def run(self, para = None):
        IPy.alert('Do what you like here!')
        
# you can also write muti class in the current modal then:
# plgs = [class1, class2...]