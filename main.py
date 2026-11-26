"""Draw a self-contained illustrated world-news front page for 26 November 2026."""

import math
import os
import struct
import zlib

WIDTH = HEIGHT = 1000
SCALE = 2
PAPER = (247, 242, 231)
INK = (20, 18, 14)
RED = (179, 32, 42)
NIGHT = (42, 57, 68)
SLATE = (105, 122, 130)
FAINT = (199, 190, 174)

# Original single-line vector alphabet. Coordinates use a ten-unit em;
# multiple pen paths are separated by semicolons. Curves are polygonal arcs.
# Every glyph, including lowercase and punctuation, is embedded here.
CAPS = {
 'A':'0,10 2.8,0 5.6,10;1,6.6 4.6,6.6',
 'B':'0,10 0,0 3.2,0 5,1.2 5,3.5 3.2,4.8 0,4.8;3.2,4.8 5.3,6 5.3,8.5 3.4,10 0,10',
 'C':'5.3,1 4,0 1.5,0 0,1.6 0,8.4 1.5,10 4,10 5.3,9',
 'D':'0,10 0,0 2.7,0 5.2,2 5.2,8 2.7,10 0,10',
 'E':'5,0 0,0 0,10 5,10;0,4.8 4.2,4.8',
 'F':'0,10 0,0 5,0;0,4.8 4.2,4.8',
 'G':'5.3,1.3 4,0 1.5,0 0,1.6 0,8.4 1.5,10 5.3,10 5.3,5.5 3,5.5',
 'H':'0,0 0,10;5.2,0 5.2,10;0,5 5.2,5',
 'I':'0,0 4,0;2,0 2,10;0,10 4,10',
 'J':'0,8.3 1.4,10 3.3,10 4.5,8.4 4.5,0',
 'K':'0,0 0,10;5.3,0 0,5 5.5,10',
 'L':'0,0 0,10 5,10',
 'M':'0,10 0,0 3.2,5.7 6.4,0 6.4,10',
 'N':'0,10 0,0 5.5,10 5.5,0',
 'O':'1.5,0 4,0 5.5,1.6 5.5,8.4 4,10 1.5,10 0,8.4 0,1.6 1.5,0',
 'P':'0,10 0,0 3.2,0 5.2,1.5 5.2,3.8 3.2,5.3 0,5.3',
 'Q':'1.5,0 4,0 5.5,1.6 5.5,8.4 4,10 1.5,10 0,8.4 0,1.6 1.5,0;3.2,7.3 6.2,10.6',
 'R':'0,10 0,0 3.2,0 5.2,1.5 5.2,3.8 3.2,5.3 0,5.3;2.8,5.3 5.6,10',
 'S':'5.2,1 3.9,0 1.4,0 0,1.4 0,3.4 1.4,4.6 3.9,5.4 5.2,6.6 5.2,8.6 3.8,10 1.3,10 0,9',
 'T':'0,0 6,0;3,0 3,10',
 'U':'0,0 0,8.2 1.5,10 4,10 5.5,8.2 5.5,0',
 'V':'0,0 2.8,10 5.6,0',
 'W':'0,0 1.6,10 3.8,4.2 6,10 7.6,0',
 'X':'0,0 5.6,10;5.6,0 0,10',
 'Y':'0,0 2.8,5 5.6,0;2.8,5 2.8,10',
 'Z':'0,0 5.5,0 0,10 5.5,10',
 '0':'1.3,0 3.8,0 5.1,1.6 5.1,8.4 3.8,10 1.3,10 0,8.4 0,1.6 1.3,0;0.6,8.8 4.5,1.2',
 '1':'0,2 2.2,0 2.2,10;0,10 4.5,10',
 '2':'0,1.4 1.4,0 3.8,0 5.2,1.4 5.2,3.2 0,10 5.2,10',
 '3':'0,0 5,0 2.5,4.5 4,4.5 5.3,6 5.3,8.5 3.8,10 1.3,10 0,9',
 '4':'4,10 4,0 0,6.6 5.5,6.6',
 '5':'5,0 0,0 0,4.4 3.6,4.4 5.1,5.8 5.1,8.5 3.6,10 1.2,10 0,9',
 '6':'4.8,0 2.2,0 0,3 0,8.5 1.4,10 3.8,10 5.2,8.5 5.2,5.9 3.8,4.5 0,4.5',
 '7':'0,0 5.5,0 1.5,10',
 '8':'1.4,0 3.8,0 5.2,1.4 5.2,3.4 3.8,5 1.4,5 0,3.4 0,1.4 1.4,0;1.4,5 0,6.5 0,8.5 1.4,10 3.8,10 5.2,8.5 5.2,6.5 3.8,5',
 '9':'5.2,5.5 1.4,5.5 0,4.1 0,1.5 1.4,0 3.8,0 5.2,1.5 5.2,7 3,10 0.4,10',
 '.':'0,9.6 0,10', ',':'1,9 0,11.8', ':':'0,3 0,3.4;0,9.6 0,10',
 ';':'1,3 1,3.4;1,9 0,11.8', '!':'0,0 0,6.6;0,9.6 0,10',
 '?':'0,1.3 1.3,0 3.4,0 4.7,1.3 4.7,3.2 2.4,5.2 2.4,6.7;2.4,9.6 2.4,10',
 "'":'0,0 0,2.5', '-':'0,5 4,5', '+':'0,5 5,5;2.5,2.5 2.5,7.5',
 '/':'0,10 4.5,0', '(':'2.5,0 0.5,2.5 0,5 0.5,7.5 2.5,10',
 ')':'0,0 2,2.5 2.5,5 2,7.5 0,10',
 '$':'5,1.6 3.8,0.7 1.5,0.7 0,2 0,3.7 1.4,4.8 3.8,5.5 5,6.6 5,8.2 3.7,9.4 1.3,9.4 0,8.5;2.5,-0.6 2.5,10.7',
 '€':'5.3,1 4,0 1.5,0 0,2 0,8 1.5,10 4,10 5.3,9;0,4 4,4;0,6 3.5,6',
 '%':'0,10 6,0;0,0 1.5,0 1.5,2.5 0,2.5 0,0;4.5,7.5 6,7.5 6,10 4.5,10 4.5,7.5',
 '·':'0,5 0.1,5', '—':'0,5 8,5',
}
LOWER = {
 'a':'0,4 1.2,3 3.3,3 4.5,4.2 4.5,10;4.5,6 1.2,6 0,7.1 0,8.8 1.2,10 3.2,10 4.5,8.8',
 'b':'0,0 0,10;0,4.3 1.4,3 3.3,3 4.7,4.5 4.7,8.5 3.3,10 1.4,10 0,8.7',
 'c':'4.4,3.8 3.3,3 1.3,3 0,4.4 0,8.6 1.3,10 3.3,10 4.4,9.2',
 'd':'4.7,0 4.7,10;4.7,4.3 3.3,3 1.4,3 0,4.5 0,8.5 1.4,10 3.3,10 4.7,8.7',
 'e':'0,6.3 4.6,6.3 4.6,4.5 3.2,3 1.4,3 0,4.5 0,8.5 1.4,10 3.3,10 4.6,9.2',
 'f':'1.2,10 1.2,1.3 2.5,0 4,0;0,3.5 3.5,3.5',
 'g':'4.7,3 4.7,11.4 3.4,12.8 1,12.8;4.7,4.3 3.3,3 1.4,3 0,4.5 0,8 1.4,9.4 3.3,9.4 4.7,8',
 'h':'0,0 0,10;0,4.5 1.5,3 3.2,3 4.6,4.4 4.6,10',
 'i':'0,0.3 0,0.5;0,3.3 0,10',
 'j':'1.5,0.3 1.5,0.5;1.5,3.3 1.5,11.4 0.3,12.8 -1,12.8',
 'k':'0,0 0,10;4.4,3 0,6.8 4.7,10', 'l':'0,0 0,9 1,10',
 'm':'0,10 0,3;0,4.4 1.3,3 2.7,3 4,4.4 4,10;4,4.4 5.3,3 6.7,3 8,4.4 8,10',
 'n':'0,10 0,3;0,4.4 1.4,3 3.1,3 4.6,4.4 4.6,10',
 'o':'1.4,3 3.3,3 4.7,4.4 4.7,8.6 3.3,10 1.4,10 0,8.6 0,4.4 1.4,3',
 'p':'0,13 0,3;0,4.3 1.4,3 3.3,3 4.7,4.5 4.7,8.5 3.3,10 1.4,10 0,8.7',
 'q':'4.7,13 4.7,3;4.7,4.3 3.3,3 1.4,3 0,4.5 0,8.5 1.4,10 3.3,10 4.7,8.7',
 'r':'0,10 0,3;0,4.8 1.8,3 3.6,3',
 's':'4.4,3.7 3.2,3 1.3,3 0,4.1 0,5.3 1.3,6.3 3.2,6.8 4.4,7.8 4.4,9 3.2,10 1.3,10 0,9.3',
 't':'1.3,0.8 1.3,8.8 2.5,10 4,10;0,3.3 3.7,3.3',
 'u':'0,3 0,8.6 1.4,10 3.1,10 4.6,8.6;4.6,3 4.6,10',
 'v':'0,3 2.4,10 4.8,3', 'w':'0,3 1.7,10 3.6,5 5.5,10 7.2,3',
 'x':'0,3 4.6,10;4.6,3 0,10', 'y':'0,3 2.5,10;5,3 1.5,12.8 0,12.8',
 'z':'0,3 4.5,3 0,10 4.5,10',
}
FONT = {}
for char, data in list(CAPS.items()) + list(LOWER.items()):
    paths = [[tuple(map(float, pt.split(','))) for pt in path.split()]
             for path in data.split(';')]
    FONT[char] = (paths, max(x for path in paths for x, y in path) + 2.1)
FONT[' '] = ([], 3.5)


class Canvas:
    def __init__(self):
        self.w = WIDTH * SCALE
        self.h = HEIGHT * SCALE
        self.data = bytearray(bytes(PAPER) * self.w * self.h)

    def rect(self, x, y, w, h, color):
        x0, x1 = max(0, round(x*SCALE)), min(self.w, round((x+w)*SCALE))
        y0, y1 = max(0, round(y*SCALE)), min(self.h, round((y+h)*SCALE))
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1-x0)
        for yy in range(y0, y1):
            i = (yy*self.w+x0)*3
            self.data[i:i+len(row)] = row

    def polygon(self, points, color):
        points = [(x*SCALE, y*SCALE) for x, y in points]
        lo = max(0, math.floor(min(y for x, y in points)))
        hi = min(self.h, math.ceil(max(y for x, y in points)))
        for yy in range(lo, hi):
            sy = yy + .5
            xs = []
            for i, (x1, y1) in enumerate(points):
                x2, y2 = points[(i+1) % len(points)]
                if (y1 <= sy < y2) or (y2 <= sy < y1):
                    xs.append(x1+(sy-y1)*(x2-x1)/(y2-y1))
            xs.sort()
            for i in range(0, len(xs)-1, 2):
                a = max(0, math.ceil(xs[i]-.5))
                b = min(self.w, math.ceil(xs[i+1]-.5))
                if b > a:
                    j = (yy*self.w+a)*3
                    self.data[j:j+(b-a)*3] = bytes(color)*(b-a)

    def circle(self, x, y, r, color):
        cx, cy, rr = x*SCALE, y*SCALE, r*SCALE
        for yy in range(max(0, math.floor(cy-rr)), min(self.h, math.ceil(cy+rr))):
            half = math.sqrt(max(0, rr*rr-(yy+.5-cy)**2))
            a, b = max(0, math.ceil(cx-half-.5)), min(self.w, math.ceil(cx+half-.5))
            if b > a:
                i = (yy*self.w+a)*3
                self.data[i:i+(b-a)*3] = bytes(color)*(b-a)

    def line(self, a, b, width=1, color=INK):
        x, y = a
        xx, yy = b
        d = math.hypot(xx-x, yy-y)
        if not d:
            self.circle(x, y, width/2, color)
            return
        nx, ny = -(yy-y)*width/(2*d), (xx-x)*width/(2*d)
        self.polygon([(x+nx,y+ny),(xx+nx,yy+ny),(xx-nx,yy-ny),(x-nx,y-ny)], color)
        self.circle(x, y, width/2, color)
        self.circle(xx, yy, width/2, color)

    def path(self, points, width=1, color=INK):
        for a, b in zip(points, points[1:]):
            self.line(a, b, width, color)

    def text(self, text, x, y, size, bold=False, color=INK, condensed=1.0):
        unit = size/10
        pen = x
        weight = (1.55 if bold else .78) * unit
        for char in text:
            paths, advance = FONT[char]
            for path in paths:
                self.path([(pen+px*unit*condensed, y+py*unit) for px, py in path], weight, color)
            pen += advance*unit*condensed
        return pen

    def pixels(self):
        # Exact 2x2 box filter; antialiasing does not depend on external libraries.
        result = bytearray(WIDTH*HEIGHT*3)
        src, stride = self.data, self.w*3
        for y in range(HEIGHT):
            top = y*2*stride
            for x in range(WIDTH):
                i, j = top+x*6, (y*WIDTH+x)*3
                for c in range(3):
                    result[j+c] = (src[i+c]+src[i+3+c]+src[i+stride+c]+src[i+stride+3+c]+2)//4
        return result


def text_width(text, size, condensed=1):
    return sum(FONT[c][1] for c in text)*size/10*condensed


def centered(c, text, y, size, bold=False, color=INK, condensed=1):
    c.text(text, (WIDTH-text_width(text,size,condensed))/2, y, size, bold, color, condensed)


def lines(c, content, x, y, size, leading, bold=False, color=INK, condensed=1):
    for i, text in enumerate(content):
        c.text(text,x,y+i*leading,size,bold,color,condensed)


def wrapped(c, text, x, y, width, size, leading, bold=False, color=INK):
    words, row, rows = text.split(), '', []
    for word in words:
        trial = (row+' '+word).strip()
        if text_width(trial,size) > width and row:
            rows.append(row)
            row = word
        else:
            row = trial
    if row:
        rows.append(row)
    lines(c, rows,x,y,size,leading,bold,color)
    return y+(len(rows)-1)*leading+size


def rule(c,y,x=36,end=964,color=INK,width=.8):
    c.line((x,y),(end,y),width,color)


def kicker(c,text,x,y):
    c.text(text,x,y,12,True,RED)


def starburst(c,x,y,r):
    for a in range(0,360,45):
        angle=math.radians(a)
        c.line((x+math.cos(angle)*r*.25,y+math.sin(angle)*r*.25),
               (x+math.cos(angle)*r,y+math.sin(angle)*r),1.5,PAPER)
    c.circle(x,y,3,PAPER)
    c.circle(x,y,1,RED)


def riyadh_scene(c):
    x,y,w,h = 36,328,576,154
    c.rect(x,y,w,h,NIGHT)
    # Moon, three ballistic paths, and two interceptor trails.
    c.circle(568,349,10,PAPER)
    c.circle(573,345,9,NIGHT)
    for pts in [((72,446),(143,350),(217,366)),((296,449),(320,342),(398,359)),((477,448),(472,358),(440,372))]:
        a,b,d=pts
        curve=[]
        for i in range(45):
            t=i/44
            curve.append(((1-t)**2*a[0]+2*(1-t)*t*b[0]+t*t*d[0],
                          (1-t)**2*a[1]+2*(1-t)*t*b[1]+t*t*d[1]))
        c.path(curve,1.5,SLATE)
    for a,b in [((123,448),(217,366)),((353,447),(398,359)),((543,447),(440,372))]:
        c.line(a,b,2.2,PAPER)
        c.line(a,((a[0]+b[0])*.5,(a[1]+b[1])*.5),4,SLATE)
        starburst(c,*b,12)
    # City silhouette, including a tall divided crown and industrial stacks.
    c.rect(36,450,576,32,INK)
    buildings=[(39,430,27,25),(72,440,18,18),(97,423,22,32),(129,433,35,22),
               (174,417,19,38),(202,438,31,20),(245,428,26,29),(281,413,24,43),
               (318,439,34,19),(365,426,20,30)]
    for bx,by,bw,bh in buildings:
        c.rect(bx,by,bw,bh,INK)
    c.polygon([(157,450),(164,409),(170,400),(177,409),(184,450)],INK)
    c.polygon([(166,409),(170,416),(174,409)],NIGHT)
    for bx in (423,439,590):
        c.rect(bx,409 if bx!=590 else 419,5,43,INK)
        c.line((bx,411),(bx+5,411),2,RED)
    for bx,bw in [(458,46),(511,58)]:
        c.rect(bx,433,bw,20,SLATE)
        c.polygon([(bx,433),(bx+8,428),(bx+bw-8,428),(bx+bw,433)],SLATE)
        c.line((bx,440),(bx+bw,440),1,INK)
    c.text('RAS TANURA',469,466,8.6,True,PAPER)
    c.text('RIYADH / NIGHT SKY',48,335,8.2,False,PAPER)


def market(c):
    x=645
    rule(c,370,x,964,FAINT)
    c.text('PARTNERS',x,384,12,True)
    c.text('14',922,379,27,True,RED)
    c.text('incl. China, EU, Japan, India',x,404,12.1)
    rule(c,425,x,964,FAINT)
    c.text('BRENT',x,439,14,True)
    c.text('$91.19',739,436,19,True)
    c.text('+0.61%',863,441,13.5,True,RED)
    c.path([(950,451),(950,436),(945,441),(950,436),(955,441)],1.5,RED)
    rule(c,466,x,964,FAINT)
    c.text('NVIDIA',x,480,14,True)
    c.text('-3.9%',856,477,21,True)
    c.path([(950,480),(950,495),(945,490),(950,495),(955,490)],1.5,INK)


def tanker(c,x,y):
    c.rect(x,y+17,80,17,INK)
    c.polygon([(x+83,y+15),(x+98,y+15),(x+108,y+26),(x+108,y+35),(x+83,y+35)],INK)
    c.rect(x+87,y+19,9,8,PAPER)
    c.circle(x+13,y+36,7,INK)
    c.circle(x+69,y+36,7,INK)
    c.circle(x+97,y+36,7,INK)
    c.line((x-4,y+44),(x+114,y+44),1,FAINT)
    for dx,hh in [(12,23),(31,34),(51,25),(69,39)]:
        c.polygon([(x+dx-9,y+17),(x+dx-8,y+5),(x+dx-3,y+8),(x+dx+1,y-hh+17),
                   (x+dx+8,y-1),(x+dx+7,y+17)],RED)
        c.polygon([(x+dx-3,y+16),(x+dx+2,y+3),(x+dx+5,y+16)],PAPER)


def jet(c,x,y,s=1,angle=0,color=INK):
    pts=[(0,-16),(3,-5),(14,5),(14,8),(3,5),(3,13),(7,17),(7,19),(0,16),
         (-7,19),(-7,17),(-3,13),(-3,5),(-14,8),(-14,5),(-3,-5)]
    a=math.radians(angle)
    c.polygon([(x+s*(px*math.cos(a)-py*math.sin(a)),y+s*(px*math.sin(a)+py*math.cos(a))) for px,py in pts],color)


def airbase(c,x,y):
    c.line((x-15,y+24),(x+140,y+24),1,FAINT)
    # Smoke trails the tilted jet's tail, clear of the body copy below.
    for dx,dy,r in [(64,18,4),(71,17,3.2),(76,14,2.5),(80,11,1.7)]:
        c.circle(x+dx,y+dy,r,(139,139,134))
    for i in range(5):
        jet(c,x+i*28,y,.60,25 if i==3 else 0,RED if i==3 else INK)


def launcher(c,x,y):
    c.rect(x,y+27,104,14,INK)
    for dx in (11,33,71,93):
        c.circle(x+dx,y+43,6,INK)
    c.polygon([(x+83,y+16),(x+97,y+16),(x+106,y+27),(x+83,y+27)],INK)
    c.rect(x+87,y+20,9,6,PAPER)
    c.polygon([(x+9,y+25),(x+63,y-14),(x+73,y-17),(x+69,y-7),(x+17,y+32)],INK)
    c.line((x+19,y+21),(x+60,y-9),2,PAPER)
    c.polygon([(x+60,y-12),(x+73,y-17),(x+69,y-5)],RED)
    c.line((x-4,y+51),(x+114,y+51),1,FAINT)


def station(c,x,y):
    points=[]
    for i in range(65):
        a=i*math.tau/64
        points.append((x+math.cos(a)*67,y+math.sin(a)*19+math.cos(a)*13))
    c.path(points,.8,SLATE)
    c.line((x-30,y+13),(x+29,y-12),5,INK)
    c.line((x-7,y-16),(x+7,y+16),6,INK)
    for dx in (-1,1):
        for dy in (-1,1):
            bx=x+dx*34
            by=y+dy*12
            c.polygon([(bx-16,by-7),(bx+10,by-15),(bx+15,by-2),(bx-11,by+6)],NIGHT)
            c.line((bx-3,by-11),(bx+2,by+2),.8,PAPER)
            c.line((bx-14,by),(bx+13,by-8),.8,PAPER)
    c.circle(x+54,y-3,3,RED)


def masthead(c):
    rule(c,28,width=2)
    c.text('GLOBAL BRIEFING',36,38,9.7,True)
    right='WORLD EDITION / 26.11.2026'
    c.text(right,964-text_width(right,9.7),38,9.7,True)
    centered(c,'THE WORLD TODAY',63,59,True,condensed=1.34)
    rule(c,136,width=1.5)
    centered(c,'THURSDAY 26 NOVEMBER 2026',148,22.5,True,RED)
    centered(c,"The day's world news in one page",181,12.4)
    rule(c,203,width=1.5)


def lead_stories(c):
    # The masthead uses 203 px; the content grid below begins at 219.
    kicker(c,'RIYADH',36,215)
    lines(c,['SAUDI AIR DEFENCES','DESTROY HOUTHI MISSILES','FIRED AT RIYADH'],
          36,234,25.8,31,True,condensed=1.20)
    riyadh_scene(c)
    wrapped(c,'Interceptors knocked out the salvo over the capital. Houthi attacks also hit Saudi ports and the Ras Tanura refinery.',
            36,495,576,13.8,18)
    c.line((628,217),(628,529),.7,FAINT)
    kicker(c,'WASHINGTON',645,218)
    lines(c,['US PROPOSES NEW','TARIFFS ON 14','TRADING PARTNERS'],645,242,24,32,True,condensed=.95)
    market(c)
    wrapped(c,'Markets rattled as the plan lands; oil up, chip shares down.',645,511,319,11.7,15)
    rule(c,547,width=1.3)


def supporting_panels(c):
    c.line((500,559),(500,799),.7,FAINT)
    kicker(c,'CAIRO',36,561)
    lines(c,['FUEL-TANKER FIRE','KILLS AT LEAST 31'],36,583,20.3,25,True)
    tanker(c,361,585)
    wrapped(c,'A tanker caught fire on the ring road; about 21 people were hurt.',
            36,642,438,12.5,16)
    kicker(c,'UKRAINE',520,561)
    lines(c,['STRIKE ON RUSSIAN AIRBASE','DAMAGES 5 JETS'],520,583,19.1,25,True,condensed=.90)
    airbase(c,817,616)
    wrapped(c,'Savasleyka airbase, east of Moscow: 3 MiG-31 and 2 Su-34 hit.',
            520,644,444,12.4,16)
    rule(c,680,color=FAINT)
    kicker(c,'PYONGYANG',36,694)
    lines(c,['KIM VOWS WIDER TACTICAL-','NUKE DEPLOYMENT'],36,715,18.4,24,True,condensed=.92)
    launcher(c,358,715)
    wrapped(c,"Kim Jong Un says the arsenal's role should grow.",36,776,438,12.4,16)
    kicker(c,'SPACE',520,694)
    lines(c,['FIRST FOREIGN ASTRONAUT','BOARDS TIANGONG'],520,715,18.4,24,True,condensed=.90)
    station(c,897,746)
    wrapped(c,"Pakistan's Muhammad Zeeshan Ali is the first foreign astronaut aboard China's station. The FCC also cleared SpaceX's plan for up to 1,000,000 satellites.",
            520,769,444,11.0,14)
    rule(c,818,width=1.3)


CARDS = [
 ('SPAIN VOTES SUNDAY',"Snap election; the right is favoured to end Sanchez's 8 years."),
 ('EU CLASH OVER UKRAINE LOAN','Leaders split in Brussels over a 45bn euro package.'),
 ('NETANYAHU CASE TWIST','Judges suggest dropping the bribery charge.'),
 ('LONDON TUBE STRIKE','Underground walkout runs Thursday to Friday.'),
 ('13 MINERS TRAPPED IN BOGOR','Rescuers race a flooded illegal gold mine in Indonesia.'),
 ('HONG KONG REMEMBERS','One year since the fire that killed 168.'),
 ('US TELLS CITIZENS: LEAVE IRAN','Warning issued as war fears grow.'),
 ('LILLE 2-1 BAYERN','Champions League upset of the night.'),
]


def regional_cards(c):
    for i,(headline,body) in enumerate(CARDS):
        col,row=i%4,i//4
        x,y=36+col*237,830+row*64
        if col:
            c.line((x-12,y-1),(x-12,y+53),.6,FAINT)
        end=wrapped(c,headline,x,y,213,11.8,15,True)
        # Enlarge only cards whose existing line breaks remain identical.
        body_size = 11.0 if i in (1,2,3,5,7) else 10.6
        wrapped(c,body,x,end+8,213,body_size,13)
    rule(c,887,color=FAINT,width=.6)


def numbers_and_footer(c):
    c.rect(36,950,928,26,RED)
    c.text('THE DAY IN NUMBERS',46,958,9.7,True,PAPER)
    c.line((175,956),(175,970),.6,PAPER)
    c.text('14 tariff partners · 31 dead in Cairo · 5 jets damaged · 1,000,000 satellites cleared · $91.19 Brent · 13 miners trapped',
           186,957,11.8,False,PAPER,condensed=.92)
    # The single red band carries the complete fact strip; footer is separate.
    rule(c,980,width=.6)
    c.text('All stories as reported on Thursday 26 November 2026.',36,984,7.4)
    c.text('THE WORLD TODAY',856,984,7.4,True)


def write_png(path,pixels):
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    # Filter 1 (Sub) markedly reduces flat artwork and repeated letter strokes.
    rows=bytearray()
    stride=WIDTH*3
    for y in range(HEIGHT):
        rows.append(1)
        row=pixels[y*stride:(y+1)*stride]
        rows.extend((value-(row[i-3] if i>=3 else 0))&255 for i,value in enumerate(row))
    data=(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',WIDTH,HEIGHT,8,2,0,0,0))+
          chunk(b'IDAT',zlib.compress(rows,9))+chunk(b'IEND',b''))
    with open(path,'wb') as file:
        file.write(data)


def main():
    c=Canvas()
    masthead(c)
    lead_stories(c)
    supporting_panels(c)
    regional_cards(c)
    numbers_and_footer(c)
    output=os.environ.get('MAKEFUN_OUTPUT_DIR','/output')
    os.makedirs(output,exist_ok=True)
    write_png(os.path.join(output,'entry.png'),c.pixels())


if __name__=='__main__':
    main()
