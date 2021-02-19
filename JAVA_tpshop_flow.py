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
        url = self.url_all+self.data.url
        result = RunMain().run_main(type, url, self.data.data, 'pc')
        order_sn = str(Flow_all().get_json_value(json.loads(result), 'order_sn')).replace(']', '').replace('[', '')\
            .replace("'", '')
        self.total_amount = Flow_all().get_json_value(json.loads(result), 'total_amount')
        order_sn_c = OperationMysql('bb2_order').search_one("SELECT order_sn FROM `bb2_order`.`order` "
                                                            " where order_sn = "+order_sn)
        res1 = str(Flow_all().get_json_value(order_sn_c, 'order_sn')).replace(']', '').replace('[', '') \
            .replace("'", '')
        store_id = str(Flow_all().get_json_value(json.loads(result), 'store_id')[1]).replace(']', '').replace('[', '') \
            .replace("'", '')
        store_id_c = OperationMysql('bb2_order').search_one("SELECT store_id FROM `bb2_order`.`order` "
                                                            " where store_id = " + store_id)
        res2 = str(Flow_all().get_json_value(store_id_c, 'store_id')).replace(']', '').replace('[', '') \
            .replace("'", '')
        order_id = str(Flow_all().get_json_value(json.loads(result), 'order_id')[1]).replace(']', '').replace('[', '') \
            .replace("'", '')
        order_id_c = OperationMysql('bb2_order').search_one("SELECT order_id FROM `bb2_order`.`order` where order_id "
                                                            "= " + order_id)
        res3 = str(Flow_all().get_json_value(order_id_c, 'order_id')).replace(']', '').replace('[', '') \
            .replace("'", '')
        rec_id = str(Flow_all().get_json_value(json.loads(result), 'rec_id')).replace(']', '').replace('[', '') \
            .replace("'", '')
        if not order_sn and not self.total_amount:
            logger.error("创建订单失败")
            logger.error(result)
        elif res1 == order_sn and res2 == store_id and res3 == order_id:
            logger.info("创建订单成功")

    '''提交订单'''
    @check_login
    def order_sn_info(self):
        type = 'get_cookies'
        url = self.url_all + "/api/order/user?"
        data = 'order_sn='+order_sn
        result = RunMain().run_main(type, url, data, 'pc')
        pay_status = str(Flow_all().get_json_value(json.loads(result), 'pay_status')).replace(']', '').replace('[', '') \
            .replace("'", '')
        order_status = str(Flow_all().get_json_value(json.loads(result), 'order_status')).replace(']', '').replace('[', '') \
            .replace("'", '')
        store_id_confirm = str(Flow_all().get_json_value(json.loads(result), 'store_id')).replace(']', '').replace('[', '') \
            .replace("'", '')
        if pay_status != 1 and order_status != 0 and store_id_confirm != store_id:
            logger.error("提交订单失败  pay_status:"+pay_status+",order_status:"+order_status+",store_id:"+store_id)
            logger.error(result)
        else:
            logger.info("提交订单成功")

    '''商家确认订单'''
    @check_login_seller
    def order_sn_confirm(self):
        type = 'put_cookies'
        url = self.url_all + "/api/order/order_status/1"
        data = {"order_id": order_id,
                "store_id": store_id,
                "action_user": 14,
                "action_note": ""
                }
        result = RunMain().run_main(type, url, data, 'seller')
        status = str(Flow_all().get_json_value(json.loads(result), 'status')).replace(']', '').replace('[', '') \
            .replace("'", '')
        if status == '1':
            logger.info("商家确认订单成功")
        else:
            logger.error("商家确认订单失败  status:" + status)
            logger.error(result)

    '''商家已确认订单状态'''
    @check_login_seller
    def order_sn_confirm_seller(self):
        type = 'get_cookies'
        url = self.url_all + "/api/order/seller?"
        data = 'store_id='+store_id+'&order_sn='+order_sn
        result = RunMain().run_main(type, url, data, 'seller')
        pay_status = str(Flow_all().get_json_value(json.loads(result), 'pay_status')).replace(']', '').replace('[', '') \
            .replace("'", '')
        order_status = str(Flow_all().get_json_value(json.loads(result), 'order_status')).replace(']', '').replace('[',                                                                                    '') \
            .replace("'", '')
        shipping_status = str(Flow_all().get_json_value(json.loads(result), 'shipping_status')).replace(']', '').replace('[',                                                                                                     '') \
            .replace("'", '')
        if pay_status != 1 and order_status != '1' and shipping_status != 0:
            logger.error("商家已确认订单失败  pay_status:" + pay_status + ",order_status:" + shipping_status + ",shipping_status:" + shipping_status)
            logger.error(result)
        else:
            logger.info("商家已确认订单成功")

    '''商家订单发货'''
    @check_login_seller
    def order_deliver_goods(self):
        type = 'post_cookies'
        url = self.url_all + "/api/order/batch_delivery"
        data = {"store_id":store_id,"seller_id":14,"shipping_name":"null","shipping_code":"null","send_type":3,"note":"","store_address_id":"null","orders":[{"order_id":order_id,"order_sn":order_sn,"user_id":5,"master_order_sn":order_sn,"order_status":1,"pay_status":1,"shipping_status":0,"consignee":"ssssss","country":0,"province":38,"city":21298,"district":21579,"twon":64963,"address":"ALABAMAAutauga CountyAutaugaville36003","zipcode":"","mobile":"sssss","email":"1979635421@qq.com","shipping_code":"","shipping_name":"","shipping_price":6.99,"shipping_time":0,"pay_code":"","pay_name":"","invoice_title":"","taxpayer":"","goods_price":1.69,"user_money":8.85,"coupon_price":0,"integral":0,"integral_money":0,"order_amount":0,"total_amount":8.68,"paid_money":0,"tip_money":0.17,"tax_price":0,"add_time":1611977090,"confirm_time":0,"pay_time":1611977090,"transaction_id":"","prom_id":0,"prom_type":0,"order_prom_id":0,"order_prom_amount":0,"discount":0,"user_note":"","admin_note":"","parent_sn":"","store_id":store_id,"order_store_id":0,"is_comment":0,"shop_id":0,"deleted":0,"order_statis_id":0,"show_status":2,"shipping_time_desc":"","confirm_time_desc":"","consignee_desc":"ssssss:sssss","shipping_status_detail":"未发货","prom_type_desc":"普通订单","add_time_detail":"2021-01-29 22:24:50","pay_status_detail":"已支付","pay_status_refund_desc":"待处理","pay_time_detail":"2021-01-29 22:24:50","shipping_time_detail":"","order_goods":[{"rec_id":1587,"order_id":order_id,"goods_id":698,"goods_name":"日本AMANOYA天乃屋 歌舞伎扬日式米果 62g","goods_sn":"JYT0020","goods_num":1,"tax_price":0,"final_price":1.69,"goods_price":1.69,"cost_price":0,"member_goods_price":1.69,"give_integral":0,"spec_key":"","spec_key_name":"","bar_code":"125231224","is_comment":0,"prom_type":0,"prom_id":0,"is_send":0,"delivery_id":0,"sku":"4901035222923","store_id":store_id,"commission":0,"is_checkout":0,"deleted":0,"distribut":0,"shop_id":0,"goods_total":1.69,"unsend":0,"is_comment_desc":"未评价","checked":"true"}],"order_goods_count":1,"order_status_detail":"待发货","order_status_desc":"已确认","is_able_pay":"false","is_able_cancel":"true","is_able_cancel_pay":"true","is_able_receive":"false","is_able_comment":"false","is_able_shipping":"false","is_able_return":"false","is_able_invalid":"false","is_able_refund":"false","is_able_admin_refund":"false","is_able_confirm":"false","is_able_cancel_confirm":"true","is_able_delivery":"true","is_able_modify":"false","is_able_refund_back":"false","province_name":"ALABAMA","city_name":"Autauga County","district_name":"Autaugaville","total_goods_count":1,"unsend":0,"invoice_no":""}]}
        result = RunMain().run_main(type, url, data, 'seller')
        status = str(Flow_all().get_json_value(json.loads(result), 'status')).replace(']', '').replace('[', '') \
            .replace("'", '')
        if status == '1':
            logger.info("商家订单发货成功")
        else:
            logger.error("商家订单发货失败  status:" + status)
            logger.error(result)

    '''用户订单确认收货'''
    @check_login
    def user_deliver_confirm(self):
        type = 'put_cookies'
        url = self.url_all + "/api/order/order_status/2"
        data = {"order_id":order_id,"order_sn":order_sn,"user_id":5,"master_order_sn":"1395206050021408","order_status":1,"pay_status":1,"shipping_status":1,"consignee":"ssssss","country":0,"province":38,"city":21298,"district":21579,"twon":64963,"address":"ALABAMAAutauga CountyAutaugaville36003","zipcode":"","mobile":"sssss","email":"1979635421@qq.com","shipping_code":"null","shipping_name":"null","shipping_price":6.99,"shipping_time":1611985815,"pay_code":"","pay_name":"","invoice_title":"","taxpayer":"","goods_price":1.69,"user_money":8.85,"coupon_price":0,"integral":0,"integral_money":0,"order_amount":0,"total_amount":8.68,"paid_money":0,"tip_money":0.17,"tax_price":0,"add_time":1611970888,"confirm_time":0,"pay_time":1611970888,"transaction_id":"","prom_id":0,"prom_type":0,"order_prom_id":0,"order_prom_amount":0,"discount":0,"user_note":"","admin_note":"","parent_sn":"","store_id":13,"order_store_id":0,"is_comment":0,"shop_id":0,"deleted":0,"order_statis_id":0,"show_status":3,"shipping_time_desc":"2021_01-30 00:50:15","confirm_time_desc":"","consignee_desc":"ssssss:sssss","shipping_status_detail":"已发货","prom_type_desc":"普通订单","add_time_detail":"2021-01-29 20:41:28","pay_status_detail":"已支付","pay_status_refund_desc":"待处理","pay_time_detail":"2021-01-29 20:41:28","shipping_time_detail":"2021-01-30 00:50:15","order_goods":[{"rec_id":1593,"order_id":order_id,"goods_id":698,"goods_name":"日本AMANOYA天乃屋 歌舞伎扬日式米果 62g","goods_sn":"JYT0020","goods_num":1,"tax_price":0,"final_price":1.69,"goods_price":1.69,"cost_price":0,"member_goods_price":1.69,"give_integral":0,"spec_key":"","spec_key_name":"","bar_code":"1750691487","is_comment":0,"prom_type":0,"prom_id":0,"is_send":0,"delivery_id":0,"sku":"4901035222923","store_id":13,"commission":0,"is_checkout":0,"deleted":0,"distribut":0,"shop_id":0,"goods_total":1.69,"unsend":0,"is_comment_desc":"未评价"}],"order_goods_count":1,"store_name":"紀元商城","store_qq":"1354984","order_status_detail":"待收货","order_status_desc":"已确认","is_able_pay":"false","is_able_cancel":"false","is_able_cancel_pay":"false","is_able_receive":"true","is_able_comment":"false","is_able_shipping":"true","is_able_return":"true","is_able_invalid":"false","is_able_refund":"false","is_able_admin_refund":"false","is_able_confirm":"false","is_able_cancel_confirm":"false","is_able_delivery":"false","is_able_modify":"false","is_able_refund_back":"false","total_goods_count":1}
        result = RunMain().run_main(type, url, data, 'pc')
        status = str(Flow_all().get_json_value(json.loads(result), 'status')).replace(']', '').replace('[', '') \
            .replace("'", '')
        if status == '1':
            logger.info("用户订单确认收货成功")
        else:
            logger.error("用户订单确认收货失败  status:" + status)
            logger.error(result)

    '''用户评论订单'''
    @check_login
    def user_order_comment(self):
        type = 'post_cookies'
        url = self.url_all + "/api/order/order_comment"
        data = {"describe_score":4 ,"logistics_score":3 ,"seller_score":4 ,"order_id":order_id}
        result = RunMain().run_main(type, url, data, 'pc')
        status = str(Flow_all().get_json_value(json.loads(result), 'status')).replace(']', '').replace('[', '') \
            .replace("'", '')
        if status == '1':
            logger.info("用户评论订单成功")
        else:
            logger.error("用户评论订单失败  status:" + status)
            logger.error(result)

    '''用户提交申请售后退款'''
    @check_login
    def user_order_sales(self):
        type = 'post_cookies'
        url = self.url_all + "/api/order/return_goods"
        data = {"rec_id":rec_id,"type":0,"is_receive":0,"goods_num":1,"reason":"不喜欢/不想要","describe":"","evidence":1,"consignee":"xiaxia ","mobile":"15773027507","imgs":"https://nicefood-usa-goods-images.s3.us-east-2.amazonaws.com/nicefood-usa-goods-images/161216169568462689a5192b7a81971a6691eb2eb63a7.jpg"}
        result = RunMain().run_main(type, url, data, 'pc')
        status = str(Flow_all().get_json_value(json.loads(result), 'status')).replace(']', '').replace('[', '') \
            .replace("'", '')
        if status == -10079:
            logger.info("已经在申请退货中")
        elif status == 0:
            logger.info("用户提交申请售后退款失败 status:" + status)
            logger.error(result)
        else:
            logger.error("用户提交申请售后退款成功")

    '''获取商家售后退换订单信息'''
    @check_login
    def seller_order_sales(self):
        type = 'get_cookies'
        url = self.url_all + "/api/order/seller?"
        data = "order_id="+order_id
        result = RunMain().run_main(type, url, data, 'seller')
        shipping_status = str(Flow_all().get_json_value(json.loads(result), 'shipping_status')).replace(']', '').replace('[', '') \
            .replace("'", '')
        order_sn_s = str(Flow_all().get_json_value(json.loads(result), 'order_sn')).replace(']','').replace('[','') \
            .replace("'", '')
        if shipping_status != 1 and order_sn_s != order_sn:
            logger.info("获取商家售后退换订单信息失败 shipping_status:" + shipping_status + "order_sn:"+order_sn_s)
            logger.error(result)
        else:
            logger.error("获取商家售后退换订单信息成功")

    '''确认获取商家售后退换订单'''
    @check_login
    def seller_order_sales_confirm(self):
        type = 'put_cookies'
        url = self.url_all + "/api/order/return_goods/status/1"
        data = {"is_receive":0,"status":0,"type_desc":"仅退款","imgs_url":["https://nicefood-usa-goods-images.s3.us-east-2.amazonaws.com/nicefood-usa-goods-images/161216169568462689a5192b7a81971a6691eb2eb63a7.jpg"],"status_desc":"待审核","admin_status_desc":"无","refund_time_format":"","add_time_format":"2021-02-01 03:25:47","check_time_format":"","receive_time_format":"","is_can_agree_or_refuse":"true","is_can_return":"false","id":81,"rec_id":rec_id,"order_id":order_id,"order_sn":order_sn,"goods_id":698,"goods_num":1,"reason":"不喜欢/不想要","describe":"","evidence":"1","imgs":"https://nicefood-usa-goods-images.s3.us-east-2.amazonaws.com/nicefood-usa-goods-images/161216169568462689a5192b7a81971a6691eb2eb63a7.jpg","remark":"","user_id":5,"store_id":store_id,"spec_key":"","consignee":"xiaxia ","mobile":"15773027507","refund_integral":0,"refund_deposit":1.69,"refund_money":0,"refund_type":0,"refund_mark":"","refund_time":0,"type":0,"addtime":1612167947,"checktime":0,"receivetime":0,"canceltime":0,"gap":0,"gap_reason":"","seller_is_can_receive":"false"}
        result = RunMain().run_main(type, url, data, 'seller')
        status = str(Flow_all().get_json_value(json.loads(result), 'status')).replace(']', '').replace('[', '') \
            .replace("'", '')
        if status != 1:
            logger.info("确认获取商家售后退换订单失败 status:" + status +"  "+ order_sn +"  "+ store_id+"  " + order_id +"  "+ rec_id)
            logger.error(result)
        else:
            logger.error("确认获取商家售后退换订单成功")

if __name__ == '__main__':
    a = Flow_all()
    a.order_class()
    a.order_sn_info()
    a.order_sn_confirm()
    a.order_sn_confirm_seller()
    a.order_deliver_goods()
    a.user_deliver_confirm()
    a.user_order_comment()
    a.user_order_sales()
    a.seller_order_sales()
    a.seller_order_sales_confirm()