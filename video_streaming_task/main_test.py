import os

from moviepy.video.io.VideoFileClip import VideoFileClip

from video_streaming_task.mysql_sql import *
from video_streaming_task.upload import send_file
from video_streaming_task.yingshi import *

dirPath = 'C:\\Users\\EDZ\\Desktop\\video'


def my_job():
    print("当前时间:{}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    # 获取一小时前的时间戳
    time_now = int(round(time.time() * 1000) - 3600 * 1000)
    # 生成文件列表
    file_list_creat(time_now)
    device_list = find_device_data()
    for device in device_list:
        print("当前设备：{}".format(device[0]))
        yingshi_data_list = get_store_file_data(device[0], time_now)
        if yingshi_data_list["code"] == '200' and yingshi_data_list["data"] is not None:
            node_list = find_node_by_time(yingshi_data_list["data"])
            for yingshi_data in node_list:  # yingshi_data_list["data"]:
                data = {}
                device_serial = yingshi_data["deviceSerial"]
                startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(yingshi_data["startTime"]) / 1000))
                endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(yingshi_data["endTime"]) / 1000))
                # date = time.strftime('%Y%m%d', time.localtime(time.time()))
                date = 20190923
                data["date"] = date
                data["device_serial"] = device_serial
                data["startTime"] = startTime
                data["endTime"] = endTime
                print(data)
                video_node = find_file_list_node(data)
                # 表示日期为凌晨11点到第二天
                if len(video_node) != 2:
                    continue
                data = {}
                start_node = video_node[0]
                end_node = video_node[1]
                data["startTime"] = start_node[1]
                data["endTime"] = end_node[1]
                data["device_serial"] = device_serial
                # 根据两个端点获取文件列表
                file_list = find_file_list(data)
                for file in file_list:
                    print("下载：{}".format(file[1]))

                    timestamp = int(round(time.mktime(
                        time.strptime(creat_start_date(file[1]),
                                      "%Y-%m-%d %H:%M:%S")) * 1000))
                    """
                    64408405314_1569246587000_22_C97043289.MP4
                    """
                    clip = VideoFileClip(dirPath + "\\" + file[1])
                    new_name = yingshi_data[
                                   'fileId'] + "_" + str(timestamp) + "_" + str(round(clip.duration)) + "_" + str(
                        device_serial) + ".MP4"
                    clip.close()
                    # 重命名文件
                    os.rename(dirPath + "\\" + file[1], dirPath + "\\" + new_name)
                    video_path = dirPath + "\\" + new_name
                    # 保证上传
                    while True:
                        try:
                            response = send_file(device_serial, video_path, timestamp, str(round(clip.duration)))
                            if response:
                                updata_video_data(new_name, yingshi_data[
                                    'fileId'], file[0])
                                os.remove(dirPath + "\\" + new_name)
                                break
                        except Exception as e:
                            print(e)
                            pass

                print(file_list)
                print(video_node)
        else:
            print("{}为空".format(device[0]))
    # 清空一小时数据
    delete_file_by_time(time_now)


# 生成文件列表
def file_list_creat(time_now):
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
        data_size = getDocSize(dirPath + "\\" + file)
        if data_size < 10:
            print("删除文件：" + dirPath + "\\" + file + "文件大小：" + str(data_size) + "M")
            os.remove(dirPath + "\\" + file)
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
    return date


# 删除文件
def delete_file_by_time(time_now):
    # 获取文件列表
    dirList = os.listdir(dirPath)
    for file in dirList:
        start_date = creat_start_date(file)
        time_start_date = int(round(time.mktime(
            time.strptime(start_date,
                          "%Y-%m-%d %H:%M:%S")) * 1000))
        # 找一个小时前的
        if time_now < time_start_date:
            continue
        print("删除文件：" + dirPath + "\\" + file)
        os.remove(dirPath + "\\" + file)


# 根据监测点获取node列表
def find_node_by_time(data):
    print(len(data))
    node_list = []
    # 记录该数据填充情况
    matrix = [0 for i in range(len(data))]
    for i in range(len(data)):
        # 如果最后一个节点已经标识过说明可以直接退出
        if matrix[-1] == 1:
            break
        if matrix[i] == 0:
            pre_endTime = data[i]["endTime"]
            # 初始化节点数据
            node = copy_yingshi_node_data(data[i])
            # 如果是最后一个节点，直接添加
            if i == len(data) - 1:
                node_list.append(node)
                break
            # 标识已经使用
            matrix[i] = 1
            for n in range(i + 1, len(data)):
                if matrix[n] == 0:
                    # startTime = time.strftime('%Y-%m-%d %H:%M:%S',
                    #                           time.localtime(int(pre_endTime + 3600 * 1000 / 2) / 1000))
                    # endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data[n]["startTime"]) / 1000))
                    # print(startTime)
                    # print(endTime)
                    # 判断上个节点的结束时间后半个小时是否大于下个节点的时间
                    if int(pre_endTime) + 3600 * 1000 / 2 > int(data[n]["startTime"]):
                        # 记录最后更新的时间
                        pre_endTime = data[n]["endTime"]
                        # 标识已经使用
                        matrix[n] = 1
                    else:
                        # 记录节点最后的一次值将本次最后的时间修改
                        node["endTime"] = pre_endTime
                        # 大于1小时
                        # if int(node["startTime"]) + 3600 * 1000 < int(node["endTime"]):
                        #     print("--------------------------------------------node start:")
                        #     for x in range(i, n):
                        #         startTime = time.strftime('%Y-%m-%d %H:%M:%S',
                        #                                   time.localtime(int(data[x]["startTime"]) / 1000))
                        #         endTime = time.strftime('%Y-%m-%d %H:%M:%S',
                        #                                 time.localtime(int(data[x]["endTime"]) / 1000))
                        #         print(startTime)
                        #         print(endTime)
                        #     print("-------------------------------------------node end:")

                        # 小于一分钟
                        if int((int(node["endTime"]) - int(node["startTime"])) / 1000) < 60:
                            print("############################################node start:")
                            for x in range(i, n):
                                startTime = time.strftime('%Y-%m-%d %H:%M:%S',
                                                          time.localtime(int(data[x]["startTime"]) / 1000))
                                endTime = time.strftime('%Y-%m-%d %H:%M:%S',
                                                        time.localtime(int(data[x]["endTime"]) / 1000))
                                print(startTime)
                                print(endTime)
                            print("############################################node end:")
                        startTime = time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(int(node["startTime"]) / 1000))
                        endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(node["endTime"]) / 1000))
                        print("开始时间：{}".format(startTime))
                        print("结束时间：{}".format(endTime))

                        node_list.append(node)
                        break
    print(node_list)
    return node_list


# copy萤石数据
def copy_yingshi_node_data(data):
    node = {}
    node["startTime"] = data["startTime"]
    node["endTime"] = data["endTime"]
    node["deviceSerial"] = data["deviceSerial"]
    node["fileId"] = data["fileId"]
    return node


# sched = BlockingScheduler()
#
# sched.add_job(my_job, 'cron', day='*', hour='2,5,8,11,14,17,20,23', minute=59)
#
# sched.start()

def main():
    my_job()


if __name__ == '__main__':
    main()
