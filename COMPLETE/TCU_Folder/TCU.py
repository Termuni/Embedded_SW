#import
import sys, os
import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
import time
import numpy as np
import sys
sys.path.append(os.path.dirname(os.path.dirname(__path__)))

#==================CUSTOM IMPORT==================
from Communication import TCU_Socket_Receive as tcu_R
#==================CUSTOM IMPORT==================

#Init
def Init_TCU():
    global GPIO, debug_mode, mode_change_input, control, warning_LV
    # 1. SET GPIO
    GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
    #GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD
       
    # 2. SET TCU-R
    tcu_R.While_Server(tcu_R.Start_Server()) 
    
    # 3. SET extra Datas
    debug_mode = False
    mode_change_input = False
    warning_LV = 0
    control = np.zeros(3)


#====================Main==================

try:
    #INIT VALUES
    Init_TCU()

    print("ACTIVE PROCESSING")
    while True:
        #If Debug Mode
        if mode_change_input:
            mode_change_input = not mode_change_input
            
            if debug_mode:
                print("DEBUG MODE ACTIVATE")
            
            else:
                #Else Getting Sensor Value
                print("DEBUG MODE DEACTIVATE")
                
        
        #If Warning Lv 2
        if warning_LV == 2:
            #Streaming Inside CAM
            print("Streaming Inside CAM")
        
        
        
        #If Warning Lv 3
        if warning_LV == 3:
            #Streaming Outside CAM
            print("Streaming Outside CAM")
        
            #Sending Handling Data to CCU
            
            #Get Data from Center? -> Get What?
            control = tcu_R.While_Server()
        
        
        
        print("")
        
except:
    print("END")
    
finally:
    print("CLEAN")