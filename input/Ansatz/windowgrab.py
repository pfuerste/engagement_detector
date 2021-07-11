import sys
import os
from PIL import Image
import numpy as np

sys.path.insert(0, os.path.abspath(r"E:\Users\Alexander\anaconda3\Lib\site-packages\win32\win32gui.pyd"))
sys.path.insert(0, os.path.abspath(r"E:\Users\Alexander\anaconda3\Lib\site-packages\win32\win32ui.pyd"))
sys.path.insert(0, os.path.abspath(r"E:\Users\Alexander\anaconda3\Lib\site-packages\win32\win32api.pyd"))

from win32api import GetSystemMetrics
import win32gui
import win32ui
import win32.lib.win32con as win32con


def background_screenshot(hwnd, width, height):
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
    bmpinfo = dataBitMap.GetInfo()
    bmpstr = dataBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())    
    return np.array(im)

def is_out_of_screen(x0,x1,y0,y1):
    width=GetSystemMetrics(0)
    height=GetSystemMetrics(1)
    if (x0<width and x0>0) and (x1<width and x1>0) and (y0<width and y0>0) and (y1<height and y1>0):
        return True
    return False

def windowgrab(name):
    hwnd=win32.gui.FindWindow(None,name)
    x0,y0,x1,y1=win32gui.GetWindowRect(hwnd)
    #No Idea how to send it to GUI from here. Call it from Main?
    return background_screenshot(hwnd,x1-abs(x0),y1-y0)


##needs to be in main
'''
hwnd = win32gui.FindWindow(None, gui_start.WindowName)
x0,y0,x1,y1=win32gui.GetWindowRect(hwnd)
if {importfile}.is_out_of_screen()==False:
    gui_running.WindowWarning()
{importfile}.background_screenshot(hwnd, x1-x0, y1-y0)
'''