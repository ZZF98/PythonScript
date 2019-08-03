# 快排算法
def quick_sort(start, end, arr, sort):
    # 如果start>=end了就说明已经递归完整个数组了
    if not start < end:
        return

    """
    取第一个数为基准数，然后将比其小的放左边比它大的放右边，由此可以划分两个数组。
    然后将这两个数组再次快排，就实现了整个快排算法，这也是一种分治思想
    """
    baseValue = arr[start]

    # 用来标记比基准数大的偏移量（从左往右）
    little = start
    # 用来标记比基准数小的偏移量（从右往左）
    big = end

    if sort == "<":
        # 只要big和little没有碰头就说明没有遍历完整个数组
        while little < big:

            """
            只要数组未便利完，并且当前数组右侧比左侧大可以说明该右侧数组是存放比基准数大的数组。
            如果出现比基准数小的，则跳出循环并且将该值覆盖到arr[little]的位置，如果是第一次则相当于将基数覆盖
            """
            while little < big and arr[big] > baseValue:
                big -= 1

            # 跳出循环说明该arr[big]的值比arr[little]的值小，所以进行覆盖
            arr[little] = arr[big]

            """
            只要数组未便利完，并且当前数组左侧比右侧大可以说明该左侧数组是存放比基准数小的数组。
            如果出现比基准数大的，则跳出循环并且将该值覆盖到arr[big]的位置
            """
            while little < big and arr[little] <= baseValue:
                little += 1

            # 跳出循环说明该arr[little]的值比arr[big]的值大，所以进行覆盖
            arr[big] = arr[little]
    else:
        # 只要big和little没有碰头就说明没有遍历完整个数组
        while little < big:

            """
            原理跟正序便利相同，结果相反而已
            """
            while little < big and arr[big] < baseValue:
                big -= 1

            arr[little] = arr[big]

            """
            原理跟正序便利相同，结果相反而已
            """
            while little < big and arr[little] >= baseValue:
                little += 1

            arr[big] = arr[little]

    # 当这个while跳出来之后相当于little和big碰头了，所以可以理解为这个位置是类似于中位数的一个存在
    arr[little] = baseValue

    """
    这时候以中位数为标准可以知道左侧存放的都是比其小的，右侧是放比它大的。
    然后通过同样的算法可以获取一个顺序的数组
    """
    # 中位数左侧数组
    quick_sort(start, little - 1, arr, sort)
    # 中位数右侧数组
    quick_sort(little + 1, end, arr, sort)


if __name__ == '__main__':
    arr = [5, 4, 7, 2, 1, 5, 3, 2, 9, 6, 7]
    quick_sort(0, len(arr) - 1, arr, "<")
    print(arr)
    arr = [5, 4, 7, 2, 1, 5, 3, 2, 9, 6, 7]

    quick_sort(0, len(arr) - 1, arr, ">")
    print(arr)
