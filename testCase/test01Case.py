import json
import unittest
from common.configHttp import RunMain
import paramunittest
import geturlParams as geturlParams
from common.Assert import Assertions
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
        # new_url_data = new_url + "?" + self.query
        # data1 = dict(urllib.parse.parse_qsl(
        #     urllib.parse.urlsplit(new_url_data).query))  # 将一个完整的URL中的name=&pwd=转换为{'name':'xxx','pwd':'bbb'}
        if self.method == 'post_cookies' or self.method == 'post':
            info = RunMain().run_main(self.method, new_url, json.loads(self.query), 'pc')  # 根据Excel中的method调用run_main来进行requests请求，并拿到响应
        elif self.method == 'get_cookies' or self.method == 'get':
            info = RunMain().run_main(self.method, new_url, self.query, 'pc')
        ss = json.loads(info)  # 将响应转换为字典格式
        #提交订单
        if self.case_name == 'order_class':
            Assertions.assert_body(self, ss, 'status', 2)
        # #获取订单号
        # if self.case_name == 'order_sn':
        #     self.assertTrue(ss['user_money'])
        # #获取用户订单
        # if self.case_name == 'order_user':
        #     self.assertTrue(ss['brand_id'])
        # #取消订单
        # if self.case_name == 'cancel_order':
        #     self.assertEqual(ss['msg'], '成功')
        # #新增地址
        # if self.case_name == 'address':
        #     self.assertEqual(ss['msg'], '成功')
if __name__ == '__main__':
    unittest.main()