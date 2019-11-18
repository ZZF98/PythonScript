import ctypes
import inspect
import threading
import time


def main(a):
    while True:
        print(a)


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        main(self.name)


# 停止多线程
def _async_raise(tid, exctype):
    print("停止多线程_async_raise")
    print("停止多线程_async_raise:" + str(tid))
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    print("开始停止推流stop_thread")
    count = 0
    while True:
        try:
            _async_raise(thread.ident, SystemExit)
        except ValueError as e:
            count = count + 1
            print(e)
            if count > 5:
                return
        except SystemError as e:
            count = count + 1
            print(e)
            if count > 5:
                return
        else:
            return


if __name__ == '__main__':
    nameList = [1, 2, 3, 4, 5, 6]
    threadList = []
    for name in nameList:
        threadList.append(myThread(str(name)))

    # 开启线程
    for thread in threadList:
        thread.start()

    # 停止线程
    time.sleep(1)
    for thread in threadList:
        stop_thread(thread)
        # threadList.remove(thread)
