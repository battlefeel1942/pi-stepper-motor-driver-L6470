from Slush.Board import *
from Slush.Constants import *

import math

#Sometimes it's nice to track the methods for debugging
showMethod = False #True #False

class Motor(sBoard):
    
    boardInUse = 0
    
    def __init__(self, motorNumber):
        
        if showMethod == True:
            print("DEBUG - __init__(self, motorNumber)")

       
        #setting the particular chip parameters
        if motorNumber == 0:
            self.chipSelect = MTR0_ChipSelect
        if motorNumber == 1:
            self.chipSelect = MTR1_ChipSelect
        if motorNumber == 2:
            self.chipSelect = MTR2_ChipSelect
        if motorNumber == 3:
            self.chipSelect = MTR3_ChipSelect   
        if motorNumber == 4:
            self.chipSelect = MTR4_ChipSelect
        if motorNumber == 5:
            self.chipSelect = MTR5_ChipSelect
        if motorNumber == 6:
            self.chipSelect = MTR6_ChipSelect
        #init the hardware
        self.initPeripherals()

    ''' initalise the appropriate pins and buses '''
    def initPeripherals(self):
        
        if showMethod == True:
            print("DEBUG - initPeripherals(self)")


        #check that the motors SPI is actually working
        if (self.getParam(CONFIG) == 0x2e88):
            print ("Motor Drive Connected on GPIO " + str(self.chipSelect))
            self.boardInUse = 0
        elif (self.getParam([0x1A, 16]) == 0x2c88):
            print ("High Power Drive Connected on GPIO " + str(self.chipSelect))
            self.boardInUse = 1
        else:
            print ("communication issues; check SPI configuration and cables")

        #based on board type init driver accordingly
        if self.boardInUse == 0:
            self.setOverCurrent(2000)
            self.setMicroSteps(16)
            self.setCurrent(70, 90, 100, 100)
            self.setParam([0x1A, 16], 0x3608)
        if self.boardInUse == 1:
            self.setParam([0x1A, 16], 0x3608)
            self.setCurrent(100, 120, 140, 140)
            self.setMicroSteps(16)

        #self.setParam(KVAL_RUN, 0xff)
        self.getStatus()
        self.free()
        
    ''' check if the motion engine is busy '''
    def isBusy(self):
        
        if showMethod == True:
            print("DEBUG - isBusy(self)")

        print(self.getStatus())
        status = self.getStatus()
        return (not ((status >> 1) & 0b1))
    
    ''' wait for motor to finish moving *** Caution this is blocking *** '''
    def waitMoveFinish(self):
        
        if showMethod == True:
            print("DEBUG - waitMoveFinish(self)")

        status = 1
        while status:
            status = self.getStatus()
            status = not((status >> 1) & 0b1)

    ''' set the microstepping level '''
    def setMicroSteps(self, microSteps):
        
        if showMethod == True:
            print("DEBUG - setMicroSteps(self, microSteps)")

        self.free()
        stepVal = 0

        for stepVal in range(0, 8):
            if microSteps == 1:
                break
            microSteps = microSteps >> 1;
            
        self.setParam(STEP_MODE, (0x00 | stepVal | SYNC_SEL_1))

    ''' set the threshold speed of the motor '''
    def setThresholdSpeed(self, thresholdSpeed):
        
        if showMethod == True:
            print("DEBUG - setThresholdSpeed(self, thresholdSpeed)")

        if thresholdSpeed == 0:
            self.setParam(FS_SPD, 0x3ff)
        else:
            self.setParam(FS_SPD, self.fsCalc(thresholdSpeed))

    ''' set the current'''
    def setCurrent(self, hold, run, acc, dec):
        
        if showMethod == True:
            print("DEBUG - setCurrent(self, hold, run, acc, dec)")

        self.setParam(KVAL_RUN, run)
        self.setParam(KVAL_ACC, acc)
        self.setParam(KVAL_DEC, dec)
        self.setParam(KVAL_HOLD, hold)

    '''set the maximum motor speed'''
    def setMaxSpeed(self, speed):
        
        if showMethod == True:
            print("DEBUG - setMaxSpeed(self, speed)")

        self.setParam(MAX_SPEED, self.maxSpdCalc(speed))

    ''' set the minimum speed '''
    def setMinSpeed(self, speed):
        
        if showMethod == True:
            print("DEBUG - setMinSpeed(self, speed)")

        self.setParam(MIN_SPEED, self.minSpdCalc(speed))

    ''' set accerleration rate '''
    def setAccel(self, acceleration):
        
        if showMethod == True:
            print("DEBUG - setAccel(self, acceleration)")

        accelerationBytes = self.accCalc(acceleration)
        self.setParam(ACC, accelerationBytes)

    ''' set the deceleration rate '''
    def setDecel(self, deceleration):
        
        if showMethod == True:
            print("DEBUG - setDecel(self, deceleration)")

        decelerationBytes = self.decCalc(deceleration)
        self.setParam(DEC, decelerationBytes)

    ''' get the posistion of the motor '''
    def getPosition(self):
        
        if showMethod == True:
            print("DEBUG - getPosition(self)")

        return self.convert(self.getParam(ABS_POS))

    ''' get the speed of the motor '''
    def getSpeed(self):
        
        if showMethod == True:
            print("DEBUG - getSpeed(self)")

        return self.getParam(SPEED)

    ''' set the overcurrent threshold '''
    def setOverCurrent(self, ma_current):
        
        if showMethod == True:
            print("DEBUG - setOverCurrent(self, ma_current)")

        OCValue = math.floor(ma_current/375)
        if OCValue > 0x0f: OCValue = 0x0f
        self.setParam((OCD_TH), OCValue)

    ''' set the stall current level '''
    def setStallCurrent(self, ma_current):
        
        if showMethod == True:
            print("DEBUG - setStallCurrent(self, ma_current)")

        STHValue = round(math.floor(ma_current/31.25))
        if(STHValue > 0x80): STHValue = 0x80
        if(STHValue < 0): STHValue = 9
        self.setParam((STALL_TH), STHValue)

    ''' set low speed optamization '''
    def setLowSpeedOpt(self, enable):
        
        if showMethod == True:
            print("DEBUG - setLowSpeedOpt(self, enable)")

        self.xfer(SET_PARAM | MIN_SPEED[0])
        if enable: self.param(0x1000, 13)
        else: self.param(0, 13)

    ''' start the motor spinning '''
    def run(self, dir, spd):
        
        if showMethod == True:
            print("DEBUG - run(self, dir, spd)")

        speedVal = self.spdCalc(spd)
        self.xfer(RUN | dir)
        if speedVal > 0xfffff: speedVal = 0xfffff
        self.xfer(speedVal >> 16)
        self.xfer(speedVal >> 8)
        self.xfer(speedVal)

    ''' sets the clock source '''
    def stepClock(self, dir):
        
        if showMethod == True:
            print("DEBUG - stepClock(self, dir)")

        self.xfer(STEP_CLOCK | dir)

    ''' move the motor a number of steps '''
    def move(self, nStep):
        
        if showMethod == True:
            print("DEBUG - move(self, nStep)")

        dir = 0

        if nStep >= 0:
            dir = FWD
        else:
            dir = REV

        n_stepABS = abs(nStep)

        self.xfer(MOVE | dir)
        if n_stepABS > 0x3fffff: nStep = 0x3fffff
        self.xfer(n_stepABS >> 16)
        self.xfer(n_stepABS >> 8)
        self.xfer(n_stepABS)

    ''' move to a position with refrence to the motors current position '''
    def goTo(self, pos):
        
        if showMethod == True:
            print("DEBUG - goTo(self, pos)")

        self.xfer(GOTO)
        if pos > 0x3fffff: pos = 0x3fffff
        self.xfer(pos >> 16)
        self.xfer(pos >> 8)
        self.xfer(pos)

    ''' same as go to but with a forced direction '''
    def goToDir(self, dir, pos):
        
        if showMethod == True:
            print("DEBUG - goToDir(self, dir, pos)")

        self.xfer(GOTO_DIR)
        if pos > 0x3fffff: pos = 0x3fffff
        self.xfer(pos >> 16)
        self.xfer(pos >> 8)
        self.xfer(pos)

    ''' sets the hardstop option for the limit switch '''
    def setLimitHardStop(self, stop):
        
        if showMethod == True:
            print("DEBUG - setLimitHardStop(self, stop)")

        if stop == 1: self.setParam([0x1A, 16], 0x3608)
        if stop == 0: self.setParam([0x1A, 16], 0x3618)

    ''' go until switch press event occurs '''
    def goUntilPress(self, act, dir, spd):
        
        if showMethod == True:
            print("DEBUG - goUntilPress(self, act, dir, spd)")

        self.xfer(GO_UNTIL | act | dir)
        if spd > 0x3fffff: spd = 0x3fffff
        self.xfer(spd >> 16)
        self.xfer(spd >> 8)
        self.xfer(spd)

    def getSwitch(self):
        
        if showMethod == True:
            print("DEBUG - getSwitch(self)")

        if self.getStatus() & 0x4: return 1
        else: return 0

    ''' go until switch release event occurs '''
    def goUntilRelease(self, act, dir):
        
        if showMethod == True:
            print("DEBUG - goUntilRelease(self, act, dir)")

        self.xfer(RELEASE_SW | act | dir)

    ''' reads the value of the switch '''
    def readSwitch(self):
        
        if showMethod == True:
            print("DEBUG - readSwitch(self)")

        if self.getStatus() & 0x4: return 1
        else: return 0
    
    ''' go home '''
    def goHome(self):
        
        if showMethod == True:
            print("DEBUG - goHome(self)")

        self.xfer(GO_HOME)

    ''' go to mark position '''
    def goMark(self):
        
        if showMethod == True:
            print("DEBUG - goMark(self)")

        self.xfer(GO_MARK)

    ''' set mark point '''
    def setMark(self, value):
        
        if showMethod == True:
            print("DEBUG - setMark(self, value)")


        if value == 0: value = self.getPosition()
        self.xfer(MARK)
        if value > 0x3fffff: value = 0x3fffff
        if value < -0x3fffff: value = -0x3fffff

        self.xfer(value >> 16)
        self.xfer(value >> 8)
        self.xfer(value)

    ''' set current position to the home position '''
    def setAsHome(self):
        
        if showMethod == True:
            print("DEBUG - setAsHome(self)")

        self.xfer(RESET_POS)

    ''' reset the device to initial conditions '''
    def resetDev(self):
        
        if showMethod == True:
            print("DEBUG - resetDev(self)")

        self.xfer(RESET_DEVICE)
        if self.boardInUse == 1: self.setParam([0x1A, 16], 0x3608)
        if self.boardInUse == 0: self.setParam([0x1A, 16], 0x3608)

    ''' stop the motor using the decel '''
    def softStop(self):
        
        if showMethod == True:
            print("DEBUG - softStop(self)")

        self.xfer(SOFT_STOP)

    ''' hard stop the motor without concern for decel curve '''
    def hardStop(self):
        
        if showMethod == True:
            print("DEBUG - hardStop(self)")

        self.xfer(HARD_STOP)

    ''' decelerate the motor and the disable hold '''
    def softFree(self):
        
        if showMethod == True:
            print("DEBUG - softFree(self)")

        self.xfer(SOFT_HIZ)

    ''' disable hold '''
    def free(self):
        
        if showMethod == True:
            print("DEBUG - free(self)")

        self.xfer(HARD_HIZ)

    ''' get the status of the motor '''
    def getStatus(self):
        
        if showMethod == True:
            print("DEBUG - getStatus(self)")

        temp = 0;
        self.xfer(GET_STATUS)
        temp = self.xfer(0) << 8
        temp += self.xfer(0)
        return temp

    ''' calculates the value of the ACC register '''
    def accCalc(self, stepsPerSecPerSec):
        
        if showMethod == True:
            print("DEBUG - accCalc(self, stepsPerSecPerSec)")

        temp = float(stepsPerSecPerSec) * 0.137438
        if temp > 4095.0: return 4095
        else: return round(temp)

    ''' calculated the value of the DEC register '''
    def decCalc(self, stepsPerSecPerSec):
        
        if showMethod == True:
            print("DEBUG - decCalc(self, stepsPerSecPerSec)")

        temp = float(stepsPerSecPerSec) * 0.137438
        if temp > 4095.0: return 4095
        else: return round(temp)

    ''' calculates the max speed register '''
    def maxSpdCalc(self, stepsPerSec):
        
        if showMethod == True:
            print("DEBUG - maxSpdCalc(self, stepsPerSec)")

        temp = float(stepsPerSec) * 0.065536
        if temp > 1023.0: return 1023
        else: return round(temp)

    ''' calculates the min speed register '''
    def minSpdCalc(self, stepsPerSec):
        
        if showMethod == True:
            print("DEBUG - minSpdCalc(self, stepsPerSec)")

        temp = float(stepsPerSec) * 4.1943
        if temp > 4095.0: return 4095
        else: return round(temp)

    ''' calculates the value of the FS speed register '''
    def fsCalc(self, stepsPerSec):
        
        if showMethod == True:
            print("DEBUG - fsCalc(self, stepsPerSec)")

        temp = (float(stepsPerSec) * 0.065536) - 0.5
        if temp > 1023.0: return 1023
        else: return round(temp)

    ''' calculates the value of the INT speed register '''
    def intSpdCalc(self, stepsPerSec):
        
        if showMethod == True:
            print("DEBUG - intSpdCalc(self, stepsPerSec)")

        temp = float(stepsPerSec) * 4.1943
        if temp > 16383.0: return 16383
        else: return round(temp)

    ''' calculate speed '''
    def spdCalc(self, stepsPerSec):
        
        if showMethod == True:
            print("DEBUG - spdCalc(self, stepsPerSec)")

        temp = float(stepsPerSec) * 67.106
        if temp > float(0x000fffff): return 0x000fffff
        else: return round(temp)

    ''' utility function '''
    def param(self, value, bit_len):
        
        if showMethod == True:
            print("DEBUG - param(self, value, bit_len)")

        ret_value = 0

        byte_len = bit_len/8
        if (bit_len%8 > 0): byte_len +=1

        mask = 0xffffffff >> (32 - bit_len)
        if value > mask: value = mask

        if byte_len >= 3.0:
            temp = self.xfer(value >> 16)
            ret_value |= temp << 16
        if byte_len >= 2.0:
            temp = self.xfer(value >>8)
            ret_value |= temp << 8
        if byte_len >= 1.0:
            temp = self.xfer(value)
            ret_value |= temp
       
        return (ret_value & mask)

    ''' transfer data to the spi bus '''
    def xfer(self, data):
        
        if showMethod == True:
            print("DEBUG - xfer(self, data)")


        #mask the value to a byte format for transmision
        data = (int(data) & 0xff)

        #toggle chip select and SPI transfer
        gpio.output(self.chipSelect, gpio.LOW)
        response = sBoard.spi.xfer2([data])
        gpio.output(self.chipSelect, gpio.HIGH)        

        return response[0]

    ''' set a parameter of the motor driver '''
    def setParam(self, param, value):
        
        if showMethod == True:
            print("DEBUG - setParam(self, param, value)")

        self.xfer(SET_PARAM | param[0])
        return self.paramHandler(param, value)

    ''' get a parameter from the motor driver '''
    def getParam(self, param):
        
        if showMethod == True:
            print("DEBUG - getParam(self, param)")

        self.xfer(GET_PARAM | param[0])
        return self.paramHandler(param, 0)

    ''' convert twos compliment '''
    def convert(self, val):
        
        if showMethod == True:
            print("DEBUG - convert(self, val)")

        if val > 0x400000/2:
            val = val - 0x400000
        return val

    ''' switch case to handle parameters '''
    def paramHandler(self, param, value):
        
        if showMethod == True:
            print("DEBUG - paramHandler(self, param, value)")

        return self.param(value, param[1])
