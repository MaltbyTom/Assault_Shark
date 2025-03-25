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
        self.rectsurf = pygame.Rect(x,y,width,height)
        self.rectbox = pygame.Rect(x - border, y - border, width + (2 * border), height + (2 * border))
        self.boxcolor = color
        self.rectborder = pygame.Rect(x - border - border2, y - border - border2, width + (2 * border) + (2 * border2), height + (2 * border) + (2 * border2))
        self.bordercolor = color2
        self.row = 0
        self.column = 0
        self.selected = False
        self.selgrow = 2
        self.selborder = pygame.Rect(x - border - border2 - self.selgrow, y - border - border2 - self.selgrow, width + (2 * border) + (2 * border2) + (2 * self.selgrow), height + (2 * border) + (2 * border2) + (2 * self.selgrow))
        self.left = x
        self.top = y
        self.hmod = 0
        self.wmod = 0
        self.partofcboxi = 0
        self.partofrboxi = 0
        #self.surf = pygame.Surface()
        stuff = True

    def draw(self,target):
        if self.selected == False:
            pygame.draw.rect(target, self.bordercolor, self.rectborder)
        else:
            pygame.draw.rect(target, self.bordercolor, self.selborder)
        pygame.draw.rect(target, self.boxcolor, self.rectbox)
        target.blit(self.surf, (self.left + self.wmod, self.top + self.hmod))
        stuff = False
        
    def update(self):
        stuff = False

class Cboxi():

    def __init__(self, cdict, target, source, secondkey):
        super(Cboxi, self).__init__()
        stuff = False
        self.cdict = cdict
        self.target = target
        self.source = source
        self.secondkey = secondkey
    
    def selectnext(self):
        stuff = False
        # Select next boxi down in column of savegames
        newselect = False
        for sel, value in self.source.items():
            if self.source[sel]["my_boxi"].selected == True: 
                selectedrow = self.source[sel]["my_boxi"].row
                if selectedrow < len(self.source) - 1:
                    self.source[sel]["my_boxi"].selected = False
                    self.source[sel]["my_boxi"].draw(self.target)
                    selectedrow += 1
                    newselect = True
        if newselect == True:
            # Selection changed, redraw this column of boxis
            self.target.fill((255, 255, 255))
            for sel, value in self.source.items():
                if self.source[sel]["my_boxi"].row == selectedrow:
                    self.source[sel]["my_boxi"].selected = True
                    selectedboxi = sel
                self.source[sel]["my_boxi"].draw(self.target)
            # Redraw the selected boxi last for highlighting
            self.source[selectedboxi]["my_boxi"].draw(self.target)
    
    def selectprev(self):
        stuff = False
        # Select next boxi up in column of savegames
        newselect = False
        for sel, value in self.source.items():
            if self.source[sel]["my_boxi"].selected == True: 
                selectedrow = self.source[sel]["my_boxi"].row
                if selectedrow > 0:
                    self.source[sel]["my_boxi"].selected = False
                    self.source[sel]["my_boxi"].draw(self.target)
                    selectedrow -= 1
                    newselect = True
        if newselect == True:
            # Selection changed, redraw this column of boxis
            self.target.fill((255, 255, 255))
            for sel, value in self.source.items():
                if self.source[sel]["my_boxi"].row == selectedrow:
                    self.source[sel]["my_boxi"].selected = True
                    selectedboxi = sel
                self.source[sel]["my_boxi"].draw(self.target)
            # Redraw the selected boxi last for highlighting
            self.source[selectedboxi]["my_boxi"].draw(self.target)

class Cboxiscroll():

    def __init__(self, cdict, target, source, secondkey, numvis):
        super(Cboxiscroll, self).__init__()
        stuff = False
        self.cdict = cdict
        self.target = target
        self.source = source
        self.numvis = numvis
        self.firstrow =  0
        self.lastrow = len(source) - 1
        self.firstvis = 0
        self.lastvis = numvis - 1
        self.secondkey = secondkey
    
    def selectnext(self):
        stuff = False
        # Select next boxi down in column of savegames
        newselect = False
        for sel, value in self.source.items():
            if self.source[sel]["my_boxi"].selected == True: 
                selectedrow = self.source[sel]["my_boxi"].row
                # Checks if at last item: Here we check to see if we call a scrolldown event.
                if selectedrow < len(self.source) - 1:
                    self.source[sel]["my_boxi"].selected = False
                    self.source[sel]["my_boxi"].draw(self.target)
                    selectedrow += 1
                    newselect = True
                elif selectedrow < self.lastrow:
                    self.scrolldown
        if newselect == True:
            # Selection changed, redraw this column of boxis
            self.target.fill((255, 255, 255))
            for sel, value in self.source.items():
                if self.source[sel]["my_boxi"].row == selectedrow:
                    self.source[sel]["my_boxi"].selected = True
                    selectedboxi = sel
                self.source[sel]["my_boxi"].draw(self.target)
            # Redraw the selected boxi last for highlighting
            self.source[selectedboxi]["my_boxi"].draw(self.target)
    
    def selectprev(self):
        stuff = False
        # Select next boxi up in column of savegames
        newselect = False
        for sel, value in self.source.items():
            if self.source[sel]["my_boxi"].selected == True: 
                selectedrow = self.source[sel]["my_boxi"].row
                # Checks if at first item: Here we check to see if we call a scrollup event.
                if selectedrow > 0:
                    self.source[sel]["my_boxi"].selected = False
                    self.source[sel]["my_boxi"].draw(self.target)
                    selectedrow -= 1
                    newselect = True
                elif selectedrow > self.firstrow:
                    self.scrollup()
        if newselect == True:
            # Selection changed, redraw this column of boxis
            self.target.fill((255, 255, 255))
            for sel, value in self.source.items():
                if self.source[sel]["my_boxi"].row == selectedrow:
                    self.source[sel]["my_boxi"].selected = True
                    selectedboxi = sel
                self.source[sel]["my_boxi"].draw(self.target)
            # Redraw the selected boxi last for highlighting
            self.source[selectedboxi]["my_boxi"].draw(self.target)

        def scrolldown(self):
            # Update labels top and bottom 
            self.firstvis += 1
            self.lastvis += 1          
            bct = 0 # This iterates through the available source
            visctr = 0 # This counts iterations for filling the visible boxes
            for b, thing in self.source.items():
                self.source[b]["my_boxi"] = None
                if visctr >= self.firstvis and visctr <= self.lastvis:
                    if self.secondkey in self.source[b]:
                        thisboxi = self.cdict[visctr]["boxi"]
                        self.source[b]["my_boxi"] =  thisboxi 
                        self.source[b]["my_boxi"].row = visctr
                        self.cdict[visctr] = {"boxi": thisboxi, "key": b, "picture": self.source[b][self.secondkey]}
                        
                    visctr += 1
                bct += 1
            stuff = False
        
        def scrollup(self):
            # Update labels top and bottom
            stuff = False
    

def boxi(target, thing, destytop, destxleft, border, backcolor, border2, bordercolor, ovhi, ovwid):
    wmod = 0
    hmod = 0
    if ovhi > 0:
        hmod = ((ovhi - thing.height) // 2)
    else:
        ovhi = thing.height
    if ovwid > 0:
        wmod = ((ovwid - thing.width) // 2)
    else:
        ovwid = thing.width
    #if border2 > 0:
        # Border box
    #loadbox = Boxi(destxleft , destytop, thing.width + ovwid, thing.height + ovhi, border, backcolor, border2, bordercolor)
    loadbox = Boxi(destxleft, destytop, ovwid, ovhi, border, backcolor, border2, bordercolor)
    loadbox.surf = thing
    loadbox.hmod = hmod
    loadbox.wmod = wmod
        #pygame.draw.rect(target, bordercolor, loadborder, 0, 2)
    # Inner box
    #loadbox = pygame.Rect(destxleft, destytop, thing.width, thing.height)
    #pygame.draw.rect(target, backcolor, loadbox, 0, 2)
    loadbox.draw(target)
    target.blit(thing, (destxleft + wmod, destytop + hmod))
    return loadbox

def cboxi(target, things, secondkey, destytop, destxleft, border, backcolor, border2, bordercolor, maxh, maxw):
    maxwid = 0
    maxhi = 0
    columnofboxis = {}
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
        if secondkey in things[b]:
            thisboxi = boxi(target, things[b][secondkey], destytop + (bct * (maxhi + border + border2)), destxleft, border, backcolor, border2, bordercolor, maxhi, maxwid)
            things[b]["my_boxi"] =  thisboxi #boxi(target, things[b][secondkey], destytop + (bct * (maxhi + border + border2)), destxleft, border, backcolor, border2, bordercolor, maxhi, maxwid)
            things[b]["my_boxi"].row = bct
            columnofboxis[bct] = {"boxi": thisboxi, "key": b, "picture": things[b][secondkey]}
            #columnofboxis[bct, "boxi"] = thisboxi
            #columnofboxis[bct, "key"] = b
            #columnofboxis[bct, "picture"] = thing
        bct += 1
    createdcboxi = Cboxi(columnofboxis, target, things, secondkey)
    bct = 0
    print(columnofboxis)
    for b in columnofboxis:
        columnofboxis[bct]["boxi"].partofcboxi = createdcboxi
        bct += 1

    print("Modified:")
    print(columnofboxis)
    return createdcboxi
    

def rboxi(target, things, secondkey, destytop, destxleft, border, backcolor, border2, bordercolor, maxh, maxw):
    maxwid = 0
    maxhi = 0
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
            boxi(target, things[b][secondkey], destytop, destxleft + (bct * (maxwid + border + border2)), border, backcolor, border2, bordercolor, maxhi, maxwid)
        bct += 1

def cboxiscroll(target, things, secondkey, destytop, destxleft, border, backcolor, border2, bordercolor, maxh, maxw, numvis):
    # Scrolling column of boxes: numvis is the number of elements to display
    # The corresponding Cboxiscroll class has scrolldown and scrollup events triggered by moving selection
    maxwid = 0
    maxhi = 0
    columnofboxis = {}
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
    visctr = 1 # This counts iterations for filling the visible boxes
    for b, thing in things.items():
        if visctr < numvis:
            if secondkey in things[b]:
                thisboxi = boxi(target, things[b][secondkey], destytop + (bct * (maxhi + border + border2)), destxleft, border, backcolor, border2, bordercolor, maxhi, maxwid)
                things[b]["my_boxi"] =  thisboxi 
                things[b]["my_boxi"].row = bct
                columnofboxis[bct] = {"boxi": thisboxi, "key": b, "picture": things[b][secondkey]}
        bct += 1
        visctr += 1
    createdcboxi = Cboxiscroll(columnofboxis, target, things, secondkey, numvis)
    bct = 0
    print(columnofboxis)
    for b in columnofboxis:
        columnofboxis[bct]["boxi"].partofcboxi = createdcboxi
        bct += 1

    print("Modified:")
    print(columnofboxis)
    return createdcboxi

# Render a dictionary of text items, add "render" key to it containing images of the text
def rendertext(textdic, font, color):
    for key, value in textdic.items():
        textdic[key]["render"] = font.render(key, 1, color)
    return textdic