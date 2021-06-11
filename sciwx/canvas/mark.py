import numpy as np
from math import sin, cos
from sciapp import Source

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
text = {'type':'text', 'color':(255,255,0), 'fcolor':(0,0,0), 'lw':8, 'fill':True, 'body':(100,200,'id=0')}
texts = {'type':'texts', 'color':(255,255,0), 'fcolor':(0,0,0), 'lw':8, 'fill':True, 'body':[(100,200,'id=0'),(180,250,'id=1')]}

layer = {'type':'layer', 'num':-1, 'clolor':(255,255,0), 'fcolor':(255,255,255), 'fill':False, 
			'body':[point, points, line, lines, polygon, polygons, circle, circles, ellipse, ellipses, rectangle, rectangles, text, texts]}
		
layers = {'type':'layers', 'num':-1, 'clolor':(255,255,0), 'fcolor':(255,255,255), 'fill':False, 
	'body':{1:points, 2:line, 3:layer}}

def cross(ori, cont, win, cell):
    kx = (cont[2]-cont[0])/(ori[2]-ori[0])
    ky = (cont[3]-cont[1])/(ori[3]-ori[1])
    ox = cont[0] - ori[0]*kx
    oy = cont[1] - ori[1]*kx
    cell = [cell[0]*kx+ox, cell[1]*ky+oy, 
        cell[2]*kx+ox, cell[3]*kx+oy]
    if cell[0]>win[2] or cell[2]<win[0]: return 0
    if cell[1]>win[3] or cell[3]<win[1]: return 0
    l = (cell[2]-cell[0])**2 + (cell[3]-cell[1])**2
    return max(int(l ** 0.5), 5)

def plot(pts, dc, f, **key):
	oribox, conbox, winbox = key['oribox'], key['conbox'], key['winbox']
	sap = cross(oribox, conbox, winbox, pts.box)
	if sap == 0: return

	pen, brush = dc.GetPen(), dc.GetBrush()
	width, color = pen.GetWidth(), pen.GetColour()
	fcolor, style = brush.GetColour(), brush.GetStyle()
	
	if pts.color:
		pen.SetColour(pts.color)
	if pts.fcolor:
		brush.SetColour(pts.fcolor)
	if pts.lw:
		pen.SetWidth(pts.lw)
	if not pts.fill is None:
		brush.SetStyle((106,100)[pts.fill])

	dc.SetPen(pen)
	dc.SetBrush(brush)
	
	if pts.dtype == 'point':
		pen.SetWidth(1)
		brush.SetStyle(100)
		brush.SetColour(pen.GetColour())
		dc.SetPen(pen)
		dc.SetBrush(brush)
		r = pts.r or 2
		x, y =  f(*pts.body)
		dc.DrawEllipse((x-r).round(),(y-r).round(),r*2,r*2)
		pen.SetWidth(pts.lw or width)
		brush.SetStyle(style if pts.fill is None else (106,100)[pts.fill])
		brush.SetColour(pts.fcolor or fcolor)
		dc.SetPen(pen)
		dc.SetBrush(brush)
	elif pts.dtype in {'points','line'}:
		lst, plst = [], []
		r = 2
		x, y = pts.body.T[:2]
		xy = np.vstack(f(x, y)).T
		lst = np.hstack((xy-r, np.ones((len(x),2))*(r*2)))
		isline = pts.lstyle and '-' in pts.lstyle
		ispoint = pts.lstyle and 'o' in pts.lstyle
		if pts.dtype == 'polygon':
			dc.DrawPolygon(xy.round())
		
		if isline or pts.dtype == 'line':
			dc.DrawLines(xy.round())
		
		if pts.dtype=='points' or ispoint:
			pen.SetWidth(1)
			brush.SetStyle(100)
			brush.SetColour(pen.GetColour())
			dc.SetPen(pen)
			dc.SetBrush(brush)
			dc.DrawEllipseList(lst.round())
			pen.SetWidth(pts.lw if not pts.lw is None else width)
			brush.SetStyle((106,100)[pts.fill] if pts.fill != None else style)
			brush.SetColour(pts.fcolor or fcolor)
			dc.SetPen(pen)
			dc.SetBrush(brush)
	elif pts.dtype in {'lines','polygon', 'polygons'}:
		body, lst, plst = [], [], []
		if pts.dtype != 'polygons':
			body = pts.body
		else:
			for i in pts.body: body.extend(i)
		r = 2
		for i in body:
			if len(i)>sap:
				idx = np.linspace(0, len(i), min(len(i), sap), False, dtype=np.uint16)
				i = i[idx]
			x, y = i.T[:2]
			xy = np.vstack(f(x, y)).T
			lst.append(np.hstack((xy-r, np.ones((len(x),2))*(r*2))))
			plst.append(xy)
		isline = pts.lstyle and '-' in pts.lstyle
		ispoint = pts.lstyle and 'o' in pts.lstyle
		if pts.dtype in {'polygon', 'polygons'}:
			dc.DrawPolygonList(plst)
		
		if isline or pts.dtype == 'lines':
			for line in plst:
				dc.DrawLines(line)
		
		if ispoint:
			pen.SetWidth(1)
			brush.SetStyle(100)
			brush.SetColour(pen.GetColour())
			dc.SetPen(pen)
			dc.SetBrush(brush)
			for i in lst: dc.DrawEllipseList(i.round())
			pen.SetWidth(pts.lw or width)
			brush.SetStyle((106,100)[pts.fill] if pts.fill != None else style)
			brush.SetColour(pts.fcolor or fcolor)
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
	
	if not pts.color is None: 
		pen.SetColour(pts.color)
	if not pts.fcolor is None:
		brush.SetColour(pts.fcolor)
	if not pts.lw is None:
		pen.SetWidth(pts.lw)
	if not pts.fill is None:
		brush.SetStyle((106,100)[pts.fill])

	dc.SetPen(pen)
	dc.SetBrush(brush)

	if pts.dtype == 'circle':
		x, y ,r = pts.body
		x, y =  f(x, y)
		dc.DrawCircle(x, y, r*key['k'])
	if pts.dtype == 'circles':
		lst = []
		x, y, r = pts.body.T
		x, y = f(x, y)
		r = r * key['k']
		lst = np.vstack([x-r, y-r, r*2, r*2]).T
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
	
	if not pts.color is None: 
		pen.SetColour(pts.color)
	if not pts.fcolor is None:
		brush.SetColour(pts.fcolor)
	if not pts.lw is None:
		pen.SetWidth(pts.lw)
	if not pts.fill is None:
		brush.SetStyle((106,100)[pts.fill])

	dc.SetPen(pen)
	dc.SetBrush(brush)

	if pts.dtype == 'ellipse':
		x, y ,l1, l2, a = pts.body
		elp = make_ellipse(l1,l2,a) + (x,y)
		elp = np.vstack(f(*elp.T[:2])).T
		dc.DrawPolygon(elp)
	if pts.dtype == 'ellipses':
		lst = []
		for x, y, l1, l2, a in pts.body:
			elp = make_ellipse(l1,l2,a) + (x,y)
			lst.append(np.vstack(f(*elp.T[:2])).T)
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
	
	if not pts.color is None: 
		pen.SetColour(pts.color)
	if not pts.fcolor is None:
		brush.SetColour(pts.fcolor)
	if not pts.lw is None:
		pen.SetWidth(pts.lw)
	if not pts.fill is None:
		brush.SetStyle((106,100)[pts.fill])

	dc.SetPen(pen)
	dc.SetBrush(brush)

	if pts.dtype == 'rectangle':
		x, y, w, h = pts.body
		w, h = f(x+w, y+h)
		x, y = f(x, y)
		dc.DrawRectangle(x.round(), (y).round(), 
			(w-x).round(), (h-y).round())
	if pts.dtype == 'rectangles':
		x, y, w, h = pts.body.T
		w, h = f(x+w, y+h)
		x, y = f(x, y)
		lst = np.vstack((x,y,w-x,h-y)).T
		dc.DrawRectangleList(lst.round())

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
	dc.SetTextForeground(color)
	dc.SetTextBackground(fcolor)
	if not pts.color is None: 
		pen.SetColour(pts.color)
		dc.SetTextForeground(pts.color)
	brush.SetColour(pen.GetColour())
	brush.SetStyle(100)
	if not pts.fill is None:
		dc.SetBackgroundMode((106, 100)[pts.fill])
	if not pts.fcolor is None:
		dc.SetTextBackground(pts.fcolor)
	if not pts.lw is None:
		font.SetPointSize(pts.lw)

	dc.SetPen(pen)
	dc.SetBrush(brush)
	dc.SetFont(font)

	if pts.dtype == 'text':
		(x, y), text = pts.body, pts.txt
		x, y = f(x, y)
		dc.DrawText(text, x+1, y+1)
		if not pts.lstyle is None:
			dc.DrawEllipse(x-2,y-2,4,4)
	if pts.dtype == 'texts':
		tlst, clst, elst = [], [], []
		x, y = pts.body.T
		tlst = pts.txt
		x, y = f(x, y)
		r = x * 0 + 4
		dc.DrawTextList(tlst, np.vstack((x,y)).T)
		if pts.fill:
			dc.DrawEllipseList(np.vstack((x,y,r,r)).T)

	font.SetPointSize(size)
	pen.SetColour(color)
	brush.SetColour(fcolor)
	brush.SetStyle(style)
	dc.SetPen(pen)
	dc.SetBrush(brush)
	dc.SetFont(font)
	dc.SetTextForeground(tcolor)
	dc.SetTextBackground(bcolor)

draw_dic = {'points':plot, 'point':plot, 'line':plot, 
			'polygon':plot, 'lines':plot, 'polygons':plot, 
			'circle':draw_circle, 'circles':draw_circle, 
			'ellipse':draw_ellipse, 'ellipses':draw_ellipse, 
			'rectangle':draw_rectangle, 'rectangles':draw_rectangle, 
			'text':draw_text, 'texts':draw_text}

def draw(obj, dc, f, **key): 
	if len(obj.body)==0: return
	draw_dic[obj.dtype](obj, dc, f, **key)

def draw_layer(pts, dc, f, **key):
	pen, brush = dc.GetPen(), dc.GetBrush()
	width, color = pen.GetWidth(), pen.GetColour()
	fcolor, style = brush.GetColour(), brush.GetStyle()
	tcolor = dc.GetTextForeground()
	if pts.color: 
		pen.SetColour(pts.color)
	if pts.tcolor:
		dc.SetTextForeground(pts.tcolor)
	if pts.fcolor: 
		brush.SetColour(pts.fcolor)
	if pts.lw != None: 
		pen.SetWidth(pts.lw)
	if not pts.fill is None:
		brush.SetStyle((106,100)[pts.fill])

	dc.SetPen(pen)
	dc.SetBrush(brush)

	for i in pts.body:draw(i, dc, f, **key)

	dc.SetTextForeground(tcolor)
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
	
	if pts.color: 
		pen.SetColour(pts.color)
	if pts.fcolor: 
		brush.SetColour(pts.fcolor)
	if pts.lw != None: 
		pen.SetWidth(pts.lw)
	if pts.fill: 
		brush.SetStyle((106,100)[pts.fill])

	dc.SetPen(pen)
	dc.SetBrush(brush)
	print(pts.body.keys(), key['cur'])
	if key['cur'] in pts.body:
		draw(pts.body[key['cur']], dc, f, **key)

	pen.SetWidth(width)
	pen.SetColour(color)
	brush.SetColour(fcolor)
	brush.SetStyle(style)
	dc.SetPen(pen)
	dc.SetBrush(brush)

draw_dic['layers'] = draw_layers

def drawmark(dc, f, body, **key):
	default_style = body.default
	pen, brush, font = dc.GetPen(), dc.GetBrush(), dc.GetFont()
	pen.SetColour(default_style['color'])
	brush.SetColour(default_style['fcolor'])
	brush.SetStyle((106,100)[default_style['fill']])
	pen.SetWidth(default_style['lw'])
	dc.SetTextForeground(default_style['tcolor'])
	font.SetPointSize(default_style['size'])
	dc.SetPen(pen); dc.SetBrush(brush); dc.SetFont(font);
	draw(body, dc, f, **key)

if __name__ == '__main__':
	pass
	# print(make_ellipse(0,0,2,1,0))