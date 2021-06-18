import numpy as np

def create_cube(p1=(0,0,0), p2=(1,1,1)):
    p = np.array([[1, 1, 1], [0, 1, 1], [0, 0, 1], [1, 0, 1],
                  [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 0]])
    faces_p = [0, 1, 2, 3, 0, 3, 4, 5, 0, 5, 6, 1, 1, 6, 7, 2, 7, 4, 3, 2, 4, 7, 6, 5]
    vertices = p[faces_p]
    vertices *= np.subtract(p2, p1); vertices += p1
    filled = np.resize(np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32), 6 * (2 * 3))
    filled += np.repeat(4 * np.arange(6, dtype=np.uint32), 6)
    filled = filled.reshape((len(filled) // 3, 3))
    outline = np.resize(np.array([0, 1, 1, 2, 2, 3, 3, 0], dtype=np.uint32), 6 * (2 * 4))
    outline += np.repeat(4 * np.arange(6, dtype=np.uint32), 8)
    return vertices, filled, outline.reshape(-1,2)


def create_plane(width=1, height=1, width_segments=1, height_segments=1,
                 direction='+z'):
    x_grid = width_segments
    y_grid = height_segments

    x_grid1 = x_grid + 1
    y_grid1 = y_grid + 1

    # Positions, normals and texcoords.
    positions = np.zeros(x_grid1 * y_grid1 * 3)
    normals = np.zeros(x_grid1 * y_grid1 * 3)
    texcoords = np.zeros(x_grid1 * y_grid1 * 2)

    y = np.arange(y_grid1) * height / y_grid - height / 2
    x = np.arange(x_grid1) * width / x_grid - width / 2

    positions[::3] = np.tile(x, y_grid1)
    positions[1::3] = -np.repeat(y, x_grid1)

    normals[2::3] = 1

    texcoords[::2] = np.tile(np.arange(x_grid1) / x_grid, y_grid1)
    texcoords[1::2] = np.repeat(1 - np.arange(y_grid1) / y_grid, x_grid1)

    # Faces and outline.
    faces, outline = [], []
    for i_y in range(y_grid):
        for i_x in range(x_grid):
            a = i_x + x_grid1 * i_y
            b = i_x + x_grid1 * (i_y + 1)
            c = (i_x + 1) + x_grid1 * (i_y + 1)
            d = (i_x + 1) + x_grid1 * i_y

            faces.extend(((a, b, d), (b, c, d)))
            outline.extend(((a, b), (b, c), (c, d), (d, a)))

    positions = np.reshape(positions, (-1, 3))
    texcoords = np.reshape(texcoords, (-1, 2))
    normals = np.reshape(normals, (-1, 3))

    faces = np.reshape(faces, (-1, 3)).astype(np.uint32)
    outline = np.reshape(outline, (-1, 2)).astype(np.uint32)

    direction = direction.lower()
    if direction in ('-x', '+x'):
        shift, neutral_axis = 1, 0
    elif direction in ('-y', '+y'):
        shift, neutral_axis = -1, 1
    elif direction in ('-z', '+z'):
        shift, neutral_axis = 0, 2

    sign = -1 if '-' in direction else 1

    positions = np.roll(positions, shift, -1)
    normals = np.roll(normals, shift, -1) * sign
    colors = np.ravel(positions)
    colors = np.hstack((np.reshape(np.interp(colors,
                                             (np.min(colors),
                                              np.max(colors)),
                                             (0, 1)),
                                   positions.shape),
                        np.ones((positions.shape[0], 1))))
    colors[..., neutral_axis] = 0

    vertices = np.zeros(positions.shape[0],
                        [('position', np.float32, 3),
                         ('texcoord', np.float32, 2),
                         ('normal', np.float32, 3),
                         ('color', np.float32, 4)])

    vertices['position'] = positions
    vertices['texcoord'] = texcoords
    vertices['normal'] = normals
    vertices['color'] = colors

    return vertices, faces, outline


def create_box(width=1, height=1, depth=1, width_segments=1, height_segments=1,
               depth_segments=1, planes=None):
    planes = (('+x', '-x', '+y', '-y', '+z', '-z')
              if planes is None else
              [d.lower() for d in planes])

    w_s, h_s, d_s = width_segments, height_segments, depth_segments

    planes_m = []
    if '-z' in planes:
        planes_m.append(create_plane(width, depth, w_s, d_s, '-z'))
        planes_m[-1][0]['position'][..., 2] -= height / 2
    if '+z' in planes:
        planes_m.append(create_plane(width, depth, w_s, d_s, '+z'))
        planes_m[-1][0]['position'][..., 2] += height / 2

    if '-y' in planes:
        planes_m.append(create_plane(height, width, h_s, w_s, '-y'))
        planes_m[-1][0]['position'][..., 1] -= depth / 2
    if '+y' in planes:
        planes_m.append(create_plane(height, width, h_s, w_s, '+y'))
        planes_m[-1][0]['position'][..., 1] += depth / 2

    if '-x' in planes:
        planes_m.append(create_plane(depth, height, d_s, h_s, '-x'))
        planes_m[-1][0]['position'][..., 0] -= width / 2
    if '+x' in planes:
        planes_m.append(create_plane(depth, height, d_s, h_s, '+x'))
        planes_m[-1][0]['position'][..., 0] += width / 2

    positions = np.zeros((0, 3), dtype=np.float32)
    texcoords = np.zeros((0, 2), dtype=np.float32)
    normals = np.zeros((0, 3), dtype=np.float32)

    faces = np.zeros((0, 3), dtype=np.uint32)
    outline = np.zeros((0, 2), dtype=np.uint32)

    offset = 0
    for vertices_p, faces_p, outline_p in planes_m:
        positions = np.vstack((positions, vertices_p['position']))
        texcoords = np.vstack((texcoords, vertices_p['texcoord']))
        normals = np.vstack((normals, vertices_p['normal']))

        faces = np.vstack((faces, faces_p + offset))
        outline = np.vstack((outline, outline_p + offset))
        offset += vertices_p['position'].shape[0]

    vertices = np.zeros(positions.shape[0],
                        [('position', np.float32, 3),
                         ('texcoord', np.float32, 2),
                         ('normal', np.float32, 3),
                         ('color', np.float32, 4)])

    colors = np.ravel(positions)
    colors = np.hstack((np.reshape(np.interp(colors,
                                             (np.min(colors),
                                              np.max(colors)),
                                             (0, 1)),
                                   positions.shape),
                        np.ones((positions.shape[0], 1))))

    vertices['position'] = positions
    vertices['texcoord'] = texcoords
    vertices['normal'] = normals
    vertices['color'] = colors

    return vertices, faces, outline


def create_sphere(rows, cols):
    verts = np.empty((rows+1, cols, 3), dtype=np.float32)

    # compute vertices
    phi = (np.arange(rows+1) * np.pi / rows).reshape(rows+1, 1)
    s = np.sin(phi)
    verts[..., 2] = np.cos(phi)
    th = ((np.arange(cols) * 2 * np.pi / cols).reshape(1, cols))
    th = th + ((np.pi / cols) * np.arange(rows+1).reshape(rows+1, 1))
    verts[..., 0] = s * np.cos(th)
    verts[..., 1] = s * np.sin(th)
    # remove redundant vertices from top and bottom
    verts = verts.reshape((rows+1)*cols, 3)[cols-1:-(cols-1)]

    # compute faces
    faces = np.empty((rows*cols*2, 3), dtype=np.uint32)
    rowtemplate1 = (((np.arange(cols).reshape(cols, 1) +
                      np.array([[1, 0, 0]])) % cols) +
                    np.array([[0, 0, cols]]))
    rowtemplate2 = (((np.arange(cols).reshape(cols, 1) +
                      np.array([[1, 0, 1]])) % cols) +
                    np.array([[0, cols, cols]]))
    for row in range(rows):
        start = row * cols * 2
        faces[start:start+cols] = rowtemplate1 + row * cols
        faces[start+cols:start+(cols*2)] = rowtemplate2 + row * cols
    # cut off zero-area triangles at top and bottom
    faces = faces[cols:-cols]

    # adjust for redundant vertices that were removed from top and bottom
    vmin = cols-1
    faces[faces < vmin] = vmin
    faces -= vmin
    vmax = verts.shape[0]-1
    faces[faces > vmax] = vmax
    return verts, faces

def create_grid_mesh(xs, ys, zs):
    h, w = xs.shape
    vts = np.array([xs, ys, zs], dtype=np.float32)
    did = np.array([[0, 1, 1+w, 0, 1+w, w]], dtype=np.uint32)
    rcs = np.arange(0,w*h-w,w)[:,None] + np.arange(0,w-1,1)
    faces = rcs.reshape(-1,1) + did
    return vts.reshape(3,-1).T.copy(), faces.reshape(-1,3)

def create_ball(o, r, rows=16, cols=16):
    ball = create_sphere(rows, cols)
    ball[0][:] *= r; ball[0][:] += o;
    return ball

def create_balls(os, rs, cs=None, rows=16, cols=16):
    os, rs = np.asarray(os), np.asarray(rs)
    verts, faces = create_sphere(rows, cols)
    if not isinstance(cs, tuple) and not cs is None:
        cs = np.repeat(cs, len(verts))
    offset = np.arange(len(os)) * len(verts)
    verts = verts[None, :, :] * rs[:, None, None]
    verts += os[:, None, :]
    faces = faces[None,:,:] + offset[:,None,None]
    return verts.reshape(-1,3), faces.reshape(-1,3), cs

def create_line(xs, ys, zs):
    vts = np.array([xs, ys, zs], dtype=np.float32)
    fs = np.arange(len(xs))
    return vts.T, np.array([fs[:-1], fs[1:]], np.uint32).T

def mesh_merge(vts, fs, cs):
    cc = [None]*len(vts) if isinstance(cs, tuple) else cs
    def makecolor(c, vts):
        if c is None: return None
        if len(c)==len(vts): return c
        return np.repeat([c], len(vts), axis=0)
    cc = [makecolor(c,v) for c,v in zip(cc, vts)]
    offset = np.cumsum([0]+[len(i) for i in vts[:-1]])
    if not isinstance(cs, tuple): cs = np.vstack(cc)
    for f,s in zip(fs, offset): f += s
    return np.vstack(vts), np.vstack(fs), cs

def create_lines(xs, ys, zs, cs):
    vtsfs = [create_line(x,y,z) for x,y,z in zip(xs,ys,zs)]
    return mesh_merge(*list(zip(*vtsfs)), cs)

def create_bound(p1, p2, nx=1, ny=1, nz=1):
    vts, fs, ls = create_box(1, 1, 1, nx, ny, nz)
    vts['position'] *= np.subtract(p2, p1)
    vts['position'] += p1 - vts['position'].min(axis=0)
    return vts['position'], ls

def create_surface2d(img, sample=1, sigma=0, k=0.3):
    from scipy.ndimage import gaussian_filter
    #start = time()
    img = img[::sample, ::sample].astype(np.float32)
    if sigma>0: img = gaussian_filter(img, sigma)
    xs, ys = np.mgrid[:img.shape[0],:img.shape[1]]
    xs *= sample; ys *= sample
    return create_grid_mesh(xs, ys, img*k)

def create_surface3d(imgs, level, sample=1, sigma=0, step=1):
    from skimage.measure import marching_cubes_lewiner
    from scipy.ndimage import gaussian_filter
    imgs = imgs[::sample,::sample,::sample]
    if sigma>0: imgs = gaussian_filter(imgs, sigma)
    vts, fs, ns, cs =  marching_cubes_lewiner(imgs, level, step_size=step)
    return vts * sample, fs

def build_arrow(v1, v2, rs, re, ts, te, c):
    v = (v2-v1)/np.linalg.norm(v2-v1)
    ss, ee = v1 + v*rs*ts, v2 - v*re*te
    vx = np.cross(v, np.random.rand(3))
    vx /= np.linalg.norm(vx)
    vy = np.cross(vx, v)
    angs = np.linspace(0, np.pi*2, 17)
    vas = np.array([np.cos(angs), np.sin(angs)])
    vxy = np.dot(vas.T, np.array([vx, vy]))
    vts = np.vstack((v1, ss + rs * vxy, ee + re * vxy, v2))
    fs1 = build_pringidx(0, 16, 1)
    fs = build_twringidx(16, 1)
    fs2 = build_pringidx(35, 16, 18)
    face = np.vstack((fs1, fs, fs2))
    ns = np.vstack((-v, vxy, vxy, v)).astype(np.float32)
    cs = (np.ones((len(vts), 3))*c).astype(np.float32)
    return vts.astype(np.float32), face, ns, cs

def build_arrows(v1s, v2s, rss, res, tss, tes, cs):
    if not isinstance(cs, list): cs = [cs] * len(v1s)
    if not isinstance(tss, list): tss = [tss] * len(v1s)
    if not isinstance(tes, list): tes = [tes] * len(v1s)
    if not isinstance(rss, list): rss = [rss] * len(v1s)
    if not isinstance(res, list): res = [res] * len(v1s)
    vtss, fss, nss, css = [], [], [], []
    s = 0
    for v1, v2, rs, re, ts, te, c in zip(v1s, v2s, rss, res, tss, tes, cs):
        if np.linalg.norm(v1-v2) < 0.1: continue
        vv, ff, nn, cc = build_arrow(v1, v2, rs, re, ts, te, c)
        fss.append(ff+s)
        s += len(vv)
        vtss.append(vv)
        nss.append(nn)
        css.append(cc)
    print(np.vstack(vtss).shape, np.vstack(fss).shape, np.vstack(nss).shape, np.vstack(css).shape)
    return np.vstack(vtss), np.vstack(fss), np.vstack(nss), np.vstack(css)
