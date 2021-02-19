import readConfig as readConfig

readconfig = readConfig.ReadConfig()

class geturlParams():
    def get_Url(self):
        # 执行用例时需要调用这个地址  是你的接口地址
        new_url = readconfig.get_http('scheme') + "://" + readconfig.get_http("baseurl")
        return new_url

if __name__ == '__main__':
    print(geturlParams().get_Url())