import time
# https://blog.csdn.net/ithaibiantingsong/article/details/87775362
from apscheduler.schedulers.blocking import BlockingScheduler


# 上午12点
def my_job_12():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


# 晚上12点
def my_job_24():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


sched = BlockingScheduler()

sched.add_job(my_job_12, 'cron', day='*', hour='0-23', minute=59, second=59)

sched.start()

# def main():
#
#
# if __name__ == '__main__':
#     main()
