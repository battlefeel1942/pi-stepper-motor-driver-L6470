#import the required modules
import sys

import Slush

#the number of steps we want to be moving
stepmove = 300000

#setup the Slushengine
b = Slush.sBoard()


motor = Slush.Motor(0)
motor.resetDev()

#this isn't current
motor.setCurrent(20, 20, 20, 20)

#move the motor in one direction and wait for it to finish
while(motor.isBusy()):	
	continue
motor.move(stepmove)



while(motor.isBusy()):
	continue
motor.move(-1 * stepmove)
	
#when these operations are finished shut off the motor
while(motor.isBusy()):
	continue

#release motor	
motor.free()


