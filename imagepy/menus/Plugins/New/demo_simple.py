# -*- coding: utf-8 -*-
from sciapp.action import Simple

# a simple demo implements the next slice
class Plugin(Simple):
    # the title on the menu
    title = 'Next Slice'
    # the describe parameter
    note = ['all']

    # increase the current
    def run(self, ips, imgs, para = None):
        if ips.cur<ips.get_nslices()-1:ips.cur+=1
            
# you can also write muti class in the current modal then:
# plgs = [class1, class2...]