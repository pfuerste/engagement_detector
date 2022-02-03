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


def window_grab(name):
    """Gets the name of the window, which has to be captured
        and returns screenshot
        Args:
            name (string): name of the window

        Returns:
            np.array from background_screenshot
    """
    hwnd = win32gui.FindWindow(None, name)
    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    return background_screenshot(hwnd, x1 - abs(x0), y1 - y0)


def background_screenshot(hwnd, width, height):
    """Gets the parameters of the window, which has to be captured
        and returns screenshot
        Args:
            name (string): name of the window
            width (int): width of window
            height (int): height of window

        Returns:
            picture as np.array
    """
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


def window_out_of_screen(name):
    """Check if window is not complete on screen

        Args:
            name (string): name of the window

        Returns:
            boolean from coords_out_of_screen

    """
    hwnd = win32gui.FindWindow(None, name)
    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    return coords_out_of_screen(x0, y0, x1, y1)


def coords_out_of_screen(x0, y0, x1, y1):
    """Check if window is not complete on screen

        Args:
            name (string): name of the window
            x0 (int): top left corner
            y0 (int): top left corner
            x1 (int): bottom right corner
            y1 (int): bottom right corner

        Returns:
            True or False

    """
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    if not (-20 <= x0 <= width + 20) or not (-20 <= x1 <= width + 20) or \
       not (-20 <= y0 <= height + 20) or not (-20 <= y1 <= height + 20):
        return True
    return False


if __name__ == "__main__":
    hwnd = win32gui.FindWindow(None, "Telegram")
    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    if coords_out_of_screen(x0, y0, x1, y1) is False:
        # gui_running.WindowWarning()
        print(x0, y0, x1, y1)
    background_screenshot(hwnd, x1 - x0, y1 - y0)
