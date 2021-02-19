

"""
读取yaml测试数据

"""

import yaml
import os
import os.path


def parse():
    path_ya = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))) + '/Params/Param'
    pages = {}
    for root, dirs, files in os.walk(path_ya): #root 遍历的文件夹的名字 dirs 文件夹下的子文件夹集合 files 文件夹中的文件集合
        for name in files:
            watch_file_path = os.path.join(root, name)
            with open(watch_file_path, 'rb') as f:
                page = yaml.safe_load(f)#读取yaml文件
                pages.update(page)
        return pages


class GetPages:
    @staticmethod #定义静态方法
    def get_page_list():
        _page_list = {}
        pages = parse()
        for page, value in pages.items():
            parameters = value['parameters']
            data_list = []
            for parameter in parameters:
                data_list.append(parameter)
            _page_list[page] = data_list
        return _page_list


if __name__ == '__main__':
    lists = GetPages.get_page_list()
