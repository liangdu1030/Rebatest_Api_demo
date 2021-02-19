#coding:utf-8
import jsonpath
import requests
import json
import os
from Params.params import Login
from Log.logger import logger
from common.verification_code import ver_code


class RunMain():

    def __init__(self):
        self.url_all = 'https://nicefoodtest.com'
        self.data = Login()

    def get_json_value(self, json_data, key_name):
        '''获取到json中任意key的值,结果为list格式'''
        key_value = jsonpath.jsonpath(json_data, '$..{key_name}'.format(key_name=key_name))
        # key的值不为空字符串或者为empty（用例中空固定写为empty）返回对应值，否则返回empty

        return key_value


    def send_post(self, url, data):
        result = requests.post(url=url, json=data).json()
        res = json.dumps(result,ensure_ascii=False, sort_keys=True, indent=2)
        return res

    def send_cookies(self, type):
        if type == 'pc':
            result = RunMain().run_main('post', self.url_all+ str(self.data.url[0]),
                                        {"password": "519475228fe35ad067744465c42a19b2", "verification": ver_code(),
                                         "email": "1979635421@qq.com"})

        elif type == 'seller':
            result = RunMain().run_main('post', 'https://nicefoodtest.com/api/seller/login',
                                        {"seller_name": "jysc",
                                         "password": "519475228fe35ad067744465c42a19b2",
                                         "verification": ver_code()})

        elif type == 'admin':
            result = RunMain().run_main('post', 'https://nicefoodtest.com/api/user/login',
                                        {"password": "519475228fe35ad067744465c42a19b2", "verification": ver_code(),
                                         "email": "1979635421@qq.com"})
        token_string = RunMain().get_json_value(json.loads(result), 'access_token')
        if token_string==False:
            logger.error("Token获取失败")
            os._exit(0)
        else:
            return token_string

    def send_post_login(self, url, data, type):
        headers = {
                "Authorization": "Bearer {}".format(str(RunMain().send_cookies(type)).replace(']', '').replace('[', '').replace("'", '')),
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        result = requests.post(url=url, json=data, headers=headers).json()
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res

    def send_get_login(self, url, data, type):
        headers = {
                "Authorization": "Bearer {}".format(str(RunMain().send_cookies(type)).replace(']', '').replace('[', '').replace("'",'')),
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        result = requests.get(url=url, params=data, headers=headers).json()
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res

    def send_put_login(self, url, data, type):
        headers = {
                "Authorization": "Bearer {}".format(str(RunMain().send_cookies(type)).replace(']', '').replace('[', '').replace("'",'')),
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        result = requests.put(url=url, json=data, headers=headers).json()
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res

    def send_get(self, url, data, headers=None):
        result = requests.get(url=url, params=data, headers=headers).content.decode(encoding='utf8')
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res

    def run_main(self, method, url=None, data=None, type=None):
        result = None
        if method == 'post':
            result = self.send_post(url, data)
        elif method == 'get':
            result = self.send_get(url, data)
        elif method == 'post_cookies':
            result = self.send_post_login(url, data, type)
        elif method == 'put_cookies':
            result = self.send_put_login(url, data, type)
        elif method == 'get_cookies':
            result = self.send_get_login(url, data, type)
        else:
            print("method值错误")
        return result
#
if __name__ == '__main__':
#     # 这个类吧get和post请求给封装了
    # 模拟一次get
    # # result2 = RunMain().run_main('get', 'https://nicefoodtest.com/pc/index', ) # 模拟一次post


    result1 = RunMain().run_main('put_cookies', 'https://nicefoodtest.com/api/order/return_goods/status/1',
                                 {"is_receive":0,"status":0,"type_desc":"仅退款","imgs_url":["https://nicefood-usa-goods-images.s3.us-east-2.amazonaws.com/nicefood-usa-goods-images/161216169568462689a5192b7a81971a6691eb2eb63a7.jpg"],"status_desc":"待审核","admin_status_desc":"待处理","refund_time_format":"","add_time_format":"2021-01-29 22:24:50","check_time_format":"","receive_time_format":"","is_can_agree_or_refuse":"true","is_can_return":"false","id":79,"rec_id":1631,"order_id":1565,"order_sn":"1395618249441344","goods_id":698,"goods_num":1,"reason":"不喜欢/不想要","describe":"","evidence":"1","imgs":"https://nicefood-usa-goods-images.s3.us-east-2.amazonaws.com/nicefood-usa-goods-images/161216169568462689a5192b7a81971a6691eb2eb63a7.jpg","remark":"","user_id":5,"store_id":13,"spec_key":"","consignee":"xiaxia ","mobile":"15773027507","refund_integral":0,"refund_deposit":1.69,"refund_money":0,"refund_type":0,"refund_mark":"","refund_time":0,"type":0,"addtime":1612167538,"checktime":0,"receivetime":0,"canceltime":0,"gap":0,"gap_reason":"","seller_is_can_receive":"false"}, 'seller')
    # #result1 = RunMain().run_main('post_cookies', result)  # 模拟一次get
#     #
#     data = {"original_img":"/public/upload/store/1/goods/2021/2-1/1612172476898.png","is_free_shipping":"1","cat_id1":1,"cat_id2":2,"cat_id3":10,"video":"","spec_image":[],"store_count":22,"cat_name":"手机/运营商/数码 ➣ 手机通讯王企鹅请问 ➣ 手机","goods_name":"李伟怡傻逼东西","brand_id":0,"shop_price":"11","market_price":"22","goods_content":"","goods_images":[],"store_cat_id1":"","store_cat_id2":"","goods_attrs":[]}
#     result1 = RunMain().run_main('post_cookies', 'http://192.168.0.110:8082/mall/goods',
#                                  data, 'seller')
    print(result1)