from sciapp.action import Table

class Transpose(Table):
	title = 'Table Transpose'

	def run(self, tps, snap, data, para = None):
		tps.data = data.T

class Crop(Table):
	title = 'Table Crop'
	note = ['req_sel']
	def run(self, tps, snap, data, para):
		tps.data = tps.subtab()

class Duplicate(Table):
	title = 'Table Duplicate'
	para = {'name':'Undefined'}

	def load(self, tps):
		self.para['name'] = tps.title+'-copy'
		self.view = [(str, 'name', 'Name', '')]
		return True

	def run(self, tps, snap, data, para = None):
		self.app.show_table(tps.subtab(), para['name'])

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
		tps.data = data.reindex(index=range(data.shape[0]+para['count']), \
			method=[None,'pad'][para['fill']])

class AddCol(Table):
	title = 'Add Column'
	para = {'name':'new', 'value':1.0}
	view = [(str, 'name', 'name', ''),
			('any', 'value', 'value')]

	def run(self, tps, snap, data, para = None):
		data[para['name']] = para['value']

plgs = [Transpose, Duplicate, Crop, '-', DeleteRow, DeleteCol, AppendRow, AddCol]