#import
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__path__)))

from HeartBeat import BPM as bpm
# from ACPE
# from Window

#Set Constant Values

#====================Main==================

try:
    #INIT VALUES
    #Set Class
    
    
    print("START PROCESSING")
    while True:
        #If Debug Mode
        print("DEBUG MODE ACTIVATE")
        
        #Else Getting Sensor Value
        print("DEBUG MODE DEACTIVATE")
        
        #Warning Lv Calculate By Algorithm
        
        
        #If Warning LV 1
            #LCD Alarm
            #Remote Off
        
        
        #Elif Warning LV 2
            #Sound Output
            #LED ON
            #Remote Off
        
        
        #Elif Warning LV 3
            #Remote On
        
        
        #If Remote OFF
            #Set Motor Data by CCU
        
        
        #Else Remote ON
            #Get Motor Data from TCU
        
        
        #If There Is Nothing Blocking Front
            #Sending Motor and Submotor Value
        
        
        #Else Something Blocking Front
        print("ACPE ACTIVE")
        
except:
    print("END")
    
finally:
    print("CLEAN")