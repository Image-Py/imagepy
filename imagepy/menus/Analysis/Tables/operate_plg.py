# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 12:04:18 2016
@author: yxl
"""
from imagepy import IPy
from imagepy.core.engine import Free

class Join(Free):
    title = 'Join Tables *'

    def run(self, para = None):
        IPy.alert('join two tabl with special field, not implemented!')
        
class AddField(Free):
    title = 'Add Field *'

    def run(self, para = None):
        IPy.alert('add ont field to the table, not implemented!')
        
class Frequence(Free):
    title = 'Frequence Field *'

    def run(self, para = None):
        IPy.alert('merge the same value and count frequence, not implemented!')
        
plgs = [Join, AddField, Frequence]