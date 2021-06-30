import yaml
import os
from PIL import ImageGrab
from datetime import datetime
from time import sleep
import win32gui
import win32ui
import win32con
from ctypes import windll
# import Image
from PIL import Image


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


def screenshot():
    img = ImageGrab.grab()
    # dt = datetime.now()
    # fname = os.path.join("input", "data", "pic_{}.{}.png".format(
    #     dt.strftime("%H%M_%S"), dt.microsecond // 100000))
    return [img]


if __name__ == "__main__":
    # conf = yaml.safe_load(open("input/config.yml"))

    # hwnd = win32gui.FindWindow(None, "Telegram")
    # background_screenshot(hwnd, 1280, 780)
    # while True:
    #     take_screenshot()
    #     sleep(conf["sleep_seconds"])
#    hwnd = win32gui.FindWindow(None, 'BigBlueButton - Anwendungspraktikum')

    # hwnd = win32gui.FindWindow(None, 'Telegram')
    hwnd = win32gui.FindWindow(None, 'Zoom Meeting Participant ID: 484447')
    # Change the line below depending on whether you want the whole window
    # or just the client area.
    #left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    print(left, top, right, bot)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    print(result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        # PrintWindow Succeeded
        im.save("test.png")
