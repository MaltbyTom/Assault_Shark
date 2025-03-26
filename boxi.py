# The boxi.py Library:
# The BoxiPyG project, v0.3
# Box Intelligence for Pygame
# An UI constructor toolkit
# Tom Maltby 2025
# Code and graphics

#________________________________________
#__________,,,,,,,,,,,,,,_____/\_________
#________/ooooooooooooooo\___/|^\""\,,,__
#___/\/\/OOOOOOOOOOOOOOOOOOOOOOOOO*OOOO:_
#_______|OOOOOOOOOOOOOOOOOOOOOOOOOOOO/"__
#_______|OOOOOOOOOOOOOOOOOOOOOO/_""""____
#________\OOOOOOOOOOOOOOOOOOOO|__________
#_________\OOOOOO/""""""""\OOO\__________
#__________|O\\O|__________\O\O|_________
#__________|U||U|__________|U|U|_________
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Joystick handling imported under MIT license:
#  Copyright (c) 2017 Jon Cooper
#
#  pygame-xbox360controller.
#  Documentation, related files, and licensing can be found at
#
#      <https://github.com/joncoop/pygame-xbox360controller>.
#  Thanks to Jon Cooper, simpler than reinventing the wheel
# 
#  The screeninfo module is by authors = ["Marcin Kurczewski <rr-@sakuya.pl>"]
#  The github is at "https://github.com/rr-/screeninfo", the license is MIT, again many thanks!


import pygame



pygame.init()

# Define fonts
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
DKGRAY = pygame.Color("dimgray")
DKGREEN = pygame.Color("darkgreen")

# Screen setup inheritance from boxitest.py, etc
def screensetup(sw, sh, sh_nb):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global SCREEN_HEIGHT_NOBOX
    SCREEN_WIDTH = sw
    SCREEN_HEIGHT = sh
    SCREEN_HEIGHT_NOBOX = sh_nb

# Control registry, just a list of controls that get the self.register() function called
regcontrols = []

# Draws registered controls
def drawregcontrols():
    for control in regcontrols:
        control.draw()

# Focus on the next control in the tab order
def tabcontrols(forward):
    # Iterate to find the next control
    for control in regcontrols:
        if hasattr(control, "tabord"):
            if control.tabord > itabmax:
                itabmax = control.tabord
                

    # Move the selection boxi
    # Moving the selection boxi should set a focus global flag which is used to direct events through the focusmanager
    if forward == False:
        # Iterate backwards through the tab order as per shift-tab
        stuff = False
    else:
        # Iterate forwards through the tab order
        stuff == True

# The basic building block
class Boxi():
    
    def __init__(self, x, y, width, height, border, color, border2, color2, *args, **kwargs):
        # x - left, y - top, width, height are for the surface box (without borders included), where most images are displayed.
        # border, color, border2, color2 are size and color of borders, two underlying rectangles.  Setting border or border2 to 0
        # will result in that layer not extending beyond the layer above.  The first border property may be thought of as the interior
        # of the boxi on which the thing is placed; border2 is a frame rectangle underneath that.  A Boxi object is usually initialized
        # by calling the boxi function which sets it up.  For advanced controls, boxi is called many times by the parent's creation
        # function and __init__.  The function boxi() returns a Boxi object.

        super(Boxi, self).__init__()
        # Initialize the boxi
        self.rectsurf = pygame.Rect(x,y,width,height)
        self.rectbox = pygame.Rect(x - border, y - border, width + (2 * border), height + (2 * border))
        self.boxcolor = color
        self.rectborder = pygame.Rect(x - border - border2, y - border - border2, width + (2 * border) + (2 * border2), height + (2 * border) + (2 * border2))
        self.bordercolor = color2
        self.row = 0
        self.column = 0
        self.selected = False
        self.selgrow = 2 # self.selgrow is the border growth when selected
        self.selborder = pygame.Rect(x - border - border2 - self.selgrow, y - border - border2 - self.selgrow, width + (2 * border) + (2 * border2) + (2 * self.selgrow), height + (2 * border) + (2 * border2) + (2 * self.selgrow))
        self.left = x
        self.top = y
        self.height = height
        self.width = width
        self.border = border
        self.border2 = border2
        # These are offset holders
        self.hmod = 0
        self.wmod = 0
        # These are membership flags
        self.partofcboxi = 0
        self.partofrboxi = 0
        # This is the surface in the Boxi
        self.thing = None
        # .target is the first non-keyword optional argument
        if len(args) > 0:
            self.target = args[0]
        else:
            self.target = None

    def draw(self):
        # Redraw the boxi
        hmod = (self.height - self.thing.height) // 2
        wmod = ((self.width - self.thing.width) // 2)
        # Set offsets for thing from box - procedurally used for sizing for largest thing in columns - cboxi - or rows - rboxi
        self.wmod = wmod
        self.hmod = hmod
        # The 'selected' change in bordersize is reflected in selborder vs rectborder
        # This draws the three stacked rectangles, bottom first
        if self.selected == False:
            pygame.draw.rect(self.target, self.bordercolor, self.rectborder)
        else:
            pygame.draw.rect(self.target, self.bordercolor, self.selborder)
        pygame.draw.rect(self.target, self.boxcolor, self.rectbox)
        # This blits the image / rendered text for the top, or inside, surface
        self.target.blit(self.thing, (self.left + self.wmod, self.top + self.hmod))

    
    def register(self):
        # The self.register method enrolls the control in the update redraw cycle.
        # Only registered controls are programatically redrawn at update.
        regcontrols.append(self)


class Boxicontrolframe(Boxi):
    # A class of Boxi that multi-boxi advanced controls are and reside in

    def __init__(self, x, y, width, height, border, color, border2, color2, control):
        super().__init__(x, y, width, height, border, color, border2, color2)
        self.control = control
        self.left = control.left
        self.top = control.top
        self.width = control.width
        self.height = control.height
        self.target = control.target
        image = pygame.Surface([width,height], pygame.SRCALPHA)
        image = image.convert_alpha()
        self.thing = image

    def draw(self):
        # Make sure size is as control
        self.left = self.control.left
        self.top = self.control.top
        self.width = self.control.width
        self.height = self.control.height
        self.target = self.control.target
        # The 'selected' change in bordersize is reflected in selborder vs rectborder
        # This draws the three stacked rectangles, bottom first
        if self.selected == False:
            pygame.draw.rect(self.target, self.bordercolor, self.rectborder)
        else:
            pygame.draw.rect(self.target, self.bordercolor, self.selborder)
        pygame.draw.rect(self.target, self.boxcolor, self.rectbox)
        # This blits the image / rendered text for the top, or inside, surface
        self.target.blit(self.thing, (self.left + self.wmod, self.top + self.hmod))
        
 

class Cboxi(pygame.Rect):
    # Basic class for columns of boxis, selectable 
    def __init__(self, cdict, target, source, secondkey, top, left, height, width):
        super(Cboxi, self).__init__()
        stuff = False
        self.cdict = cdict
        self.target = target
        self.source = source
        self.secondkey = secondkey
        self.cdict[0]["boxi"].selected = True
        self.selectedrow = 0
        self.frame = Boxicontrolframe(left, top, width, height, 8, GRAY, 4, BLACK, self)
        self.cdict[0]["boxi"].draw()

    def draw(self):
        # Draw the frame
        self.frame.draw()
        # Then the column of boxis
        for sel, value in self.cdict.items():
            self.cdict[sel]["boxi"].draw()
        # Redraw the selected boxi last for highlighting
        self.cdict[self.selectedrow]["boxi"].draw()
   
    def register(self):
        # The self.register method enrolls the control in the update redraw cycle.
        # Only registered controls are programatically redrawn at update.
        regcontrols.append(self)       
    
    def selectnext(self):
        stuff = False
        # Select next boxi down in column of boxis/savegames/items...
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
        # Select next boxi up in column of boxis/savegames/items...
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
    # A scrolling column of boxis, fed by a dictionary class, and linkable to display surfaces to show extra data fields from the dictionary
    # Set up on boxitest to display savegames or enemy types
    def __init__(self, cdict, target, source, secondkey, numvis, tabord, top, left, height, width):
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
        self.top = top
        self.left = left
        self.height = height
        self.width = width
        self.displayfont = font8
        self.displayboxi1 = None
        self.displaykey1 = None
        self.displayboxi2 = None
        self.displaykey2 = None
        self.displayboxi3 = None
        self.displaykey3 = None
        self.displaycolor = BLACK       
        # This is scrolling list logic - it shows the numvis elements in their cboxi, and refreshes them if you scroll past, stopping at the
        # end or beginning.  It reports on entries above or below the screen on the border of the cboxi.
        bct = 0 # This counter numbers iteration through the available source
        visctr = 0 # This counter numbers iteration through the visible boxes
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
        self.frame = Boxicontrolframe(left, top, width, height, 8, GRAY, 4, BLACK, self)


    def draw(self):
        # Refresh the cboxiscroll onscreen
        self.frame.draw()
        for sel, value in self.cdict.items():
            self.cdict[sel]["boxi"].draw()
        # Redraw the selected boxi last for highlighting
        self.cdict[self.selectedrow]["boxi"].draw()
        # Calculate and draw the scrolling labels if all items not displayed
        # Other display options could go here, such as a border slider or a framing-slot index bar
        if self.numvis < self.lastrow:
            numup = self.firstvis
            numdown = self.lastrow - self.lastvis
            if numup > 0:
                upcol = DKGREEN
            else:
                upcol = DKGRAY
            renderup = font8.render(str(numup) + " more above", 1, upcol)
            if numdown > 0:
                downcol = DKGREEN
            else:
                downcol = DKGRAY
            renderdown = font8.render(str(numdown) + " more below", 1, downcol)
            self.target.blit(renderup, (self.left, self.cdict[0]["boxi"].top - 15))
            self.target.blit(renderdown, (self.left, self.bottom + 5))
        # Update optional displays of other keys to linked boxis:  This is useful for showing several datums about an item, such as the
        # wave number and extra lives of a save or an enemies speed and hp.  Easy to extend into a wiki of game objects.  These are passed
        # as kwargs, so they are already optional.  My interpreter doesn't like embedding kwargs' a = b expressions in a list, so they are
        # set manually.  Possibly there is a clever way to do this. 
        if self.displayboxi1 and self.displaykey1:
            dispkey = self.cdict[self.selectedrow]["key"]
            dispval = self.source[dispkey][self.displaykey1]
            self.displayboxi1.thing = rendertext(str(self.displaykey1) +":  "+ str(dispval), self.displayfont, self.displaycolor)
            self.displayboxi1.draw()
        
        if self.displayboxi2 and self.displaykey2:
            dispkey = self.cdict[self.selectedrow]["key"]
            dispval = self.source[dispkey][self.displaykey2]
            self.displayboxi2.thing = rendertext(str(self.displaykey2) +":  "+ str(dispval), self.displayfont, self.displaycolor)
            self.displayboxi2.draw()
        
        
        if self.displayboxi3 and self.displaykey3:
            dispkey = self.cdict[self.selectedrow]["key"]
            dispval = self.source[dispkey][self.displaykey3]
            self.displayboxi3.thing = rendertext(str(self.displaykey3) +":  "+ str(dispval), self.displayfont, self.displaycolor)
            self.displayboxi3.draw()


    def register(self):
        # The self.register method enrolls the control in the update redraw cycle.
        # Only registered controls are programatically redrawn at update.
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

# Now the constructor functions.  Each of these creates an object of class, so boxi(params...) creates a Boxi, cboxi(params...) --> Cboxi, etc

def boxi(target, thing, destytop, destxleft, border, backcolor, border2, bordercolor, ovhi, ovwid, *args, **kwargs ):
    # Basic Boxi object constructor function
    wmod = 0
    hmod = 0
    # Offset calculations
    if ovhi > 0:
        hmod = ((ovhi - thing.height) // 2)
    else:
        ovhi = thing.height
    if ovwid > 0:
        wmod = ((ovwid - thing.width) // 2)
    else:
        ovwid = thing.width
    # Create the Boxi
    loadbox = Boxi(destxleft, destytop, ovwid, ovhi, border, backcolor, border2, bordercolor)
    loadbox.surf = thing
    loadbox.hmod = hmod
    loadbox.wmod = wmod
    loadbox.thing = thing
    loadbox.target = target
    # Draw the boxi
    loadbox.draw()
    target.blit(thing, (destxleft + wmod, destytop + hmod))
    return loadbox

def cboxi(target, things, secondkey, destytop, destxleft, border, backcolor, border2, bordercolor, maxh, maxw):
    # Constructor function for columns of boxi - Cboxi objects
    maxwid = 0
    maxhi = 0
    columnofboxis = {}
    # Find the largest thing in the dictionary.  secondkey points to the image, key is the iterable primary.
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
    # This iterates and puts thing of iterably 'b' things into Boxi objects in the column.
    for b, thing in things.items():
        if secondkey in things[b]:
            thisboxi = boxi(target, things[b][secondkey], destytop + (bct * (maxhi + border + border2)), destxleft, border, backcolor, border2, bordercolor, maxhi, maxwid)
            things[b]["my_boxi"] =  thisboxi 
            things[b]["my_boxi"].row = bct
            columnofboxis[bct] = {"boxi": thisboxi, "key": b, "picture": things[b][secondkey]}
        bct += 1
    createdcboxi = Cboxi(columnofboxis, target, things, secondkey, destytop - (border + border2), destxleft - (border + border2), (bct * maxhi + border + border2) + 2*(border + border2), maxwid + (2 * (border + border2)) )
    bct = 0
    for b in columnofboxis:
        columnofboxis[bct]["boxi"].partofcboxi = createdcboxi
        bct += 1
    return createdcboxi
    

def rboxi(target, things, secondkey, destytop, destxleft, border, backcolor, border2, bordercolor, maxh, maxw):
    # rboxi is from an early version and very simple.  A row of boxis, or an Rboxi object.
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
    # Find largest item for sizing
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
    bct = 0 # This counts the underlying dictionary entries
    visctr = 0 # This counts iterations for filling the visible Boxi objects
    for b, thing in things.items():
        if visctr < numvis:
            if secondkey in things[b]:
                thisboxi = boxi(target, things[b][secondkey], destytop + (bct * (maxhi + border + border2)), destxleft, border, backcolor, border2, bordercolor, maxhi, maxwid)
                things[b]["my_boxi"] =  thisboxi 
                things[b]["my_boxi"].row = bct
                columnofboxis[bct] = {"boxi": thisboxi, "key": b, "bct": bct, "picture": things[b][secondkey]}
        bct += 1
        visctr += 1
    # Checks for optional tab order parameter
    if "tabord" in kwargs:
        tab = kwargs["tabord"]
    else:
        tab = None
    # Creates the object
    yextraborder = 10
    createdcboxi = Cboxiscroll(columnofboxis, target, things, secondkey, numvis, tab, destytop - border - border2 - yextraborder, destxleft - border - border2, (numvis * (maxhi + border + border2)) + (2 * (border + border2)) + (2 * yextraborder), maxwid + (2 * (border + border2)))
    
    # Iteration counter labels Boxi objects as part of the Cboxi object
    bct = 0
    for b in columnofboxis:
        columnofboxis[bct]["boxi"].partofcboxi = createdcboxi
        bct += 1

    if numvis < len(things):    
        # Add scrolling labels for offscreen record size in both directions if more items than displayed
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
    
    # Connect optional display boxis for extra fields in the dictionary entry
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
    
    # Function returns the object
    return createdcboxi

# Render an individual string in given font, color
def rendertext(text, font, color):
    return font.render(text, 1, color)

# Render a dictionary of text items, add "render" key to it containing images of the text
def rendertextdic(textdic, font, color):
    for key, value in textdic.items():
        textdic[key]["render"] = font.render(key, 1, color)
    return textdic