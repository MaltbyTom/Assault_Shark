# Box Library
# Tom Maltby
import pygame

def screensetup(sw, sh, sh_nb):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global SCREEN_HEIGHT_NOBOX
    SCREEN_WIDTH = sw
    SCREEN_HEIGHT = sh
    SCREEN_HEIGHT_NOBOX = sh_nb

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
        loadborder = pygame.Rect(destxleft - border - border2 , destytop - border - border2, thing.width + 2 * border + 2 * border2, thing.height + 2 * border + 2 * border2)
        pygame.draw.rect(target, bordercolor, loadborder, 0, 2)
    # Inner box
    loadbox = pygame.Rect(destxleft - border, destytop - border, thing.width + 2 * border, thing.height + 2 * border)
    pygame.draw.rect(target, backcolor, loadbox, 0, 2)
    target.blit(thing, (destxleft + wmod, destytop + hmod))

def cboxi(target, things, destytop, destxleft, border, backcolor, border2, bordercolor, maxh, maxw):
    maxwid = 0
    maxhi = 0
    for i, thing in things:
        if things(thing).width > maxwid:
            maxwid = things(thing).width
        if things(thing).height > maxhi:
            maxhi = things(thing).height
    hmod = 0
    for b, thing in things:
        boxi(target, things(thing), destytop + (b * maxhi) + border + border2, destxleft, border, backcolor, border2, bordercolor, maxhi, maxwid)

def rboxi(target, things, destytop, destxleft, border, backcolor, border2, bordercolor):
    maxwid = 0
    maxhi = 0
    for i, thing in things:
        if things(thing).width > maxwid:
            maxwid = things(thing).width
        if things(thing).height > maxhi:
            maxhi = things(thing).height

    for b, thing in things:
        boxi(target, things(thing), destytop + ((maxhi - things(thing).height) // 2), destxleft + b * maxwid + ((maxwid - things(thing).width) // 2) +border + border2, border, backcolor, border2, bordercolor)
