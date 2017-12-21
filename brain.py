import pygame, pygame.gfxdraw
import math, random, ctypes, tempfile, datetime
import numpy as np
from colour import Color
from scipy.spatial import Delaunay

pygame.init()
size = (1920,1080)

screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.display.iconify()

now = datetime.datetime.now()

color_steps = 20 
SECOND_COLOR = Color("#FF02F6")
FIRST_COLOR = Color("#FEBF01")
FOURTH_COLOR = Color("#000000")
THIRD_COLOR = Color("#FFFFFF")

BLEED_X = 200
BLEED_Y = 200
CELL_SIZE = 190
VARIANCE = 50
RAND_FN = random.random

done = False

def remap(OldValue, OldMin, OldMax, NewMin, NewMax):
    return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def rgbMap(OldValue):
    return remap(OldValue, 0, 1, 0, 255)

def normalX(OldValue):
    return max(0,remap(OldValue, -BLEED_X, size[0] + BLEED_X, 0.0,1.0))

def normalY(OldValue):
    return max(0,remap(OldValue, -BLEED_Y, size[1] + BLEED_Y, 0.0,1.0))

def centerX(tri):
    return (tri[0][0] + tri[1][0] + tri[2][0]) / 3

def centerY(tri):
    return (tri[0][1] + tri[1][1] + tri[2][1]) / 3

def calculate_gradient(startcolor, endcolor, rows):
    gradient = []
    sr, sg, sb = startcolor
    dr = (endcolor[0] - sr)/(rows-1)
    dg = (endcolor[1] - sg)/(rows-1)
    db = (endcolor[2] - sb)/(rows-1)
    cr, cg, cb = sr, sg, sb
    for r in range(rows):
        gradient.append((cr,cg,cb))
        cr += dr
        cg += dg
        cb += db
        cr = max(min(cr,255),0)
        cg = max(min(cg,255),0)
        cb = max(min(cb,255),0)
    return gradient

def gen_grid(w,h,b_x,b_y,cell_size,variance,rand_fn):
    w = w + b_x
    h = h + b_y
    half_cell = cell_size * 0.5

    points = []
    for i in xrange(-b_x,w,cell_size):
        for j in xrange(-b_y,h,cell_size):
            points.append([int(math.floor((i + half_cell) + (rand_fn() * variance*2 - variance))),
                           int(math.floor((j + half_cell) + (rand_fn() * variance*2 - variance)))])

    return np.array(points)


gradi_X = calculate_gradient(FIRST_COLOR.rgb, SECOND_COLOR.rgb, color_steps)
gradi_Y = calculate_gradient(THIRD_COLOR.rgb, FOURTH_COLOR.rgb, color_steps)

VARIANCE = remap(now.hour, 0, 24, 20, 155)
CELL_SIZE= remap(now.hour, 0, 24, 390, 20)

def genBackground():
    points = gen_grid(size[0],size[1],BLEED_X,BLEED_Y,CELL_SIZE,VARIANCE,RAND_FN)
    tri = Delaunay(points).simplices
    for i in points[tri]:
        currentX = int(normalX(centerX(i)*color_steps))
        currentY = int(normalY(centerY(i)*color_steps))
        xColor = gradi_X[currentX]
        yColor = gradi_Y[currentY]
        intColor = calculate_gradient(xColor,yColor,3)[1]
        colorChoice = map(rgbMap,intColor)
        pygame.gfxdraw.filled_polygon(screen, i, colorChoice)

    pygame.display.flip()

genBackground()
path = tempfile.gettempdir()+"\screenshot.jpeg"
pygame.image.save(screen, path)
ctypes.windll.user32.SystemParametersInfoA(20, 0, path, 0)

pygame.quit()
