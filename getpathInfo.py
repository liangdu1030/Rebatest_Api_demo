import os

def get_Path():
    # 这个是获取当前文件夹的路径
    path = os.path.split(os.path.realpath(__file__))[0]
    return path

if __name__ == '__main__':
    print("测试路径:",get_Path())