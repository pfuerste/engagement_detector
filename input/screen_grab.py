import yaml
import os
from PIL import ImageGrab
from datetime import datetime
from time import sleep
import win32gui
import win32ui
import win32con


def background_screenshot(hwnd, width, height):
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, 'screenshot.bmp')
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())


def take_screenshot():
    im = ImageGrab.grab()
    dt = datetime.now()
    fname = os.path.join("input", "data", "pic_{}.{}.png".format(
        dt.strftime("%H%M_%S"), dt.microsecond // 100000))
    im.save(fname, 'png')


if __name__ == "__main__":
    conf = yaml.safe_load(open("input/config.yml"))

    hwnd = win32gui.FindWindow(None, "Telegram")
    background_screenshot(hwnd, 1280, 780)
    # while True:
    #     take_screenshot()
    #     sleep(conf["sleep_seconds"])
