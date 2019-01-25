from imagepy.core.engine import Table
from imagepy import IPy

class Transpose(Table):
	title = 'Table Transpose'

	def run(self, tps, snap, data, para = None):
		tps.set_data(data.T)

class Corp(Table):
	title = 'Table Corp'
	note = ['req_sel']
	def run(self, tps, snap, data, para):
		tps.set_data(data.loc[tps.rowmsk, tps.colmsk])

class Duplicate(Table):
	title = 'Table Duplicate'
	para = {'name':'Undefined'}

	def load(self, tps):
		self.para['name'] = tps.title+'-copy'
		self.view = [(str, 'name', 'Name', '')]
		return True

	def run(self, tps, snap, data, para = None):
		newdata = data.loc[tps.rowmsk, tps.colmsk]
		IPy.show_table(para['name'], newdata)

class DeleteRow(Table):
	title = 'Delete Rows'
	note = ['row_sel']

	def run(self, tps, snap, data, para = None):
		data.drop(tps.rowmsk, inplace=True)

class DeleteCol(Table):
	title = 'Delete Columns'
	note = ['col_sel']

	def run(self, tps, snap, data, para = None):
		data.drop(tps.colmsk, axis=1, inplace=True)

class AppendRow(Table):
	title = 'Append Rows'
	para = {'count':1, 'fill':True}
	view = [(int, 'count', (1,100), 0, 'count', ''),
			(bool, 'fill', 'fill by last row')]

	def run(self, tps, snap, data, para = None):
		newdata = data.reindex(index=range(data.shape[0]+para['count']), \
			method=[None,'pad'][para['fill']])
		tps.set_data(newdata)

class AddCol(Table):
	title = 'Add Column'
	para = {'name':'new', 'value':1.0}
	view = [(str, 'name', 'name', ''),
			('any', 'value', 'value')]

	def run(self, tps, snap, data, para = None):
		ctype = data.columns.dtype.type
		data[ctype(para['name'])] = para['value']
		print(data.info())

plgs = [Transpose, Duplicate, Corp, '-', DeleteRow, DeleteCol, AppendRow, AddCol]