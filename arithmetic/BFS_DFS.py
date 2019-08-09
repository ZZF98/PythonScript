# 深搜广搜
class Node(object):
    """初始化一个节点,需要为节点设置值"""

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BinaryTree(object):
    """
    创建二叉树,完成
    - 添加元素
    - 广度遍历
    - 深度遍历
    """

    def __init__(self):
        self.root = None
        pass

    # 添加元素
    def addNode(self, val):
        # 创建队列结构存储结点
        nodeStack = [self.root]

        # 如果根结点为空
        if self.root == None:
            self.root = Node(val)
            print("添加根节点{0}成功!".format(self.root.val))
            return

        # 模拟生成一颗二叉树，本身只持有root节点
        while len(nodeStack) > 0:
            # 队列元素出列
            p_node = nodeStack.pop()

            # 如果左子结点为空
            if p_node.left == None:
                p_node.left = Node(val)
                print("添加左:{0} ".format(p_node.left.val))
                return

            # 如果右子节点为空
            if p_node.right == None:
                p_node.right = Node(val)
                print("添加右:{0} ".format(p_node.right.val))
                return

            # 入队
            nodeStack.insert(0, p_node.left)
            nodeStack.insert(0, p_node.right)

    # 广度优先遍历
    def BFS(self):
        nodeStack = [self.root];

        # 只要队列不为空
        while len(nodeStack) > 0:
            my_node = nodeStack.pop()
            print("-->", my_node.val)

            if my_node.left is not None:
                nodeStack.insert(0, my_node.left)

            if my_node.right is not None:
                nodeStack.insert(0, my_node.right)

    # 深度优先(先序遍历)栈
    def DFS(self, start_node):

        # 如果节点为null说明没有val
        if start_node == None:
            return

        print("-->", start_node.val)
        # 入栈,先入先出
        self.DFS(start_node.left)
        self.DFS(start_node.right)

    # # 深度优先(中序遍历)
    # def inorder(self, start_node):
    #     if start_node == None:
    #         return
    #
    #     self.inorder(start_node.left)
    #     print(start_node.val)
    #     self.inorder(start_node.right)
    #
    # # 深度优先(后序遍历)
    # def outorder(self, start_node):
    #     if start_node == None:
    #         return
    #     self.outorder(start_node.left)
    #     self.outorder(start_node.right)
    #     print(start_node.val)


def main():
    # 生成一个二叉树
    bt = BinaryTree()
    bt.addNode(0)
    bt.addNode(1)
    bt.addNode(2)
    bt.addNode(3)
    bt.addNode(4)
    bt.addNode(5)
    bt.addNode(6)
    bt.addNode(7)
    bt.addNode(8)
    bt.addNode(9)

    print("广度遍历-->")
    bt.BFS()

    print("先序遍历-->")
    bt.DFS(bt.root)

    # print("中序遍历-->")
    # bt.inorder(bt.root)
    #
    # print("后序遍历-->")
    # bt.outorder(bt.root)


import os
import collections

if __name__ == '__main__':
    main()


# 广搜
def getAllDirByBFS(path):
    queue = collections.deque()
    # 进队
    queue.append(path)
    # 循环，当队列为空，停止循环
    while len(queue) > 0:
        # 出队数据 这里相当于找到A元素的绝对路径
        dirPath = queue.popleft()
        try:
            # 找出跟目录下的所有的子目录信息，或者是跟目录下的文件信息
            dirList = os.listdir(dirPath)
            # 遍历该文件夹下的其他信息
            for filename in dirList:
                # 绝对路径
                dirAbsPath = os.path.join(dirPath, filename)
                # 判断：如果是目录dir入队操作，如果不是dir打印出即可
                if os.path.isdir(dirAbsPath):
                    print("目录：" + dirAbsPath + filename)
                    queue.append(dirAbsPath)
                else:
                    print("普通文件：" + dirAbsPath + filename)
        except:
            print("打开异常" + dirPath)


# 函数的调用
getAllDirByBFS('D:\\automatedTestTool')


# 深搜
def getAllDirByDFS(path):
    stack = []
    # 压栈操作,相当于图中的A压入
    stack.append(path)
    # 处理栈，当栈为空的时候结束循环
    while len(stack) > 0:
        # 从栈里取数据，相当于取出A，取出A的同时把BC压入
        dirPath = stack.pop()
        try:
            firstList = os.listdir(dirPath)
            # 判断：是目录压栈，把该目录地址压栈，不是目录即是普通文件，打印
            for filename in firstList:
                fileAbsPath = os.path.join(dirPath, filename)
                if os.path.isdir(fileAbsPath):
                    # 是目录就压栈
                    stack.append(fileAbsPath)
                    getAllDirByDFS(fileAbsPath)
                else:
                    # 是普通文件就打印即可，不压栈
                    print("普通文件：", fileAbsPath + filename)
        except:
            print("打开异常" + dirPath)


getAllDirByDFS(r'D:\\automatedTestTool')
