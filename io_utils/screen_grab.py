from PIL import ImageGrab, Image
from datetime import datetime
from time import sleep
from PIL import Image
import numpy as np
from win32api import GetSystemMetrics
import win32gui
import win32ui
import win32con


def screenshot():
    img = ImageGrab.grab()
    return [img]


def windowgrab(name):
    hwnd = win32gui.FindWindow(None, name)
    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    return background_screenshot(hwnd, x1 - abs(x0), y1 - y0)


def background_screenshot(hwnd, width, height):
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)
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
    return [np.array(im)]


def is_out_of_screen(x0, x1, y0, y1):
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    if not (-20 <= x0 <= width) or not (-20 <= x1 <= width) or \
       not (-20 <= y0 <= height) or not (-20 <= y1 <= height):
        return True
    return False


if __name__ == "__main__":
    hwnd = win32gui.FindWindow(None, "Telegram")
    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    if is_out_of_screen(x0, y0, x1, y1) is False:
        # gui_running.WindowWarning()
        print(x0, y0, x1, y1)
    background_screenshot(hwnd, x1 - x0, y1 - y0)
