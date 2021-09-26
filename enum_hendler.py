import win32gui
import win32con


def enum_handler(hwnd, lParam):
    if 'chromedriver.exe' in win32gui.GetWindowText(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)