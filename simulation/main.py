import pygame as pg
from Display import Display

pg.init()

# set color
blue = pg.Color("#243859")
lightblue = pg.Color("#58BEC7")
blueGray = pg.Color("#47799C")
green = pg.Color("#93CDB3")
yellow = pg.Color("#EEB462")
red = pg.Color("#E63C49")
allColor = [blue, lightblue, blueGray, green, yellow, red]

# set font
titleFont = pg.font.Font("Myriad Semibold Condensed.otf", 40)
scaleFont = pg.font.Font("Myriad Pro Semibold SemiCondensed.otf", 15)
outputFont = pg.font.Font("Myriad Pro Semibold SemiCondensed.otf", 20)
scopeFont = pg.font.Font("Myriad Pro Semibold SemiCondensed.otf", 12)
allFont = [titleFont, scaleFont, outputFont, scopeFont]

# main
screen = pg.display.set_mode((1050,600))
icon = pg.image.load("icon.png")
pg.display.set_icon(icon)
pg.display.set_caption("Projectile Simulation")
screen.fill(blue)

D = Display(screen, allFont, allColor)

while True:
    D.displayToScreen()
    pg.display.flip()