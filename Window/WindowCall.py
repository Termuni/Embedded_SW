'''
이 스크립트에서 각 레벨별 윈도우 부를 예정입니다.
'''
#import
import sys, os
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

window_path = "C:/SeonMin/Embedded_SW/Window/ui"
sub_paths = ["Debug", "Lv1", "Lv2"]#, "Lv3", "Lv4"]

for sub_path in sub_paths:
    full_path = os.path.join(window_path, sub_path)
    
    # 경로를 sys.path에 추가
    if full_path not in sys.path:
        sys.path.append(full_path)

#==================CUSTOM IMPORT==================
import Debug_Caller as dbg
import Lv1_Warning_Caller as lv1
import Lv2_Warning_Caller as lv2
#==================CUSTOM IMPORT==================


class WindowThread(QThread):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def run(self):
        if self.level == 'debug':
            dbg.Open_Window()
            time.sleep(1)  # 창을 1초 동안 열어둠
            dbg.Close_Debug_Window()

def Show_Window(level):
    if level == 'a':
        lv1.Show_Window()
    if level == 2:
        lv2.Show_Window()
    if level == 'debug':
        # 새로운 스레드에서 창을 열고 닫는 동작을 비동기적으로 수행
        window_thread = WindowThread('debug')
        window_thread.start()


#region API Set

#region LV1 API

def Get_LV1_BTN_Clicked():
    return lv1.Get_BTN_Clicked()

def Close_LV1_Window():
    lv1.Close_LV1_Window()

#endregion LV1 API

#region Debugging API

def Get_Debug_PPG_LV():
    return dbg.Get_Debug_PPG_LV

def Get_Debug_ECG_LV():
    return dbg.Get_Debug_ECG_LV

def Get_Debug_CAM_LV():
    return dbg.Get_Debug_CAM_LV

def Get_Debug_Pedal_ERR():
    return dbg.Get_Debug_Pedal_ERR

def Get_Debug_Mode():
    return dbg.Get_Debug_Mode

def Close_Debug_Window():
    dbg.Close_Debug_Window()

#endregion Debugging API

#endregion API Set

while True:
    print("Debug TESTING")
    Show_Window('debug')
    time.sleep(1)
    Close_Debug_Window()