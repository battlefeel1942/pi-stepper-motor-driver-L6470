#import the required modules
import sys
import time

import Slush

#initalizes the board and all its functions
SlushEngine = Slush.sBoard()
print("Initalizing the board and all its functions")
time.sleep(1)

#initalizes the az motor on the board
az = Slush.Motor(0)
az.resetDev()
print("Initalizing az the motor on the board")
time.sleep(1)

#initalizes the em motor on the board
em = Slush.Motor(1)
em.resetDev()
print("Initalizing the em motor on the board")
time.sleep(1)

#set az motor current hold, run, accel, decel & steps
az.setCurrent(10, 50, 25, 25)

az.setMicroSteps(8)
print("Setting az motor current hold, run, accel, decel & steps")
time.sleep(1)

#set em motor current hold, run, accel, decel & steps
em.setCurrent(10, 20, 25, 25)
em.setMicroSteps(8)
print("Setting em motor current hold, run, accel, decel & steps")
#time.sleep(1)

#configure az motor motion parameters
az.setAccel(100)
az.setDecel(100)
az.setMaxSpeed(600)
print("Configuring az motor motion parameters")
time.sleep(1)

#configure em motor motion parameters
em.setAccel(100)
em.setDecel(100)
em.setMaxSpeed(600)
print("Configuring em motor motion parameters")
time.sleep(1)

#move the az motor motor with move command
print("moving the az motor motor with move command")
az.move(20000)
while(az.isBusy()):
	continue

#move the az motor in reverse with move command
print("moving the az motor motor in reverse with move command")
az.move(-20000)
while(az.isBusy()):
	continue

#move the em motor forward with move command
print("moving the em motor forward with move command")
em.move(20000)
while(em.isBusy()):
	continue

#move the em motor in reverse with move command
print("moving the em motor in reverse with move command")
em.move(-20000)
while(em.isBusy()):
	continue

#Wait for 5 seconds
time.sleep(5)

#free motor
az.free()
em.free()
