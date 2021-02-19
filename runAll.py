import os
import common.HTMLTestRunner as HTMLTestRunner
import getpathInfo as getpathInfo
import unittest
import readConfig as readConfig
from common.configEmail import SendEmail
import time

now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
# 如果要发送邮箱,这些参数要填写
send_mail = SendEmail(
        username="ld15773027507@163.com",
        passwd='AQVGRABRVTQZDHFO',
        recv=['1979635421@qq.com'],    # 可以用逗号分隔,填写多个接收人
        title='测试发送测试报告',
        content="测试发送邮件",
        file=r'D:\\Rebatest_Api_demo\\result\\2020-12-24 13_52_20report.html',
        # file = r'D:\\Rebatest_Api_demo\\result\\%s' %(now + "_report.html"),
        ssl=True,
)
path = getpathInfo.get_Path()
report_path = os.path.join(os.path.join(path, 'result'))
on_off = readConfig.ReadConfig().get_email('on_off')


class AllTest:
    def __init__(self):  # 初始化一些参数和数据
        global resultPath
        #resultPath = os.path.join(report_path, now + "_" + TestCasePath.split("/")[1] + "_report.html")
        resultPath = os.path.join(report_path, now+"report.html")  # result/report.html
        self.caseListFile = os.path.join(path, "caselist.txt")  # 配置执行哪些测试文件的配置文件路径
        self.caseFile = os.path.join(path, "testCase")  # 测试断言文件路径
        self.caseList = []


    def set_case_list(self):
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):  # 如果data非空且不以#开头
                self.caseList.append(data.replace("\n", ""))  # 读取每行数据会将换行转换为\n，去掉每行数据中的\n
        fb.close()

    def set_case_suite(self):
        self.set_case_list()  # 通过set_case_list()拿到caselist元素组
        test_suite = unittest.TestSuite()
        suite_module = []
        for case in self.caseList:  # 从caselist元素组中循环取出case
            case_name = case.split("/")[-1]  # 通过split函数来将aaa/bbb分割字符串，-1取后面，0取前面
            print("执行:" + case_name + ".py")  # 打印出取出来的名称
            # 批量加载用例，第一个参数为用例存放路径，第一个参数为路径文件名
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            suite_module.append(discover)  # 将discover存入suite_module元素组
            # print('suite_module:' + str(suite_module))
        if len(suite_module) > 0:  # 判断suite_module元素组是否存在元素
            for suite in suite_module:  # 如果存在，循环取出元素组内容，命名为suite
                for test_name in suite:  # 从discover中取出test_name，使用addTest添加到测试集
                    test_suite.addTest(test_name)
        else:
            print('else:')
            return None
        return test_suite  # 返回测试集

    def run(self):
        try:
            suit = self.set_case_suite()  # 调用set_case_suite获取test_suite
            if suit is not None:  # 判断test_suite是否为空
                fp = open(resultPath, 'wb')  # 打开result/20181108/report.html测试报告文件，如果不存在就创建
                # 调用HTMLTestRunner
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                print("Have no case to test.")
        except Exception as ex:
            print(str(ex))
        finally:
            print("*********TEST END*********")

        # 判断邮件发送的开关
        if on_off == 'on':
            send_mail.send_email()
        else:
            print(on_off)
            print("邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告")

if __name__ == '__main__':
    AllTest().run()