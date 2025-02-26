import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
import time
import sys
import pygame
import threading
from pygame.locals import *
import pigpio

GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
#GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD
pi = pigpio.pi()

class Racing_Wheel:
    '''
    해당 코드는 파이게임(pygame) 이라는 라이브러리를 응용하여 조이스틱 값을 받고 사용합니다.
    함수는 다음과 같습니다.
    선언 시, 파이게임용 시간과 조이스틱을 반환합니다.
    
    Init_Racing_Wheel() -> 시작용 함수, 파이게임 시간을 반환, clock, joystick 반환
    '''
    def __init__(self, status = 0, verbose = False):   
        self.clock, self.joysticks = self.Init_Racing_Wheel()
        self.status = status
        self.verbose = verbose
        self.wheel_Value = [0, 0]
    
    #Racing Wheel 관련 시작 함수 실행, clock과 joystick을 반환함
    def Init_Racing_Wheel(self):
        pygame.init()
        pygame.joystick.init()
        self.clock = self.Set_Clock()
        self.joysticks = self.Get_Joystick()
        return self.clock, self.joysticks
    
    def Set_Clock(self):
        self.clock = pygame.time.Clock()
        return self.clock
    
    def Get_Joystick(self):
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            print(joystick.get_name())
            joystick.init()
        return self.joysticks
    
    def Update_Input_Value(self):
        counter = 0
        #time.sleep(0.35)
        
        for event in pygame.event.get():
            
            #if(counter > 20):
             #   break
            #counter+=1
            
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    self.status = 0
#                    self.wheel_Value[0] = max(2000, min(1800, ((50*(event.value* 10)) + 1500)))
                    self.wheel_Value[0] = max(750, min(2250, (1500 - (75*(event.value* 10)))))
                    #(1150,1850,50)
                elif event.axis == 2:
                    self.status = 2
                    self.wheel_Value[1] = max(0, self.wheel_Value[1] - int(event.value *5 +5))
                elif event.axis == 5:
                    self.status = 5
                    self.wheel_Value[1] = min(20, self.wheel_Value[1] + int(event.value *5 +5))
    
class RC_Car_Control:
    '''
    해당 클래스는 RC카를 제어하기 위한 클래스로
    클래스 호출 시 servo모터와 dc모터값을 설정합니다.
    MOTOR_A_A1의 PIN = 23 / MOTOR_A_B1의 PIN = 24 로 세팅되어 있으며
    servo, dc_pwm, dcMotor_Power, servo_Degree를 조정 가능
    '''
    #====================[INIT]========================
    def __init__(self, DcMotor_Power = 50, Servo_Degree = 90, GPIOPIN_MOTOR_A1 = 23, GPIOPIN_MOTOR_B1 = 24, GPIOPIN_MOTOR_A1_PWM= 0, 
                 servo = 0, dc_pwm = 0, verbose = False):
        self.GPIOPIN_MOTOR_A1 = GPIOPIN_MOTOR_A1
        self.GPIOPIN_MOTOR_B1 = GPIOPIN_MOTOR_B1
        self.GPIOPIN_MOTOR_A1_PWM = GPIOPIN_MOTOR_A1_PWM
        self.servo = servo
        self.dc_pwm = dc_pwm
        self.dcMotor_Power = DcMotor_Power
        self.servo_Degree = Servo_Degree
        #self.Setup_Servo_Motor()
        self.Setup_DC_Motor()
        self.verbose = verbose
        
    #===============[Setup_DC Motor]====================
    def Setup_DC_Motor(self, MOTOR_PWM_FREQUENCY = 20):
        '''
        이 함수는 기본적으로 PWM_Frequency, 모터 A_A1과 A_B1 값 설정
        PWM_Frequency = 20 / A_A1 = 20 / A_B1 = 21
        PWM_Frequency 값만 설정하려면 인자 하나만 입력하시면 됩니다.
        각 A_A1, A_B1 값은 GPIO 핀 값입니다.
        '''
        MOTOR_PWM_FREQUENCY = 20 # PWM Frequency
        GPIO.setup(self.GPIOPIN_MOTOR_A1, GPIO.OUT)
        GPIO.setup(self.GPIOPIN_MOTOR_B1, GPIO.OUT)
        self.GPIOPIN_MOTOR_A1_PWM = GPIO.PWM(self.GPIOPIN_MOTOR_A1, MOTOR_PWM_FREQUENCY)
        self.GPIOPIN_MOTOR_A1_PWM.start(0)
        GPIO.output(self.GPIOPIN_MOTOR_A1, GPIO.LOW)
        GPIO.output(self.GPIOPIN_MOTOR_B1, GPIO.LOW)
    
    #===============[STOP_DC Motor]====================
    def Stop_MOTOR(self):
        self.GPIOPIN_MOTOR_A1_PWM.stop()
        
        if self.verbose == True:
            print("STOP MOTOR")
    
    #===============[Change_DUTY_DC Motor]====================
    def Change_Duty_Cycle(self):
        self.GPIOPIN_MOTOR_A1_PWM.ChangeDutyCycle(self.dcMotor_Power)
        print(f"dcMotor_Power = {self.dcMotor_Power}")
        

    #===============[Setup_Servo POS]====================
    def Set_Servo_Pos(self, Servo_degree):
        '''
        서보 위치 제어 함수
        degree에 각도를 입력하면 duty로 변환후 서보 제어(ChangeDutyCycle)
        SERVO_MAX_DUTY    = 12   # 서보의 최대(180도) 위치의 주기
        SERVO_MIN_DUTY    = 3    # 서보의 최소(0도) 위치의 주기
        '''
        pi.set_servo_pulsewidth(17,Servo_degree)

        print(f"servo_degree = {Servo_degree}")
       
class UDAS:
    '''
    해당 클래스는 초음파 값 획득하기 위한 클래스로
    클래스 호출 시 DANGER_DISTANCE를 설정합니다.
    초음파의 Trigger PIN = 5 / Echo PIN = 6 로 세팅되어 있습니다.
    '''
    def __init__(self, GPIOPIN_TRIG = 21, GPIOPIN_ECHO = 20, DANGER_DISTANCE = 30, verbose = False, distance = None):
        self.GPIOPIN_TRIG = GPIOPIN_TRIG
        self.GPIOPIN_ECHO = GPIOPIN_ECHO
        self.DANGER_DISTANCE = DANGER_DISTANCE
        self.verbose = verbose
        self.distance = distance
        self.Initiate_ACPE()

    def Initiate_ACPE(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIOPIN_TRIG, GPIO.OUT)
        GPIO.setup(self.GPIOPIN_ECHO, GPIO.IN)

    def Measure_Distance(self):
        '''
        1회 거리를 측정하는 함수, delay가 0.02
        '''

        GPIO.output(self.GPIOPIN_TRIG, True)
        time.sleep(0.02)
        GPIO.output(self.GPIOPIN_TRIG, False)

        pulse_start = time.time()
        while GPIO.input(self.GPIOPIN_ECHO) == 0:
            pulse_start = time.time()

        pulse_end = time.time()
        while GPIO.input(self.GPIOPIN_ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150

        #if distance <= -500 or distance >= 500:
            #return None

        return distance

    def Update_Stable_Distance(self, samples = 5):
        '''
        5번 Sampling 해서 거리 평균 거리 측정
        '''
        distances = []
        for _ in range(samples):
            distance = self.Measure_Distance()
            if distance is not None:
                distances.append(distance)
            time.sleep(0.05)

        if len(distances) > 0:
            if self.verbose == True:
                print(f"stable distance = {sum(distances) / len(distances)}")
            self.distance = sum(distances) / len(distances)
        else:
            print("ultrasonic sensor do not working !!")
            self.distance = None
    
    
def Init_UDAS():
    global UDAS_Set, Racing_Wheel_Set, RC_Car_Set
    #변수 초기화
    UDAS_Set = UDAS()
    Racing_Wheel_Set = Racing_Wheel()
    RC_Car_Set = RC_Car_Control()

#region ============================ Threading Set (TOP) ============================

def Threading_UltraSonic():
    global UDAS_Set
    try:
        print("UltraSonic Start")
        while True:
            UDAS_Set.Update_Stable_Distance()
    except KeyboardInterrupt:
        print("Ultrasonic Stopped")

def Threading_RacingWheel():
    global Racing_Wheel_Set
    try:
        print("RacingWheel Start")
        while True:
            Racing_Wheel_Set.Update_Input_Value()
    except KeyboardInterrupt:
        print("RacingWheel Check Stopped")


#endregion ============================ Threading Set (BOTTOM) ============================
    
#region ============================ API Set (TOP) ============================

# . Racing Wheel
def Get_Racing_Wheel_Status():
    global Racing_Wheel_Set
    return Racing_Wheel_Set.status

def Get_Racing_Wheel_Value():
    global Racing_Wheel_Set
    return Racing_Wheel_Set.wheel_Value
    
def Update_Racing_Wheel():
	global Racing_Wheel_Set
	Racing_Wheel_Set.Update_Input_Value()

# . RC Car
def Get_RC_Car_DcMotor_Power():
    global RC_Car_Set
    return RC_Car_Set.dcMotor_Power

def Set_RC_Car_DcMotor_Power(value):
    global RC_Car_Set
    RC_Car_Set.dcMotor_Power = value
    
def Set_RC_Car_Servo_Pos(value):
    global RC_Car_Set
    RC_Car_Set.Set_Servo_Pos(value)
    
def Update_RC_Car_Duty_Cycle():
    global RC_Car_Set
    RC_Car_Set.Change_Duty_Cycle()
    
# . Ultra Sonic
def Get_Stable_Distance():
    global UDAS_Set
    return UDAS_Set.distance

def Get_DANGER_DISTANCE():
    global UDAS_Set
    return UDAS_Set.DANGER_DISTANCE
    
def Thread_Function_UDAS():
	global UDAS_Set
	UDAS_Set.Update_Stable_Distance()

#endregion ============================ API Set (BOTTOM) ============================


def Check_Pedal_Error():
    distance = Get_Stable_Distance()
    print(f"distance: {distance}")
    
    if distance is None:
        return False

    #if distance < Get_DANGER_DISTANCE() and Get_Racing_Wheel_Status() == 5:
    #if distance < 10 and Get_Racing_Wheel_Status() == 5:
    if distance < 25:
        print("페달 오조작 감지. 가속 제한.")
        return True
        #if Get_RC_Car_DcMotor_Power() > 1:
            #Set_RC_Car_DcMotor_Power(1)
            #RC_Car_Set.Stop_MOTOR()
            #return True
        
    else:
        #print("정상적인 조작 감지중")
        return False
    
    
    
def Init_Get_UltraSonic_Distance():
    '''
    초음파에서 데이터 받아오는 함수입니다.
    Init_UltraSonic 함수가 실행되어 있지 않다면, 실행되지 않습니다.
    (함수 내부에서 Init_UltraSonic 진행하나, 권장하지 않습니다)
    
    Returns : Mean Distance Values
    '''
    global UDAS_Set
    if (isinstance(UDAS_Set, UDAS) == False):
        Init_UDAS()
        return
    try:
        # 쓰레딩으로 데이터 한 번에 수집 
        udas_thread = threading.Thread(
            target=Threading_UltraSonic, 
            args=()
        )
        # 스레딩 시작
        udas_thread.start()
        
        #스레드 끝날대 까지 기다리기
#        udas_thread.join()
#        racing_wheel_thread.join()
        
    except KeyboardInterrupt:
        print("monitoring stopped")

def Init_Get_Racing_Wheel():
    global Racing_Wheel_Set
    
    try:
        # 쓰레딩으로 데이터 한 번에 수집 
        racing_wheel_thread = threading.Thread(
            target=Threading_RacingWheel,
            args=())
        # 스레딩 시작
        racing_wheel_thread.start()

        #스레드 끝날대 까지 기다리기
#        udas_thread.join()
#        racing_wheel_thread.join()
        
    except KeyboardInterrupt:
        print("monitoring stopped")


#Init_UDAS()
#Init_Get_UltraSonic_Distance()
#while True:
#	print(f"SD: {Get_Stable_Distance()}")
#	time.sleep(0.25)
