from sciapp.action import Table
import pandas as pd

class Plugin(Table):
	title = 'Table Sort By Key'

	para = {'major':None, 'minor':None, 'descend':False}
		
	view = [('field', 'major', 'major', 'key'),
			('field', 'minor', 'minor', 'key'),
			(bool, 'descend', 'descend')]

	def run(self, tps, snap, data, para=None):
		by = [para['major'], para['minor']]
		tps.data.sort_values(by=[i for i in by if i != 'None'], 
			axis=0, ascending=not para['descend'], inplace=True)