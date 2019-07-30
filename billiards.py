import matplotlib
import math
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import time

class Ball:

    def __init__(self, m, r, pos):

        self.m   = m                #ball mass
        self.r   = r                #ball radius
        self.v0  = [0.0, 0.0]       #initial velocity
        self.vt  = [0.0, 0.0]       #current velocity
        self.pos = pos              #position
        self.fC  = 0                #force carrying

    def amMoving(self, f, cr1, mp, thet, width, height, fR, dur, overRide):
        global check
        t = dur
        m = self.m

        if check:    
            self.f = f                                                       #if it's the first check                                      
            v0net = f  + (mp*cr1*(f/m)) / (mp + m)
            
            vt   = v0net
            self.pos[0] = self.pos[0] + ( t * vt * math.cos(thet) ) #moves forward xcomp
            self.pos[1] = self.pos[1] + ( t * vt * math.sin(thet) ) #moves forward ycomp
            
            self.v0 = [vt * math.cos(thet), vt * math.sin(thet)]  

            check = False     
            #print('cheks')
            return True
            
        elif (self.pos[0] <= width and self.pos[0] > 0) and (self.pos[1] <= height and self.pos[1] > 0):                #if ball hasn't hit wall yet
            #print('slowdown')
            print("Noraml velocity is" + str(self.v0) + "\n\n")
            print(self.pos)

            netV0       = self.v0[0]**2 + self.v0[1]**2
            netVT       = math.sqrt(netV0 - 2.0*(fR / m)*(netV0*t))
            
            self.pos[0] = self.pos[0] + ( t * netVT * math.cos(thet) ) #moves forward xcomp
            self.pos[1] = self.pos[1] + ( t * netVT * math.sin(thet) ) #moves forward ycomp
            self.v0     = [netVT * math.cos(thet), netVT * math.sin(thet)] #slows the ball down but only bc of friction
            
            #self.f      = 
            return True

        elif overRide == True:
            print("I'm overRide-ing the movement. I'm probably in a wall rn")
            input("ok so I'm seeing that the post wall vel was {}".format(self.v0))

            netV0       = math.sqrt( self.v0[0]**2 + self.v0[1]**2)
            #netVT       = netV0 - 2.0*(fR / m)*(netV0*t)
            
            self.pos[0] = self.pos[0] +( t * netV0 * math.cos(thet) ) #moves forward xcomp
            self.pos[1] = self.pos[1] + ( t * netV0 * math.sin(thet) ) #moves forward ycomp
            self.v0     = [netV0 * math.cos(thet), netV0 * math.sin(thet)] #slows the ball down but only bc of friction
            
            input("My pos is {} \n\n".format(self.pos))
            input("My vel is {} \n\n".format(self.v0))
              
            return True
        else:            
            print('hit wall')                                                    #if ball hit wall
            print('I tried man but you in a wall')
            return False
    
    def wallHit(self, thet, cr2, d, f0, width, height):
        
        print("dims are {} x {}".format(width, height))
        print("My position is {}".format(self.pos))
        input("My post-wall velocity is {}\n\n\n".format([vX, vY]))


                               
class Boarder:

    def __init__(self, width, height, wallM):
        
        self.width   = width
        self.height  = height
        self.holePos = [1, 2, 3, 4, 5, 6]
        self.wallM   = 100 #should go unused until project fully works



#----------------------------------------------------------------------------------------------
m  = .37
mP = 5.0
r  = 4.0
f  = 30

cr1 = .9      #coefficient of resitution que and ball
cr2 = .5      #coefficient of restitution wall and ball

mu  = .3
fR  = mu * m * 9.8

dur = .01
d   = .001

theta = 3 * (math.pi / 4)

global check
check = True

width = 100.0
height = 300.0

xLim = 300.0
yLim = 300.0
#----------------------------------------------------------------------------------------------

allPos = [[50,50]]
balls  = [i for i in range(len(allPos))]
circs  = [i for i in range(len(allPos))]

for i in range(len(allPos)):
    pos     = allPos[i]
    balls[i] = Ball(m, r, pos)

t    = 0
thet = 3*(math.pi / 4)
posA = [[] for i in range(len(balls))]

while t <= 30:  #30 'seconds'. Each frame moves forward dur second

    # fig, ax = plt.subplots()
    # ax.set_xlim((0, xLim))
    # ax.set_ylim((0, yLim))
    # ax.axis('equal')
    # ax.add_artist(plt.Rectangle([0, 0], 150, 300))

    for i, ball in enumerate(balls):
        x = ball.pos[0] 
        y = ball.pos[1]
        
        if ball.amMoving(f, cr1, mP, thet, width, height, fR, dur, False) == True:
            pass
            # if (x >= 0 and x <= width) and (y >= 0 and y <=height):
            # ball.amMoving(f, cr1, mP, thet, width, height, fR, dur)
            print("no wall")

            posA[i] = ball.pos
            t = t + dur
        elif ball.amMoving(f, cr1, mP, thet, width, height, fR, dur, False) == False: #x <= 0 or x >= width) or (y <= 0 or y>= height):
            print('wall')

            while (x not in range(int(width))) or (y not in range(int(height))):
                ball.amMoving(f, cr1, mP, thet, width, height, fR, dur, True)

            posA[i] = ball.pos
            #ax.add_artist(circs[i])
            t = t + dur
        else:
            print("screw up")

    tList = list(map(list, zip(*posA)))
   
    plt.scatter(tList[0], tList[1])

    plt.xlim(0, width)
    plt.ylim(0, height)
    
    plt.draw()
    plt.pause(.01)
    plt.clf()
    
 