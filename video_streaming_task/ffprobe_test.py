# -*- coding: utf-8 -*-
import json
import subprocess
import time


def getLength(filename):
    command = ["ffprobe", "-loglevel", "quiet", "-print_format", "json", "-show_format", "-show_streams", "-i",
               filename]
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = result.stdout.read()
    # print(str(out))
    temp = str(out.decode('utf-8'))
    try:
        data = json.loads(temp)['streams'][1]['width']
    except:
        data = json.loads(temp)['streams'][0]['width']
    return data


def getLenTime(filename):
    command = ["ffprobe", "-loglevel", "quiet", "-print_format", "json", "-show_format", "-show_streams", "-i",
               filename]
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = result.stdout.read()
    # print(str(out))
    temp = str(out.decode('utf-8'))
    data = json.loads(temp)
    file_message = {"size": data["format"]['size'], "time": data["format"]['duration']}
    return file_message


print(int(time.time()) * 1000)
a = getLenTime('D:\\video\\C90840816-2019-10-12-01-45-10.mp4')
print(a)
print(time.time() * 1000)
