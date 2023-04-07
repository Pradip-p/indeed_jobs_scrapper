import requests
import json

from requests.auth import HTTPProxyAuth
from itertools import cycle
from fake_useragent import UserAgent
ua = UserAgent()


def get_proxies(): 
    payload ={
    "username": "",
    "country": "Random",
    "hostname": "ip",
    "ssl": "http",
    "sticky": "sticky",
    "format": "username:password:hostname:port",
    "quantity": "1000"
}

    url = ''
    headers = {'Authorization':''}
    response = requests.post(url,headers=headers,data=json.dumps(payload))
    return response.json()
def formatted():
    jsn = get_proxies()
    passwords = [p.split(':')[1]for p in jsn.get('data').get('formatted_proxy_list')]
    
    host = jsn['data']['proxy_host']
    port = jsn['data']['proxy_port']
    username = jsn['data']['proxy_username']
    password = jsn['data']['proxy_password']
    f_proxies = []
    for pas in passwords:
        formatted_proxy = username+':'+pas+'@'+host+':'+port
        proxy = {'http':'http://'+formatted_proxy,'https':'https://'+formatted_proxy}
        f_proxies.append(proxy)
    return f_proxies
    
all_proxies = formatted()

def get_response(link,all_proxies=all_proxies):
        
        
    header = {'Host': 'au.linkedin.com', 'User-Agent': ua.Chrome, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br'}
    proxy_pool = cycle(all_proxies)
    for p in range(1,11):
        
        proxy = next(proxy_pool)
        s = requests.Session()
        s.proxies = proxy
        username = ''
        password = proxy['http'].split('@')[0].split(':')[-1]
        auth = HTTPProxyAuth(username, password)
        s.auth = auth
        s.headers = header
        try:
            print('trying',proxy)
            response = s.get(link,timeout=6)
            if response.status_code==200:
                return response.text
                break
        except:
            continue
