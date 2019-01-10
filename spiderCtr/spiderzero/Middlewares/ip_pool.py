# -*- coding: utf-8 -*-
import requests
import random
import json

class Ip_Pool(object):
    
    def process_request(self,request,spider):
        url = 'http://ip.16yun.cn:817/myip/pl/4d1d189c-38b9-4115-aa14-42875a5688b3/?s=kdnmqfihlw&u=devillove085&format=json'
        res = requests.get(url)
        a = json.loads(res.text)
        b = a.get("proxy")
        
        proxy = random.choice(b)

        ip = proxy.get("ip")
        port = proxy.get("port")

        request.meta['proxy'] = "http://" + str(ip) + ":" + str(port)