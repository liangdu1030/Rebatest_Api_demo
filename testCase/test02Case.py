import json
import unittest
from common.configHttp import RunMain
import paramunittest
import geturlParams as geturlParams
import urllib.parse
import readExcel as readExcel

url = geturlParams.geturlParams().get_Url()
login_xls = readExcel.readExcel().get_xls('userCase.xlsx','login')

@paramunittest.parametrized(*login_xls)
class testUserLogin(unittest.TestCase):
    def setParameters(self, case_name, path, query, method):
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = str(query)
        self.method = str(method)

    def description(self):
        self.case_name

    def setUp(self):
        print(self.case_name + "测试开始前准备")

    def test01case(self):
        self.checkResult()

    def tearDown(self):
        print("测试结束，输出log完结\n\n")

    def checkResult(self):  # 断言
        new_url = url + self.path
        info = RunMain().run_main(self.method, new_url, json.loads(self.query))  # 根据Excel中的method调用run_main来进行requests请求，并拿到响应
        ss = json.loads(info)  # 将响应转换为字典格式
        if self.case_name == 'order_class':  # 如果case_name是login，说明合法，返回的code应该为200
            self.assertEqual(ss['token_type'], "bearer")
if __name__ == '__main__':
    unittest.main()