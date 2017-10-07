Duplicate>{'name': 'gray', 'stack': True}
8-bit>None
Duplicate>{'name': 'watershed', 'stack': True}
Sobel>{'axis': 'both'}
Multiply>{'num': 5.0}
Gaussian>{'sigma': 8.0}
Find Minimum>{'tol': 12, 'mode': False, 'wsd': False}
Watershed With ROI>{'sigma': 0, 'type': 'white line', 'ud': True}
Select None>None
Invert>None
Duplicate>{'name': 'filter', 'stack': True}
Intensity Filter>{'con': '4-connect', 'inten': 'gray', 'max': 0.0, 'min': 0.0, 'mean': 80.0, 'std': 0.0, 'sum': 0.0, 'front': 255, 'back': 0}
Intensity Analysis>{'con': '4-connect', 'inten': 'gray', 'slice': False, 'max': True, 'min': True, 'mean': True, 'center': True, 'var': False, 'std': True, 'sum': True, 'extent': False}
Duplicate>{'name': 'line', 'stack': True}
Binary Outline>None
Binary Dilation>{'w': 3, 'h': 3}
Image Calculator>{'img1': 'gray', 'op': 'max', 'img2': 'line'}