import multiprocessing
import time
from threading import Thread

import PyHook3

import check_syslock, hook, qt_lock, myblue


def lock(hm, lock_status):
    mask = multiprocessing.Process(target=qt_lock.show_mywindow)
    mask.start()
    #遮罩传入hook进程 用于紧急解锁情况下在hook模块停止遮罩
    t_lock = Thread(target=hm.hook_input, args=(mask,))
    t_lock.start()

    lock_status[0] = True
    return mask


def unlock(hm, lock_status, mask):
    hm.unhook_input()
    mask.terminate()
    mask.join()
    lock_status[0] = False


# WIN原生锁屏
# user32 = windll.LoadLibrary('user32.dll')
# user32.LockWorkStation()


syslock_status = [False]
lock_status = [False]


def main():
    lock_counter = 0
    unlock_counter = 0
    hm = hook.hook()
    p_check = multiprocessing.Process(target=check_syslock.get_lock, args=(syslock_status,))
    p_check.start()

    # mask = lock(hm, lock_status)
    # time.sleep(z3)
    # unlock(hm, lock_status, mask)

    while True:
        # time.sleep(3)
        exist = myblue.find_only('94:65:2D:89:96:68')
        # 锁屏 在系统未锁屏、自写未锁屏时
        if not exist and not syslock_status[0] and not lock_status[0]:
            lock_counter += 1
            if lock_counter >= 3:
                mask = lock(hm, lock_status)
                lock_counter = 0
        if exist:
            lock_counter = 0

        # 解锁 取消hook 在发现设备和系统锁屏时
        if (exist or syslock_status[0]) and lock_status[0]:
            print(lock_status)
            unlock_counter += 1
            unlock(hm, lock_status, mask)
            # find_all()

        # 紧急解锁 同步hook的解锁屏状态到主进程
        if hm.is_lock == False and lock_status[0]:
            lock_status[0]=False
            time.sleep(60)

        print(lock_counter)
        print(lock_status)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
