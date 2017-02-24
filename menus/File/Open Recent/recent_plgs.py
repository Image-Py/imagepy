# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 02:38:04 2016

@author: yxl
"""
from core import managers
from core.engines import Macros
import IPy

recent = managers.ConfigManager.get('recent')

def f(path):
	return Macros(path, ["Open>{'path':%s}"%repr(path)])

def add(path):
	global recent, plgs
	if path in recent:
		idx = recent.index(path)
		recent.insert(0, recent.pop(idx))
		plgs.insert(0, plgs.pop(idx))
	else: 
		recent.insert(0, path)
		plgs.insert(0, f(path))
	if len(recent)>5:
		recent = recent[:5]
		plgs = plgs[:5]

	managers.ConfigManager.set('recent', recent)
	IPy.curapp.reload_plugins()

plgs = [f(i) for i in recent]