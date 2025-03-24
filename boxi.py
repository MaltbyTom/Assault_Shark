# Box Library
# Tom Maltby
import pygame



pygame.init()

pygame.font.init()
font15 = pygame.font.Font("fonts/arcade_r.ttf", 15)
font16 = pygame.font.Font("fonts/arcade_r.ttf", 16)
font20 = pygame.font.Font("fonts/arcade_r.ttf", 20)
font30 = pygame.font.Font("fonts/arcade_r.ttf", 30)
font50 = pygame.font.Font("fonts/arcade_r.ttf", 50)
font60 = pygame.font.Font("fonts/arcade_r.ttf", 60)
font75 = pygame.font.Font("fonts/arcade_r.ttf", 75)

def screensetup(sw, sh, sh_nb):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global SCREEN_HEIGHT_NOBOX
    SCREEN_WIDTH = sw
    SCREEN_HEIGHT = sh
    SCREEN_HEIGHT_NOBOX = sh_nb

class Boxi():
    
    def __init__(self, x, y, width, height, border, color, border2, color2):
        super(Boxi, self).__init__()
        self.rectsurf = pygame.rect(x,y,width,height)
        self.rectbox = pygame.rect(x - border, y - border, width + (2 * border), height + (2 * border))
        self.rectbox.color = color
        self.rectborder = pygame.rect(x - border - border2, y - border - border2, width + (2 * border) + (2 * border2), height + (2 * border) + (2 * border2))
        self.rectborder.color = color2
        self.row = 0
        self.column = 0
        self.surf = pygame.Surface()
        stuff = True

    def draw(self,target):
        pygame.draw.rect(target, self.rectborder.color, self.rectborder)
        pygame.draw.rect(target, self.rectbox.color, self.rectbox)
        stuff = False
        
    def update(self):
        stuff = False

def boxi(target, thing, destytop, destxleft, border, backcolor, border2, bordercolor, ovhi, ovwid):
    wmod = 0
    hmod = 0
    if ovhi > 0:
        hmod = ((ovhi - thing.height) // 2)
    if ovwid > 0:
        if ovwid:
            wmod = ((ovwid - thing.width) // 2)
    if border2 > 0:
        # Border box
        loadbox = Boxi(destxleft , destytop, thing.width, thing.height , border, backcolor, border2, bordercolor)
        loadbox.surf = thing
        #pygame.draw.rect(target, bordercolor, loadborder, 0, 2)
    # Inner box
    #loadbox = pygame.Rect(destxleft, destytop, thing.width, thing.height)
    pygame.draw.rect(target, backcolor, loadbox, 0, 2)
    target.blit(thing, (destxleft + wmod, destytop + hmod))

def cboxi(target, things, secondkey, destytop, destxleft, border, backcolor, border2, bordercolor, maxh, maxw):
    maxwid = 0
    maxhi = 0
    #print(things)
    for key, thing in things.items():
        if secondkey in things[key]:
            if things[key][secondkey].width > maxwid:
                maxwid = things[key][secondkey].width
            if things[key][secondkey].height > maxhi:
                maxhi = things[key][secondkey].height
        else:
            if things[key].width > maxwid:
                maxwid = things[key].width
            if things[key].height > maxhi:
                maxhi = things[key].height
    hmod = 0
    bct = 0
    for b, thing in things.items():
        if secondkey in things[key]:
            boxi(target, things[key][secondkey], destytop + (bct * (maxhi + border + border2)), destxleft, border, backcolor, border2, bordercolor, maxhi, maxwid)
        bct += 1

def rboxi(target, things, secondkey, destytop, destxleft, border, backcolor, border2, bordercolor, maxh, maxw):
    maxwid = 0
    maxhi = 0
    #print(things)
    for key, thing in things.items():
        if secondkey in things[key]:
            if things[key][secondkey].width > maxwid:
                maxwid = things[key][secondkey].width
            if things[key][secondkey].height > maxhi:
                maxhi = things[key][secondkey].height
        else:
            if things[key].width > maxwid:
                maxwid = things[key].width
            if things[key].height > maxhi:
                maxhi = things[key].height
    hmod = 0
    bct = 0
    for b, thing in things.items():
        if secondkey in things[key]:
            boxi(target, things[key][secondkey], destytop, destxleft + (bct * (maxwid + border + border2)), border, backcolor, border2, bordercolor, maxhi, maxwid)
        bct += 1
def rendertext(textdic, font, color):
    for key, value in textdic.items():
        textdic[key]["render"] = font.render(key, 1, color)
    return textdic