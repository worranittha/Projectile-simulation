import pygame as pg
import math
import csv


class Projectile:
    def __init__(self, sheight, angle, springconst, retract, theight, tDis, playspeed):  
        self.sheight = sheight # shooter height
        self.theight = theight # target height
        self.tDistance = tDis # target distance
        self.angle = angle
        self.springconst = springconst
        self.retract = retract  # retract = retraction distance
        self.playSpeed = playspeed
        self.speed = 0
        self.time = 0
        self.distance = 0

    def calculate(self):
        self.height = self.theight - self.sheight
        self.rad = self.angle*math.pi/180 # change angle in degree to radian
        h = self.retract*math.sin(self.rad) 
        energy = abs((self.springconst*(math.pow(self.retract, 2))/0.405) - (2*9.81*h)) # 0.405 = mass of shooting system (มวลส่วนหัวยิง)
        springspeed = math.pow(energy, 0.5)
        self.speed = (0.405*springspeed)/0.429 # 0.429 = 0.405+0.024 (0.024 = mass of squash ball)
        speedx = self.speed*math.cos(self.rad)
        speedy = self.speed*math.sin(self.rad)
        rootintime = math.sqrt(math.pow(speedy, 2)-(2*9.81*self.height))
        self.time = (speedy + rootintime)/(9.81)
        self.distance = speedx*self.time
        self.playSpeed = self.distance*100

        # calculate to change retraction distance (fix spring constant)
        newh = 0.405*9.81*math.sin(self.rad) # newh = mspring*g*sin
        self.newSpeed = math.pow((9.81*math.pow(self.tDistance,2)) / (2*math.pow(math.cos(self.rad),2)*(self.tDistance*math.tan(self.rad)-self.height)),0.5)
        self.newSpringSpeed = (0.429/0.405) * self.newSpeed
        self.newRetract = (newh + math.pow((newh*newh) + (self.springconst*0.405*self.newSpringSpeed*self.newSpringSpeed),0.5)) / self.springconst
        
        # calculate to change spring constant (fix retraction distance)
        self.newSpringConst = ((0.405*self.newSpringSpeed*self.newSpringSpeed) + (2*newh*self.retract)) / (self.retract*self.retract)

        # save data to file
        allData = [round(self.sheight,3), round(self.angle,3), 
                    round(self.springconst,3), round(self.retract,3), round(self.tDistance,3), 
                    round(self.speed,3), round(self.distance,3), round(self.time,3)]
        with open('data.csv', 'a', newline='') as dataFile:
            writer = csv.writer(dataFile, delimiter=',')
            writer.writerow(allData)

    def createArea(self, allFont, allColor):
        self.simArea = pg.Surface((685,350))
        self.simArea.fill(allColor[0])

        # create title (fix)
        self.title = allFont[0].render("PROJECTILE SIMULATION", True, allColor[2], allColor[0])
        self.simArea.blit(self.title, (340,23))

        # create graph (fix)
        self.graph = pg.image.load("graph.png")
        height, width = self.graph.get_size()
        self.graph = pg.transform.smoothscale(self.graph, (int(height/2), int(width/2)))
        self.simArea.blit(self.graph, (55,13)) 

        # create Ball (can change)
        self.ballArea = pg.Surface((30,30))
        self.ballArea.set_colorkey((0,0,0))
        pg.draw.circle(self.ballArea, allColor[5], (15,15), 15, 15)
        # create Ball line (can change)
        self.bArea = pg.Surface((2,2))
        self.bArea.set_colorkey((0,0,0))
        pg.draw.circle(self.bArea, allColor[5], (1,1), 1, 1)

        # create result (can change)
        self.resultArea = pg.Surface((350,100))
        self.resultArea.set_colorkey((0,0,0))

        # create target (can change)
        self.target = pg.image.load("target.png")
        self.target = pg.transform.smoothscale(self.target, (49,49))

        # create shooter (can change)
        self.shooter0 = pg.image.load("shooter.png")
        self.shooter0 = pg.transform.smoothscale(self.shooter0, (95,95))
        self.shooterLeg = pg.image.load("shooterLeg.png")
        self.shooterLeg = pg.transform.smoothscale(self.shooterLeg, (50,50))

    def drawShooterAndTarget(self, screen, tDistance, sheight, angle):
        simArea = self.simArea.copy()
        # change target
        self.targetRect = self.target.get_rect(center = (int((tDistance/3.3)*600)+65, 324.5))
        # change shooter
        self.shooter = pg.transform.rotate(self.shooter0, angle - 45) # rotate shooter
        self.shootRect = self.shooter.get_rect(center = (60 , int((1-(sheight/3.3))*345)+32.5-25))  
        self.shootLegRect = self.shooterLeg.get_rect(center = (60 , int((1-(sheight/3.3))*345)+30))
        
        simArea.blit(self.target, self.targetRect)
        simArea.blit(self.shooter, self.shootRect)
        simArea.blit(self.shooterLeg, self.shootLegRect)
        screen.blit(simArea, (295,20))

    def plot(self, screen, allFont, allColor, fps, allScale):
        x = 0
        allBall = [] # keep ball line

        # show result
        if(self.distance < self.tDistance + 0.05 and self.distance > self.tDistance - 0.05): 
            d = self.distance
            self.result = allFont[2].render("GOAL!", True, allColor[4], allColor[0])
        else : 
            self.result = allFont[2].render("MISS!", True, allColor[5], allColor[0])
            if(allScale[2].option == False): # fix spring constant (change retraction distance)
                self.change = allFont[1].render("Change retraction distance to " + str(round(self.newRetract,3)) + " m", True, allColor[5], allColor[0])
                if(self.newRetract < 0.01 or self.newRetract > 0.2):
                    self.warn = allFont[1].render("Over the limit! Please change spring constant", True, allColor[5], allColor[0])
                    self.warnRect = self.warn.get_rect(center = (175,75))
                    self.resultArea.blit(self.warn, self.warnRect)  
            elif(allScale[2].option == True): # fix retraction distance (change spring constant)
                self.change = allFont[1].render("Change spring constant to " + str(round(self.newSpringConst,2)) + " N/m", True, allColor[5], allColor[0])
                if(self.newSpringConst < 100 or self.newSpringConst > 1000):
                    self.warn = allFont[1].render("Over the limit! Please change retraction distance", True, allColor[5], allColor[0])
                    self.warnRect = self.warn.get_rect(center = (175,75)) 
                    self.resultArea.blit(self.warn, self.warnRect)
            self.changeRect = self.change.get_rect(center = (175,50))  
            self.resultArea.blit(self.change, self.changeRect)  
            d = 3.3
        
        self.resultRect = self.result.get_rect(center = (175,20))
        self.resultArea.blit(self.result, self.resultRect)

        # plot ball and elements in simArea
        while(x <= d):
            t = x/(self.speed*math.cos(self.angle*math.pi/180))
            y = -(self.height) + (self.speed*math.sin(self.angle*math.pi/180)*t) - (0.5*9.81*t*t)

            xpos = int((x/3.3)*600) + 65
            ypos = int((1-(y/3.3))*345) - (self.theight*100) 

            allBall.append([xpos, ypos])

            if(xpos >= 640 or ypos >= 330): break # break before ball go out simArea

            simArea = self.simArea.copy()

            self.ball = self.ballArea.get_rect(center = (xpos,ypos))
            for b in allBall:
                self.b = self.bArea.get_rect(center = (b[0],b[1]))
                simArea.blit(self.bArea, self.b) 
            self.targetRect = self.target.get_rect(center = (int((self.tDistance/3.3)*600)+65, 324.5))
            self.shooter = pg.transform.rotate(self.shooter0, self.angle - 45)
            self.shootRect = self.shooter.get_rect(center = (60 , int((1-(self.sheight/3.3))*345)+32.5-25))             
            self.shootLegRect = self.shooterLeg.get_rect(center = (60 , int((1-(self.sheight/3.3))*345)+30))
            
            simArea.blit(self.resultArea, (325,100))
            simArea.blit(self.ballArea, self.ball)    
            simArea.blit(self.target, self.targetRect)
            simArea.blit(self.shooter, self.shootRect)
            simArea.blit(self.shooterLeg, self.shootLegRect)

            screen.blit(simArea, (295,20))

            pg.display.flip()
            fps.tick(self.playSpeed)

            x+=0.01
