import time
from threading import Thread

import PyHook3
import pythoncom


# hm = PyHook3.HookManager()

class hook():
    def __init__(self):
        self.hm = PyHook3.HookManager()
        self.init_hook()
        self.passwords = []
        self.is_lock = False

    def OnMouseEvent(self, event):
        # print('MessageName:', event.MessageName)  # 事件名称
        # print('Message:', event.Message)  # windows消息常量
        # print('Time:', event.Time)  # 事件发生的时间戳
        # print('Window:', event.Window)  # 窗口句柄
        # print('WindowName:', event.WindowName)  # 窗口标题
        # print('Position:', event.Position)  # 事件发生时相对于整个屏幕的坐标
        # print('Wheel:', event.Wheel)  # 鼠标滚轮
        # print('Injected:', event.Injected)  # 判断这个事件是否由程序方式生成，而不是正常的人为触发。
        # print('---')

        # 返回True代表将事件继续传给其他句柄，为False则停止传递，即被拦截
        return True

    def OnKeyboardEvent(self, event):
        # print('MessageName:',event.MessageName)          #同上，共同属性不再赘述
        # print('Message:',event.Message)
        # print('Time:',event.Time)
        # print('Window:',event.Window)
        # print('WindowName:',event.WindowName)
        if event.Key == 'Rcontrol':
            self.passwords.append(event.Key)
        if len(self.passwords) == 5:
            self.unhook_input()
            self.mask.terminate()
            self.mask.join()
            self.is_lock = False

        # print('Key:', event.Key)  # 按键的名称
        # print('KeyID:', event.KeyID)  # 按键的虚拟键值
        # print('ScanCode:', event.ScanCode)  # 按键扫描码
        # print('Extended:', event.Extended)  # 判断是否为增强键盘的扩展键
        # print('Injected:', event.Injected)
        # print('Alt', event.Alt)  # 是某同时按下Alt
        # print('Transition', event.Transition)  # 判断转换状态
        # print('---')

        return True

    def init_hook(self):
        self.hm.MouseAllButtonsDown = self.OnMouseEvent
        self.hm.KeyDown = self.OnKeyboardEvent

    def hook_input(self, mask):
        self.is_lock = True
        self.mask = mask
        self.hm.HookMouse()
        self.hm.HookKeyboard()
        pythoncom.PumpMessages()

    def unhook_input(self):
        self.is_lock = False
        self.passwords = []
        self.hm.UnhookMouse()
        self.hm.UnhookKeyboard()


# pythoncom.PumpMessages()

if __name__ == '__main__':
    a = hook()

    t_lock = Thread(target=a.hook_input)

    t_lock.start()
    while True:
        time.sleep(1)
        print(a.is_lock)
    # a.hook_input()
