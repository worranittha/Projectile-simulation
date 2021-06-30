import pygame as pg


class Scale:
    def __init__(self, name, xmin, xmax, xpos, value, option):
        self.name = name
        self.xmin = xmin
        self.xmax = xmax
        self.xpos = xpos
        self.ypos = 400
        self.value = value
        self.default = value
        self.press = False    
        self.option = option

    def createScale(self, allFont, allColor):
        self.scaleArea = pg.Surface((200,90))   # create surface for all scale elements
        self.scaleArea.fill(allColor[0])

        # scale bar graphic
        pg.draw.rect(self.scaleArea, allColor[3], [37.5,30,125,15]) # scale bar is in scaleArea surface

        # button on scale graphic
        self.buttonArea = pg.Surface((23,33))
        pg.draw.rect(self.buttonArea, allColor[3], [0,0,23,33]) # draw rect to button surface
        pg.draw.rect(self.buttonArea, allColor[0], [0,0,23,33], 5) # draw rect border to button surface
     
        # min-max of scale
        self.scopemin = allFont[3].render(str(self.xmin), True, allColor[3])
        self.scopemax = allFont[3].render(str(self.xmax), True, allColor[3])
        self.scopeminRect = self.scopemin.get_rect(center = (37.5, 60))
        self.scopemaxRect = self.scopemax.get_rect(center = (37.5+125, 60))
        self.scaleArea.blit(self.scopemin, self.scopeminRect)
        self.scaleArea.blit(self.scopemax, self.scopemaxRect)

        # scale name
        self.text = allFont[1].render(self.name, True, allColor[3])
        self.textRect = self.text.get_rect(center = (100, 85)) # set center of text when blit in that surface
        self.scaleArea.blit(self.text, self.textRect) # put text to scaleArea surface

    def updateValue(self):
        self.value = (((pg.mouse.get_pos()[0]-self.xpos)-37.5)*(self.xmax-self.xmin)/125) + self.xmin
        if self.value < self.xmin:
            self.value = self.xmin # value not less than min
        if self.value > self.xmax:
            self.value = self.xmax # value not greater than max

    def updateToScreen(self, screen, allFont, allColor, option): # button & value change position when mousebuttondown and move
        # put into scaleArea surface
        scaleArea = self.scaleArea.copy()

        # value of scale
        self.valueArea = allFont[1].render(str(round(self.value,3)), True, allColor[3])
        
        pos = int((self.value-self.xmin)/(self.xmax-self.xmin)*125)+37.5 # set position of button on scale
        self.button = self.buttonArea.get_rect(center=(pos, 37)) # set center of button, center can change to move button
        self.valueCenter = self.valueArea.get_rect(center = (pos,10)) # set center of value of scale

        if(self.name == "SPRING CONSTANT (N/m)" or self.name == "RETRACTION DISTANCE (m)"):
            if(option == False): # false option == close (lock)
                self.lock = pg.image.load("lock.png")     
            elif(option == True): # true option == open (unlock)
                self.lock = pg.image.load("unlock.png")
            self.lock = pg.transform.smoothscale(self.lock, (18,18))    
            self.lockRect = self.lock.get_rect(topleft = (177,26))
            scaleArea.blit(self.lock, self.lockRect)
            self.lockRect.move_ip(self.xpos,self.ypos)
        
        scaleArea.blit(self.buttonArea, self.button) # put button to scaleArea surface
        scaleArea.blit(self.valueArea, self.valueCenter) # put value to scaleArea surface       
        self.button.move_ip(self.xpos,self.ypos) # move button to screen 

        # put scaleArea into screen
        screen.blit(scaleArea, (self.xpos, self.ypos))
