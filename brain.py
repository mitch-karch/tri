from scipy.spatial import Delaunay
from scipy.ndimage import rotate
from skimage.draw import polygon
from scipy.misc import toimage
from tempfile import gettempdir
from datetime import datetime
from random import random
from colour import Color
from math import floor
import numpy as np
import ctypes

size = (1920,1080,3)

now = datetime.now()

path = gettempdir()+"\screenshot.png"
color_steps = 20 
SECOND_COLOR = Color("#FF02F6")
FIRST_COLOR = Color("#FEBF01")
THIRD_COLOR = Color("#444444")
FOURTH_COLOR = Color("#FFFFFF")
bitmapPhoto = np.zeros(size, 'uint8')

BLEED_X = 200
BLEED_Y = 200
CELL_SIZE = 190
VARIANCE = 50
RAND_FN = random


def remap(OldValue, OldMin, OldMax, NewMin, NewMax):
    """ Preforms a linear remap of OldValue from an OldRange to a New Range 
    
    Keyword Arguments:
    OldValue -- Value to remap
    OldMin   -- Minimum value of old range
    OldMax   -- Maximum value of old range
    NewMin   -- Minimum value of new range
    NewMax   -- Maximum value of new range
    """
    return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def rgbMap(OldValue):
    """ Remaps color percentage (0-1 value) to 8 bit values
    
    Keyword Arguments:
    OldValue -- Integer Value to remap. Should be from 0 to 1
    """
    return remap(OldValue, 0, 1, 0, 255)

def normalX(OldValue):
    """ Remaps X location to percentage
    
    Keyword Arguments:
    OldValue -- Integer Value to remap. Should be from -BLEED_X to BLEED_X + size[0]
    """
    return max(0,remap(OldValue, -BLEED_X, size[0] + BLEED_X, 0.0,1.0))

def normalY(OldValue):
    """ Remaps Y location to percentage
    
    Keyword Arguments:
    OldValue -- Integer Value to remap. Should be from -BLEED_Y to BLEED_Y + size[0]
    """
    return max(0,remap(OldValue, -BLEED_Y, size[1] + BLEED_Y, 0.0,1.0))

def centerX(tri):
    """ Calculates X center of a triangle.
    
    Keyword Arguments:
    tri -- a 2x3 array where each element is a coord of the triangle 
    """
    return (tri[0][0] + tri[1][0] + tri[2][0]) / 3

def centerY(tri):
    """ Calculates Y center of a triangle.
    
    Keyword Arguments:
    tri -- a 2x3 array where each element is a coord of the triangle 
    """
    return (tri[0][1] + tri[1][1] + tri[2][1]) / 3

def calculate_gradient(startcolor, endcolor, transition_steps):
    """ Calculates gradient from startcolor to endcolor with transition_steps 
    
    Keyword Arguments:
    startcolor       -- an rgb tuple of the color to start with
    endcolor         -- an rgb tuple of the color to end with
    transition_steps -- number of colors to end up with total. Must be > 3
    """

    gradient = []
    sr, sg, sb = startcolor
    dr = (endcolor[0] - sr)/(transition_steps-1)
    dg = (endcolor[1] - sg)/(transition_steps-1)
    db = (endcolor[2] - sb)/(transition_steps-1)
    cr, cg, cb = sr, sg, sb
    for r in range(transition_steps):
        gradient.append((cr,cg,cb))
        cr += dr
        cg += dg
        cb += db
        cr = max(min(cr,255),0)
        cg = max(min(cg,255),0)
        cb = max(min(cb,255),0)
    return gradient

def gen_grid(w,h,b_x,b_y,cell_size,variance,rand_fn):
    """ Calculates random 2d dot array
    
    Keyword Arguments:
    w         -- width of grid
    h         -- height of grid
    b_x       -- bleed in the x dimmension
    b_y       -- bleed in the y dimmension
    cell_size -- size of each triangle cell
    variance  -- variance in each placement
    rand_fn   -- function to generate random numbers
    """

    w = w + b_x
    h = h + b_y
    half_cell = cell_size * 0.5

    points = []
    for i in xrange(-b_x,w,cell_size):
        for j in xrange(-b_y,h,cell_size):
            points.append([int(floor((i + half_cell) + (rand_fn() * variance*2 - variance))),
                           int(floor((j + half_cell) + (rand_fn() * variance*2 - variance)))])

    return np.array(points)


VARIANCE = remap(now.hour, 0, 24, 20, 80)
CELL_SIZE= remap(now.hour, 0, 24, 390, 40)
gradi_X = calculate_gradient(FIRST_COLOR.rgb, SECOND_COLOR.rgb, color_steps)
gradi_Y = calculate_gradient(THIRD_COLOR.rgb, FOURTH_COLOR.rgb, color_steps)


def genBackground(width=size[0],height=size[1],b_x=BLEED_X,b_y=BLEED_Y,cell_s=CELL_SIZE,var=VARIANCE,r=RAND_FN):
    global bitmapPhoto
    points = gen_grid(width,height,b_x,b_y,cell_s,var,r)
    tri = Delaunay(points).simplices

    for i in points[tri]:
        currentX, currentY = int(normalX(centerX(i)*color_steps)), int(normalY(centerY(i)*color_steps))
        xColor  , yColor   = gradi_X[currentX], gradi_Y[currentY]
        intColor = calculate_gradient(xColor,yColor,3)[1]
        colorChoice = map(rgbMap,intColor)
        c = i[:,0]
        r = i[:,1]
        rr,cc = polygon(r,c)
        rr = np.clip(rr,0,height-1)
        cc = np.clip(cc,0,width-1)
        bitmapPhoto[cc,rr]=colorChoice

def renderImage():
    genBackground()
    img = toimage(bitmapPhoto, mode='RGB',channel_axis=2).rotate(90,expand=True)
    img.save(path)
    ctypes.windll.user32.SystemParametersInfoA(20, 0, path, 0)

def testImages(C=80, V=40):
    genBackground(cell_s=C, var=V)
    img = toimage(bitmapPhoto, mode='RGB',channel_axis=2).rotate(90,expand=True)
    img.show()

renderImage()
