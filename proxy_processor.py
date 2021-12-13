from itertools import cycle
import random

def GetProxies():
    with open('proxies.txt', 'r') as temp_file:
        proxies = [line.rstrip('\n') for line in temp_file]
        random.shuffle(proxies)
        return proxies

#it should work ok it does
proxies = GetProxies()
proxy_pool = cycle(proxies)

def GetProxy():
    proxy = next(proxy_pool)
    if len(proxy.split(':')) == 4:
        splitted = proxy.split(':')
        return f"{splitted[2]}:{splitted[3]}@{splitted[0]}:{splitted[1]}"
    
    return proxy