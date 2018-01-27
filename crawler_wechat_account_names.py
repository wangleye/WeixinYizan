#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import urllib.parse
import urllib.request as urlrequest
import os.path
import os
import time
from random import randint
import socket
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

socket.setdefaulttimeout(2*60) # wait for maximum two miniutes for downloading the file
PROXY_FILE = './proxies.csv'

ACCOUNTS = set()

with open(PROXY_FILE) as input_proxy_file:
    proxy_list = []
    for line in input_proxy_file:
        proxy_ip, proxy_port = line.split('\t')
        proxy_list.append("{}:{}".format(proxy_ip, proxy_port))

keyword_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x', 'y','z']

currentTime = datetime.now()
time_str = currentTime.strftime("%Y-%m-%d-%H-%M-%S")
print("crawl {}...".format(time_str))

for keyword in keyword_list:
    for proxy_url in proxy_list:
        try:
            print("try use proxy {} ...".format(proxy_url))
            if proxy_url != 'no':
                # create the object, assign it to a variable
                proxy = urlrequest.ProxyHandler({'https': proxy_url})
                # construct a new opener using your proxy settings
                opener = urlrequest.build_opener(proxy)
            else:
                opener = urlrequest.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
            # install the openen on the module-level
            urlrequest.install_opener(opener)
            print(keyword, "...")
            count = 1
            keyword_accounts = set()
            while True:
                params = urllib.parse.urlencode({'keyword': keyword, 'page':count}).encode('ascii')
                keyword_search_url = "http://web.yeezan.com/api/addispatch/mp_keyword_search"
                response = urlrequest.urlopen(keyword_search_url, params)
                search_results = json.loads(response.read().decode('utf-8'))
                old_size = len(keyword_accounts)
                for each_account in search_results['data']['list']:
                    keyword_accounts.add(each_account['mp_weixin_id'])
                if len(keyword_accounts) == old_size: # no new account, break
                    break
                print(len(keyword_accounts))
                count += 1
            break
        except Exception as e:
            print(e)
            print("exception, try again...")
    ACCOUNTS = ACCOUNTS.union(keyword_accounts)

with open("accounts", 'w') as outputfile:
    for acc in ACCOUNTS:
        outputfile.write('{}\n'.format(acc))
