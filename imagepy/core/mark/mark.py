import numpy as np
from math import sin, cos
from ..manager import ConfigManager

point = {'type':'point', 'color':(255,0,0), 'lw':1, 'body':(10,10)}
points = {'type':'points', 'color':(255,0,0), 'lw':1, 'body':[(10,10),(100,200)]}
line = {'type':'line', 'color':(255,0,0), 'lw':1, 'style':'-', 'body':[(10,10),(100,200),(200,200)]}
lines = {'type':'lines', 'color':(255,0,0), 'lw':1, 'style':'-', 'body':[[(10,10),(100,200),(200,200)],[(150,10),(50,250)]]}
polygon = {'type':'polygon', 'color':(255,0,0), 'fcolor':(255,255,0), 'lw':1, 'style':'o', 'body':[(10,10),(100,200),(200,200)]}
polygons = {'type':'polygons', 'color':(255,0,0), 'fcolor':(255,255,0,30), 'fill':False, 'lw':1, 'style':'o', 'body':[[(10,10),(100,200),(200,200)],[(150,10),(50,250),(288,0)]]}
circle = {'type':'circle', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':(100,100,50)}
circles = {'type':'circles', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':[(100,100,50),(300,300,100)]}
ellipse = {'type':'ellipse', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':(100,100,100,50,1)}
ellipses = {'type':'ellipses', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':[(100,100,100,50,1),(200,250,50,100,3.14)]}
rectangle = {'type':'rectangle', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':True, 'body':(100,100,80,50)}
rectangles = {'type':'rectangles', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':[(100,100,80,50),(200,200,80,100)]}
text = {'type':'text', 'color':(255,255,0), 'fcolor':(0,0,0), 'size':8, 'pt':True, 'body':(100,200,'id=0')}
texts = {'type':'texts', 'color':(255,255,0), 'fcolor':(0,0,0), 'size':8, 'pt':True, 'body':[(100,200,'id=0'),(180,250,'id=1')]}

layer = {'type':'layer', 'num':-1, 'clolor':(255,255,0), 'fcolor':(255,255,255), 'fill':False, 
			'body':[point, points, line, lines, polygon, polygons, circle, circles, ellipse, ellipses, rectangle, rectangles, text, texts]}
		
layers = {'type':'layers', 'num':-1, 'clolor':(255,255,0), 'fcolor':(255,255,255), 'fill':False, 
	'body':{1:points, 2:line, 3:layer}}

def plot(pts, dc, f, **key):
	pen, brush = dc.GetPen(), dc.GetBrush()
	width, color = pen.GetWidth(), pen.GetColour()
	fcolor, style = brush.GetColour(), brush.GetStyle()
	
	if 'color' in pts: 
		pen.SetColour(pts['color'])
	if 'fcolor' in pts:
		brush.SetColour(pts['fcolor'])
	if 'lw' in pts:
		pen.SetWidth(pts['lw'])
	if 'fill' in pts:
		brush.SetStyle((106,100)[pts['fill']])

	dc.SetPen(pen)
	dc.SetBrush(brush)
	
	if pts['type'] == 'point':
		pen.SetWidth(1)
		brush.SetStyle(100)
		brush.SetColour(pen.GetColour())
		dc.SetPen(pen)
		dc.SetBrush(brush)
		r = pts['r'] if 'r' in pts else 2
		x, y =  f(*pts['body'])
		dc.DrawEllipse (x-r,y-r,r*2,r*2)
		pen.SetWidth(pts['lw'] if 'lw' in pts else width)
		brush.SetStyle((106,100)[pts['fill']] if 'fill' in pts else style)
		brush.SetColour(pts['fc'] if 'fc' in pts else fcolor)
		dc.SetPen(pen)
		dc.SetBrush(brush)
	elif pts['type'] in {'points','line','polygon'}:
		lst, plst = [], []
		r = pts['r'] if 'r' in pts else 2
		for p in pts['body']:
			x, y =  f(*p)
			lst.append((x-r,y-r,r*2,r*2))
			plst.append((x,y))
		isline = 'style' in pts and '-' in pts['style']
		ispoint = 'style' in pts and 'o' in pts['style']
		if pts['type'] == 'polygon':
			dc.DrawPolygon(plst)
		
		if isline or pts['type'] == 'line':
			dc.DrawLines(plst)
		
		if pts['type']=='points' or ispoint:
			pen.SetWidth(1)
			brush.SetStyle(100)
			brush.SetColour(pen.GetColour())
			dc.SetPen(pen)
			dc.SetBrush(brush)
			dc.DrawEllipseList(lst)
			pen.SetWidth(pts['lw'] if 'lw' in pts else width)
			brush.SetStyle((106,100)[pts['fill']] if 'fill' in pts else style)
			brush.SetColour(pts['fc'] if 'fc' in pts else fcolor)
			dc.SetPen(pen)
			dc.SetBrush(brush)
	elif pts['type'] in {'lines','polygons'}:
		lst, plst = [], []
		r = pts['r'] if 'r' in pts else 2
		for i in pts['body']:
			line = []
			for p in i:
				x, y =  f(*p)
				lst.append((x-r,y-r,r*2,r*2))
				line.append((x,y))
			plst.append(line)
		isline = 'style' in pts and '-' in pts['style']
		ispoint = 'style' in pts and 'o' in pts['style']
		if pts['type'] == 'polygons':
			dc.DrawPolygonList(plst)
		
		if isline or pts['type'] == 'lines':
			for line in plst:
				dc.DrawLines(line)
		
		if pts['type']=='points' or ispoint:
			pen.SetWidth(1)
			brush.SetStyle(100)
			brush.SetColour(pen.GetColour())
			dc.SetPen(pen)
			dc.SetBrush(brush)
			dc.DrawEllipseList(lst)
			pen.SetWidth(pts['lw'] if 'lw' in pts else width)
			brush.SetStyle((106,100)[pts['fill']] if 'fill' in pts else style)
			brush.SetColour(pts['fc'] if 'fc' in pts else fcolor)
			dc.SetPen(pen)
			dc.SetBrush(brush)

	pen.SetWidth(width)
	pen.SetColour(color)
	brush.SetColour(fcolor)
	brush.SetStyle(style)
	dc.SetPen(pen)
	dc.SetBrush(brush)

def draw_circle(pts, dc, f, **key):
	pen, brush = dc.GetPen(), dc.GetBrush()
	width, color = pen.GetWidth(), pen.GetColour()
	fcolor, style = brush.GetColour(), brush.GetStyle()
	
	if 'color' in pts: 
		pen.SetColour(pts['color'])
	if 'fcolor' in pts:
		brush.SetColour(pts['fcolor'])
	if 'lw' in pts:
		pen.SetWidth(pts['lw'])
	if 'fill' in pts:
		brush.SetStyle((106,100)[pts['fill']])

	dc.SetPen(pen)
	dc.SetBrush(brush)

	if pts['type'] == 'circle':
		x, y ,r = pts['body']
		x, y =  f(x, y)
		dc.DrawCircle(x, y, r*key['k'])
	if pts['type'] == 'circles':
		lst = []
		for x, y ,r in pts['body']:
			x, y =  f(x, y)
			r *= key['k']
			lst.append((x-r,y-r,r*2,r*2))
		dc.DrawEllipseList(lst)

	pen.SetWidth(width)
	pen.SetColour(color)
	brush.SetColour(fcolor)
	brush.SetStyle(style)
	dc.SetPen(pen)
	dc.SetBrush(brush)

def make_ellipse(l1, l2, ang):
	m = np.array([[l1*cos(-ang),-l2*sin(-ang)],
				 [l1*sin(-ang),l2*cos(-ang)]])
	a = np.linspace(0, np.pi*2, 36)
	xys = np.array((np.cos(a), np.sin(a)))
	return np.dot(m, xys).T

def draw_ellipse(pts, dc, f, **key):
	pen, brush = dc.GetPen(), dc.GetBrush()
	width, color = pen.GetWidth(), pen.GetColour()
	fcolor, style = brush.GetColour(), brush.GetStyle()
	
	if 'color' in pts: 
		pen.SetColour(pts['color'])
	if 'fcolor' in pts:
		brush.SetColour(pts['fcolor'])
	if 'lw' in pts:
		pen.SetWidth(pts['lw'])
	if 'fill' in pts:
		brush.SetStyle((106,100)[pts['fill']])

	dc.SetPen(pen)
	dc.SetBrush(brush)

	if pts['type'] == 'ellipse':
		x, y ,l1, l2, a = pts['body']
		elp = make_ellipse(l1,l2,a)
		elp = elp*key['k']+f(x,y)
		dc.DrawPolygon(elp)
	if pts['type'] == 'ellipses':
		lst = []
		for x, y, l1, l2, a in pts['body']:
			elp = make_ellipse(l1,l2,a)
			lst.append(elp*key['k']+f(x,y))
		dc.DrawPolygonList(lst)
		

	pen.SetWidth(width)
	pen.SetColour(color)
	brush.SetColour(fcolor)
	brush.SetStyle(style)
	dc.SetPen(pen)
	dc.SetBrush(brush)

def draw_rectangle(pts, dc, f, **key):
	pen, brush = dc.GetPen(), dc.GetBrush()
	width, color = pen.GetWidth(), pen.GetColour()
	fcolor, style = brush.GetColour(), brush.GetStyle()
	
	if 'color' in pts: 
		pen.SetColour(pts['color'])
	if 'fcolor' in pts:
		brush.SetColour(pts['fcolor'])
	if 'lw' in pts:
		pen.SetWidth(pts['lw'])
	if 'fill' in pts:
		brush.SetStyle((106,100)[pts['fill']])

	dc.SetPen(pen)
	dc.SetBrush(brush)

	if pts['type'] == 'rectangle':
		x, y, w, h = pts['body']
		x, y = f(x, y)
		w, h = w*key['k'], h*key['k']
		dc.DrawRectangle(x-w/2, y-h/2, w, h)
	if pts['type'] == 'rectangles':
		lst = []
		for x, y, w, h in pts['body']:
			x, y = f(x, y)
			w, h = w*key['k'], h*key['k']
			lst.append((x-w/2, y-h/2, w, h))
		dc.DrawRectangleList(lst)

	pen.SetWidth(width)
	pen.SetColour(color)
	brush.SetColour(fcolor)
	brush.SetStyle(style)
	dc.SetPen(pen)
	dc.SetBrush(brush)

def draw_text(pts, dc, f, **key):
	pen, brush, font = dc.GetPen(), dc.GetBrush(), dc.GetFont()
	width, color = pen.GetWidth(), pen.GetColour()
	fcolor, style = brush.GetColour(), brush.GetStyle()
	size  = font.GetPointSize()
	tcolor = dc.GetTextForeground()
	bcolor = dc.GetTextBackground()
	
	if 'color' in pts: 
		pen.SetColour(pts['color'])
		dc.SetTextForeground(pts['color'])
	brush.SetColour(pen.GetColour())
	brush.SetStyle(100)
	if 'fcolor' in pts:
		dc.SetTextBackground(pts['fcolor'])
	if 'size' in pts:
		font.SetPointSize(pts['size'])

	dc.SetPen(pen)
	dc.SetBrush(brush)
	dc.SetFont(font)

	if pts['type'] == 'text':
		x, y, text = pts['body']
		x, y = f(x, y)
		dc.DrawText(text, x+3, y+3)
		if not 'pt' in pts or pts['pt']:
			dc.DrawEllipse(x-2,y-2,4,4)
	if pts['type'] == 'texts':
		tlst, clst, elst = [], [], []
		for x, y, text in pts['body']:
			x, y = f(x, y)
			tlst.append(text)
			clst.append((x+3, y+3))
			elst.append((x-2, y-2, 4, 4))
		dc.DrawTextList(tlst, clst)
		if not 'pt' in pts or pts['pt']:
			dc.DrawEllipseList(elst)

	font.SetPointSize(size)
	pen.SetColour(color)
	brush.SetColour(fcolor)
	brush.SetStyle(style)
	dc.SetPen(pen)
	dc.SetBrush(brush)
	dc.SetFont(font)
	dc.SetTextForeground(tcolor)
	dc.SetTextBackground(bcolor)

draw_dic = {'points':plot, 'point':plot, 'line':plot, 'polygon':plot, 'lines':plot, 'polygons':plot,
			'circle':draw_circle, 'circles':draw_circle, 'ellipse':draw_ellipse, 'ellipses':draw_ellipse,
			'rectangle':draw_rectangle, 'rectangles':draw_rectangle, 'text':draw_text, 'texts':draw_text}

def draw(obj, dc, f, **key): draw_dic[obj['type']](obj, dc, f, **key)

def draw_layer(pts, dc, f, **key):
	pen, brush = dc.GetPen(), dc.GetBrush()
	width, color = pen.GetWidth(), pen.GetColour()
	fcolor, style = brush.GetColour(), brush.GetStyle()
	
	if 'color' in pts: 
		pen.SetColour(pts['color'])
	if 'fcolor' in pts:
		brush.SetColour(pts['fcolor'])
	if 'lw' in pts:
		pen.SetWidth(pts['lw'])
	if 'fill' in pts:
		brush.SetStyle((106,100)[pts['fill']])

	dc.SetPen(pen)
	dc.SetBrush(brush)

	for i in pts['body']:draw(i, dc, f, **key)

	pen.SetWidth(width)
	pen.SetColour(color)
	brush.SetColour(fcolor)
	brush.SetStyle(style)
	dc.SetPen(pen)
	dc.SetBrush(brush)

draw_dic['layer'] = draw_layer

def draw_layers(pts, dc, f, **key):
	pen, brush = dc.GetPen(), dc.GetBrush()
	width, color = pen.GetWidth(), pen.GetColour()
	fcolor, style = brush.GetColour(), brush.GetStyle()
	
	if 'color' in pts: 
		pen.SetColour(pts['color'])
	if 'fcolor' in pts:
		brush.SetColour(pts['fcolor'])
	if 'lw' in pts:
		pen.SetWidth(pts['lw'])
	if 'fill' in pts:
		brush.SetStyle((106,100)[pts['fill']])

	dc.SetPen(pen)
	dc.SetBrush(brush)
	if key['cur'] in pts['body']:
		draw(pts['body'][key['cur']], dc, f, **key)

	pen.SetWidth(width)
	pen.SetColour(color)
	brush.SetColour(fcolor)
	brush.SetStyle(style)
	dc.SetPen(pen)
	dc.SetBrush(brush)

draw_dic['layers'] = draw_layers

class GeometryMark:
	def __init__(self, body):
		self.body = body

	def draw(self, dc, f, **key):
		pen, brush, font = dc.GetPen(), dc.GetBrush(), dc.GetFont()
		pen.SetColour(ConfigManager.get('mark_color') or (255,255,0))
		brush.SetColour(ConfigManager.get('mark_fcolor') or (255,255,255))
		brush.SetStyle((106,100)[ConfigManager.get('mark_fill') or False])
		pen.SetWidth(ConfigManager.get('mark_lw') or 1)
		dc.SetTextForeground(ConfigManager.get('mark_tcolor') or (255,0,0))
		font.SetPointSize(ConfigManager.get('mark_tsize') or 8)
		dc.SetPen(pen); dc.SetBrush(brush); dc.SetFont(font);
		draw(self.body, dc, f, **key)

if __name__ == '__main__':
	print(make_ellipse(0,0,2,1,0))