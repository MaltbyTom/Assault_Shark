# Box Library
# Tom Maltby
import pygame



pygame.init()

pygame.font.init()
font8 = pygame.font.Font("fonts/arcade_r.ttf", 8)
font15 = pygame.font.Font("fonts/arcade_r.ttf", 15)
font16 = pygame.font.Font("fonts/arcade_r.ttf", 16)
font20 = pygame.font.Font("fonts/arcade_r.ttf", 20)
font30 = pygame.font.Font("fonts/arcade_r.ttf", 30)
font50 = pygame.font.Font("fonts/arcade_r.ttf", 50)
font60 = pygame.font.Font("fonts/arcade_r.ttf", 60)
font75 = pygame.font.Font("fonts/arcade_r.ttf", 75)

# Define Colors
RED = pygame.Color("red")
BLUE = pygame.Color("blue")
GREEN = pygame.Color("green")
GRAY = pygame.Color("gray")
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
YELLOW = pygame.Color("yellow")

def screensetup(sw, sh, sh_nb):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global SCREEN_HEIGHT_NOBOX
    SCREEN_WIDTH = sw
    SCREEN_HEIGHT = sh
    SCREEN_HEIGHT_NOBOX = sh_nb

regcontrols = []

def drawregcontrols():
    for control in regcontrols:
        control.draw()

class Boxi():
    
    def __init__(self, x, y, width, height, border, color, border2, color2, *args, **kwargs):
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
        self.height = height
        self.width = width
        self.border = border
        self.border2 = border2
        self.hmod = 0
        self.wmod = 0
        self.partofcboxi = 0
        self.partofrboxi = 0
        self.thing = None
        if len(args) > 0:
            self.target = args[0]
        else:
            self.target = None
        #self.surf = pygame.Surface()
        stuff = True

    def draw(self):
        hmod = (self.height - self.thing.height) // 2
        wmod = ((self.width - self.thing.width) // 2)
        self.wmod = wmod
        self.hmod = hmod
        if self.selected == False:
            pygame.draw.rect(self.target, self.bordercolor, self.rectborder)
        else:
            pygame.draw.rect(self.target, self.bordercolor, self.selborder)
        pygame.draw.rect(self.target, self.boxcolor, self.rectbox)
        self.target.blit(self.thing, (self.left + self.wmod, self.top + self.hmod))
        stuff = False

    
    def register(self):
        regcontrols.append(self)

class Cboxi():

    def __init__(self, cdict, target, source, secondkey):
        super(Cboxi, self).__init__()
        stuff = False
        self.cdict = cdict
        self.target = target
        self.source = source
        self.secondkey = secondkey
        self.cdict[0]["boxi"].selected = True
        self.selectedrow = 0
        self.cdict[0]["boxi"].draw()

    def draw(self):
        for sel, value in self.cdict.items():
            self.cdict[sel]["boxi"].draw()
        # Redraw the selected boxi last for highlighting
        self.cdict[self.selectedrow]["boxi"].draw()
   
    def register(self):
        regcontrols.append(self)       
    
    def selectnext(self):
        stuff = False
        # Select next boxi down in column of savegames
        newselect = False
        for sel, value in self.source.items():
            if self.source[sel]["my_boxi"].selected == True: 
                selectedrow = self.source[sel]["my_boxi"].row
                if selectedrow < len(self.source) - 1:
                    self.source[sel]["my_boxi"].selected = False
                    self.source[sel]["my_boxi"].draw()
                    selectedrow += 1
                    newselect = True
        if newselect == True:
            # Selection changed, redraw this column of boxis
            for sel, value in self.source.items():
                if self.source[sel]["my_boxi"].row == selectedrow:
                    self.source[sel]["my_boxi"].selected = True
                    selectedboxi = sel
                self.source[sel]["my_boxi"].draw(self.target)
            # Redraw the selected boxi last for highlighting
            self.source[selectedboxi]["my_boxi"].draw(self.target)
        self.selectedrow = selectedrow
    
    def selectprev(self):
        stuff = False
        # Select next boxi up in column of savegames
        newselect = False
        for sel, value in self.source.items():
            if self.source[sel]["my_boxi"].selected == True: 
                selectedrow = self.source[sel]["my_boxi"].row
                if selectedrow > 0:
                    self.source[sel]["my_boxi"].selected = False
                    self.source[sel]["my_boxi"].draw()
                    selectedrow -= 1
                    newselect = True
        if newselect == True:
            # Selection changed, redraw this column of boxis
            for sel, value in self.source.items():
                if self.source[sel]["my_boxi"].row == selectedrow:
                    self.source[sel]["my_boxi"].selected = True
                    selectedboxi = sel
                self.source[sel]["my_boxi"].draw()
            # Redraw the selected boxi last for highlighting
            self.source[selectedboxi]["my_boxi"].draw()
        self.selectedrow = selectedrow

class Cboxiscroll():

    def __init__(self, cdict, target, source, secondkey, numvis, tabord):
        super(Cboxiscroll, self).__init__()
        stuff = False
        self.tabord = tabord
        self.cdict = cdict
        self.target = target
        self.source = source
        self.numvis = numvis
        self.firstrow =  0
        self.lastrow = len(source) - 1
        self.firstvis = 0
        self.lastvis = numvis - 1
        self.secondkey = secondkey
        self.selectedrow = 0
        self.top = self.cdict[0]["boxi"].top
        self.left = self.cdict[0]["boxi"].left
        self.bottom = self.top + (numvis * (self.cdict[0]["boxi"].height + self.cdict[0]["boxi"].border + self.cdict[0]["boxi"].border2))
        self.cdict[0]["boxi"].selected = True
        self.cdict[0]["boxi"].draw()
        self.displayfont = font8
        self.displayboxi1 = None
        self.displaykey1 = None
        self.displayboxi2 = None
        self.displaykey2 = None
        self.displayboxi3 = None
        self.displaykey3 = None
        self.displaycolor = BLACK       
        bct = 0 # This iterates through the available source
        visctr = 0 # This counts iterations for filling the visible boxes
        for b, thing in self.source.items():
            self.source[b]["my_boxi"] = None
            if bct >= self.firstvis and bct <= self.lastvis:
                if self.secondkey in self.source[b]:
                    thisboxi = self.cdict[visctr]["boxi"]
                    self.source[b]["my_boxi"] = thisboxi 
                    self.source[b]["my_boxi"].row = visctr
                    self.cdict[visctr] = {"boxi": thisboxi, "key": b, "bct": bct, "picture": self.source[b][self.secondkey]}
                    thisboxi.thing = self.source[b][self.secondkey]
                visctr += 1
            bct += 1


    def draw(self):
        for sel, value in self.cdict.items():
            self.cdict[sel]["boxi"].draw()
        # Redraw the selected boxi last for highlighting
        self.cdict[self.selectedrow]["boxi"].draw()
        # Calculate and draw the scrolling labels if all items not displayed
        # Other display options could go here
        if self.numvis < self.lastrow:
            numup = self.firstvis
            numdown = self.lastrow - self.lastvis
            if numup > 0:
                upcol = GREEN
            else:
                upcol = GRAY
            renderup = font8.render(str(numup) + " more above", 1, upcol)
            if numdown > 0:
                downcol = GREEN
            else:
                downcol = GRAY
            renderdown = font8.render(str(numdown) + " more below", 1, downcol)
            self.target.blit(renderup, (self.left, self.top - 12))
            self.target.blit(renderdown, (self.left, self.bottom + 2))
        # Update optional displays of other keys:
        if self.displayboxi1 and self.displaykey1:
            dispkey = self.cdict[self.selectedrow]["key"]
            dispval = self.source[dispkey][self.displaykey1]
            self.displayboxi1.thing = rendertext(str(self.displaykey1) +":  "+ str(dispval), self.displayfont, self.displaycolor)
            self.displayboxi1.draw()


    def register(self):
        regcontrols.append(self)
    
    def selectnext(self):
        stuff = False
        # Select next boxi down in column
        # If slippage
        if self.cdict[self.selectedrow]["boxi"].selected == False:
            for sel, value in self.cdict.items():
                if self.cdict[sel]["boxi"].selected == True: 
                    self.selectedrow = self.cdict[sel]["boxi"].row
        # Checks if at last displayed item: if not, move selection down
        if self.selectedrow < self.numvis - 1 and self.selectedrow < self.lastrow:
            self.cdict[self.selectedrow]["boxi"].selected = False
            self.selectedrow += 1
            self.cdict[self.selectedrow]["boxi"].selected = True
        # Here we check to see if we call a scrolldown event.
        elif self.cdict[self.selectedrow]["bct"] < self.lastrow:
            self.scrolldown()
        # Selection changed, redraw this column of boxis
        self.draw()

    def selectprev(self):
        # Select next boxi up in column
        # If slippage
        if self.cdict[self.selectedrow]["boxi"].selected == False:
            for sel, value in self.cdict.items():
                if self.cdict[sel]["boxi"].selected == True: 
                    self.selectedrow = self.cdict[sel]["boxi"].row
        # Checks if at last displayed item: if not, move selection down
        if self.selectedrow > 0:
            self.cdict[self.selectedrow]["boxi"].selected = False
            self.selectedrow -= 1
            self.cdict[self.selectedrow]["boxi"].selected = True
        # Here we check to see if we call a scrolldown event.
        elif self.cdict[self.selectedrow]["bct"] > self.firstrow:
            self.scrollup()
        # Selection changed, redraw this column of boxis
        self.draw()

    def scrolldown(self):
        # Update labels top and bottom 
        self.firstvis += 1
        self.lastvis += 1          
        bct = 0 # This iterates through the available source
        visctr = 0 # This counts iterations for filling the visible boxes
        for b, thing in self.source.items():
            self.source[b]["my_boxi"] = None
            if bct >= self.firstvis and bct <= self.lastvis:
                if self.secondkey in self.source[b]:
                    thisboxi = self.cdict[visctr]["boxi"]
                    self.source[b]["my_boxi"] = thisboxi 
                    self.source[b]["my_boxi"].row = visctr
                    self.cdict[visctr] = {"boxi": thisboxi, "key": b, "bct": bct, "picture": self.source[b][self.secondkey]}
                    thisboxi.thing = self.source[b][self.secondkey]
                visctr += 1
            bct += 1
        self.draw()
    
    def scrollup(self):
        # Update labels top and bottom 
        self.firstvis -= 1
        self.lastvis -= 1          
        bct = 0 # This iterates through the available source
        visctr = 0 # This counts iterations for filling the visible boxes
        for b, thing in self.source.items():
            self.source[b]["my_boxi"] = None
            if bct >= self.firstvis and bct <= self.lastvis:
                if self.secondkey in self.source[b]:
                    thisboxi = self.cdict[visctr]["boxi"]
                    self.source[b]["my_boxi"] = thisboxi 
                    self.source[b]["my_boxi"].row = visctr
                    self.cdict[visctr] = {"boxi": thisboxi, "key": b, "bct": bct, "picture": self.source[b][self.secondkey]}
                    thisboxi.thing = self.source[b][self.secondkey]
                visctr += 1
            bct += 1
        self.draw()

def boxi(target, thing, destytop, destxleft, border, backcolor, border2, bordercolor, ovhi, ovwid, *args, **kwargs ):
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
    loadbox = Boxi(destxleft, destytop, ovwid, ovhi, border, backcolor, border2, bordercolor)
    loadbox.surf = thing
    loadbox.hmod = hmod
    loadbox.wmod = wmod
    loadbox.thing = thing
    loadbox.target = target
    loadbox.draw()
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
            things[b]["my_boxi"] =  thisboxi 
            things[b]["my_boxi"].row = bct
            columnofboxis[bct] = {"boxi": thisboxi, "key": b, "picture": things[b][secondkey]}
        bct += 1
    createdcboxi = Cboxi(columnofboxis, target, things, secondkey)
    bct = 0
    for b in columnofboxis:
        columnofboxis[bct]["boxi"].partofcboxi = createdcboxi
        bct += 1
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

def cboxiscroll(target, things, secondkey, destytop, destxleft, border, backcolor, border2, bordercolor, maxh, maxw, numvis, *args, **kwargs):
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
    visctr = 0 # This counts iterations for filling the visible boxes
    for b, thing in things.items():
        if visctr < numvis:
            if secondkey in things[b]:
                thisboxi = boxi(target, things[b][secondkey], destytop + (bct * (maxhi + border + border2)), destxleft, border, backcolor, border2, bordercolor, maxhi, maxwid)
                things[b]["my_boxi"] =  thisboxi 
                things[b]["my_boxi"].row = bct
                columnofboxis[bct] = {"boxi": thisboxi, "key": b, "bct": bct, "picture": things[b][secondkey]}
        bct += 1
        visctr += 1
    if "tabord" in kwargs:
        tab = kwargs["tabord"]
    else:
        tab = None
    createdcboxi = Cboxiscroll(columnofboxis, target, things, secondkey, numvis, tab)
    
    bct = 0
    for b in columnofboxis:
        columnofboxis[bct]["boxi"].partofcboxi = createdcboxi
        bct += 1

    if numvis < len(things):    
        # Add scrolling labels if more items than displayed
        numup = 0
        numdown = len(things) - numvis
        renderup = font8.render(str(numup) + " more above", 1, GRAY)
        if numdown > 0:
            downcol = GREEN
        else:
            downcol = GRAY
        renderdown = font8.render(str(numdown) + " more below", 1, GREEN)
        
        target.blit(renderup, (destxleft, destytop - 12))
        target.blit(renderdown, (destxleft, destytop + (bct * (maxhi + border + border2)) + 2))
    
    # Connect optional display boxis
    if "displayfont" in kwargs:
        createdcboxi.displayfont = kwargs["displayfont"]

    if "displayboxi1" in kwargs:
        createdcboxi.displayboxi1 = kwargs["displayboxi1"]
        createdcboxi.displaykey1 = kwargs["displaykey1"]
    
    if "displayboxi2" in kwargs:
        createdcboxi.displayboxi2 = kwargs["displayboxi2"]
        createdcboxi.displaykey2 = kwargs["displaykey2"]

    
    if "displayboxi3" in kwargs:
        createdcboxi.displayboxi3 = kwargs["displayboxi3"]
        createdcboxi.displaykey3 = kwargs["displaykey3"]
        stuff = False

    if "displaycolor" in kwargs:
        createdcboxi.displaycolor = kwargs["displaycolor"]
    
    return createdcboxi

# Render an individual string in given font, color
def rendertext(text, font, color):
    return font.render(text, 1, color)

# Render a dictionary of text items, add "render" key to it containing images of the text
def rendertextdic(textdic, font, color):
    for key, value in textdic.items():
        textdic[key]["render"] = font.render(key, 1, color)
    return textdic