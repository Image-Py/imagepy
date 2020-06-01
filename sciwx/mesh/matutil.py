import numpy as np

def look_at(eye, target, up, dtype=None):
    forward = (target - eye)/np.linalg.norm(target - eye)
    side = (np.cross(forward, up))/np.linalg.norm(np.cross(forward, up))
    up = (np.cross(side, forward)/np.linalg.norm(np.cross(side, forward)))

    return np.array((
            (side[0], up[0], -forward[0], 0.),
            (side[1], up[1], -forward[1], 0.),
            (side[2], up[2], -forward[2], 0.),
            (-np.dot(side, eye), -np.dot(up, eye), np.dot(forward, eye), 1.0)
        ), dtype=np.float32)

def perspective(xmax, ymax, near, far):
	left, right = -xmax, xmax
	bottom, top = -ymax, ymax

	A = (right + left) / (right - left)
	B = (top + bottom) / (top - bottom)
	C = -(far + near) / (far - near)
	D = -2. * far * near / (far - near)
	E = 2. * near / (right - left)
	F = 2. * near / (top - bottom)
	return np.array((
		(  E, 0., 0., 0.),
		( 0.,  F, 0., 0.),
		(  A,  B,  C,-1.),
		( 0., 0.,  D, 0.),
	), dtype=np.float32)

def orthogonal(xmax, ymax, near, far):
	rml = xmax * 2
	tmb = ymax * 2
	fmn = far - near

	A = 2. / rml
	B = 2. / tmb
	C = -2. / fmn
	Tx = 0
	Ty = 0
	Tz = -(far + near) / fmn

	return np.array((
		( A, 0., 0., 0.),
		(0.,  B, 0., 0.),
		(0., 0.,  C, 0.),
		(Tx, Ty, Tz, 1.),
	), dtype=np.float32)