import sys

import win32api
import win32con
import win32gui
import win32ts
from PyQt5.QtWidgets import *

WM_WTSSESSION_CHANGE = 0x2B1
WTS_SESSION_LOCK = 0x7
WTS_SESSION_UNLOCK = 0x8


class WndProcHookMixin:
    def __init__(self):
        self.msgDict = {}

    def hookWndProc(self):
        self.oldWndProc = win32gui.SetWindowLong(self.winId(), win32con.GWL_WNDPROC, self.localWndProc)

    def unhookWndProc(self):
        win32api.SetWindowLong(self.winId(), win32con.GWL_WNDPROC, self.oldWndProc)

    def addMsgHandler(self, messageNumber, handler):
        self.msgDict[messageNumber] = handler

    def localWndProc(self, hWnd, msg, wParam, lParam):
        if msg in self.msgDict:
            if self.msgDict[msg](wParam, lParam) == False:
                return

        if msg == win32con.WM_DESTROY:
            self.unhookWndProc()

        return win32gui.CallWindowProc(self.oldWndProc, hWnd, msg, wParam, lParam)


class Window(QWidget, WndProcHookMixin):
    def __init__(self,lock_status, *args, **kwargs):
        self.lock_status=lock_status
        QWidget.__init__(self, *args, **kwargs)



        win32ts.WTSRegisterSessionNotification(self.winId(), win32ts.NOTIFY_FOR_ALL_SESSIONS)
        self.addMsgHandler(WM_WTSSESSION_CHANGE, self.on_session)
        self.hookWndProc()

    def on_session(self, wParam, lParam):
        global lock_status
        event, session_id = wParam, lParam
        if event == WTS_SESSION_LOCK:
            self.lock_status[0] = True
            print("Locked")
        if event == WTS_SESSION_UNLOCK:
            self.lock_status[0] = False
            print("Unlocked")


def get_lock(lock_status):
    app = QApplication(sys.argv)
    win = Window(lock_status)
    sys.exit(app.exec_())


if __name__ == '__main__':
    pass