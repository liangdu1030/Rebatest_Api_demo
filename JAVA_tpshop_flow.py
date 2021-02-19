#coding:utf-8
from common.configHttp import RunMain
from common.connect_db import OperationMysql
from Params.params import Basic
import jsonpath
import json
import functools
import os
from Log.logger import logger

order_sn = '' #订单号
store_id = '' #店铺id
order_id = '' #订单id
rec_id = '' #订单商品id
class Flow_all(object):

    def __init__(self):
        self.url_all = 'https://nicefoodtest.com'
        self.order_sn = None
        self.total_amount = None
        self.data = Basic()


    '''获取到json中任意key的值,结果为list格式'''
    def get_json_value(self, json_data, key_name):
        key_value = jsonpath.jsonpath(json_data, '$..{key_name}'.format(key_name=key_name))
        # key的值不为空字符串或者为empty（用例中空固定写为empty）返回对应值，否则返回empty
        return key_value

    '''登录'''
    def Login(self):
        result = RunMain().send_cookies('pc')
        if not result:
            logger.error("PC-Token获取失败,登录失败")
            logger.error(result)
            os._exit(0)
        else:
            logger.info("PC-Token获取成功")

    def check_login(func):
        '''装饰器获取Token'''
        @functools.wraps(func)
        def getlogin(self, *args, **kwargs):
            self.Login()
            return func(self, *args, **kwargs)
        return getlogin

    '''登录'''
    def Login_seller(self):
        result = RunMain().send_cookies('seller')
        if not result:
            logger.error("Seller-Token获取失败,登录失败")
            logger.error(result)
            os._exit(0)
        else:
            logger.info("Seller-Token获取成功")
            return result

    def check_login_seller(func):
        '''装饰器获取Token'''
        @functools.wraps(func)
        def getlogin(self, *args, **kwargs):
            self.Login_seller()
            return func(self, *args, **kwargs)
        return getlogin

    '''创建订单'''
    @check_login
    def order_class(self):
        global order_sn
        global store_id
        global order_id
        global rec_id
        type = 'post_cookies'
        url = self.url_all+str(self.data.url[0])
        result = RunMain().run_main(type, url, self.data.data, 'pc')
        order_sn = str(Flow_all().get_json_value(json.loads(result), 'order_sn')).replace(']', '').replace('[', '')\
            .replace("'", '')
        self.total_amount = Flow_all().get_json_value(json.loads(result), 'total_amount')
        order_sn_c = OperationMysql('bb2_order').search_one("SELECT order_sn FROM `bb2_order`.`order` "
                                                            " where order_sn = "+order_sn)
        res1 = str(Flow_all().get_json_value(order_sn_c, 'order_sn')).replace(']', '').replace('[', '') \
            .replace("'", '')
        store_id = str(Flow_all().get_json_value(json.loads(result), 'store_id')).replace(']', '').replace('[', '') \
            .replace("'", '')
        store_id_c = OperationMysql('bb2_order').search_one("SELECT store_id FROM `bb2_order`.`order` "
                                                            " where store_id = " + store_id)
        res2 = str(Flow_all().get_json_value(store_id_c, 'store_id')).replace(']', '').replace('[', '') \
            .replace("'", '')
        rec_id = str(Flow_all().get_json_value(json.loads(result), 'rec_id')).replace(']', '').replace('[', '') \
            .replace("'", '')
        if not order_sn and not self.total_amount:
            logger.error("创建订单失败")
            logger.error(result)
        elif res1 == order_sn and res2 == store_id:
            logger.info("创建订单成功")

if __name__ == '__main__':
    a = Flow_all()
    a.order_class()