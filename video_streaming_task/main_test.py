import os

# https://blog.csdn.net/ithaibiantingsong/article/details/87775362
from video_streaming_task.mysql_sql import *
from video_streaming_task.yingshi import *

dirPath = 'C:\\Users\\EDZ\\Desktop\\video'


def my_job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # 生成文件列表
    file_list_creat()
    device_list = find_device_data()
    for device in device_list:
        print("当前-----------" + device[0])
        yingshi_data_list = get_store_file_data(device[0])
        if yingshi_data_list["code"] == 200 and yingshi_data_list["data"] is not None:
            for yingshi_data in yingshi_data_list["data"]:
                device_serial = yingshi_data["deviceSerial"]
                startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(yingshi_data["startTime"]) / 1000))
                endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(yingshi_data["endTime"]) / 1000))
                date = time.strftime('%Y%m%d', time.localtime(time.time()))
                print(date)
                print(device_serial)
                print(startTime)
                print(endTime)
        else:
            print("{}为空".format(device[0]))


# 生成文件列表
def file_list_creat():
    time_now = int(round(time.time() * 1000) - 3600 * 1000)
    # 获取文件列表
    dirList = os.listdir(dirPath)
    for file in dirList:
        data = {}
        start_date = creat_start_date(file)
        time_start_date = int(round(time.mktime(
            time.strptime(start_date,
                          "%Y-%m-%d %H:%M:%S")) * 1000))
        # 找一个小时前的
        if time_now < time_start_date:
            continue

        # 过滤小于10M
        data_size = getDocSize(dirPath + "//" + file)
        if data_size < 10:
            os.remove(dirPath + "//" + file)
            continue
        data["device_serial"] = file.split(".")[0].split("-")[0]
        data["status"] = 0
        data["file_name"] = file
        data["date"] = time.strftime('%Y%m%d', time.localtime(time.time()))
        data["clinic_name"] = ""
        data["start_date"] = start_date
        print(data)
        insert_video_data(data)


# 获取文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return size / 1024 / 1024
    except Exception as err:
        print(err)


# 创建日期
def creat_start_date(file):
    file_data_list = file.split(".")[0].split("-")[1:7]
    date = str(file_data_list[0]) + "-" + str(file_data_list[1]) + "-" + str(file_data_list[2]) + " " + str(
        file_data_list[3]) + ":" + str(file_data_list[4]) + ":" + str(file_data_list[5])
    print(date)
    return date


# sched = BlockingScheduler()
#
# sched.add_job(my_job, 'cron', day='*', hour='2,5,8,11,14,17,20,23', minute=59)
#
# sched.start()

def main():
    my_job()


if __name__ == '__main__':
    main()
