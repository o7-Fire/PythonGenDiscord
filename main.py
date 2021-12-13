from hcapbypass import bypass
from generator import TokenGenerator
from discord_webhook import DiscordWebhook
import proxy_processor
import threading
import json
from itertools import cycle
import os
import time
import concurrent.futures
import shutil
#alive, idk
verbose = True
# how lmao
with open("webhooks.json") as whs:
    webhooks = json.loads(whs.read())
    
pool = cycle(webhooks)
genned = 0

def SendToken(token):
    global pool, webhooks, genned
    wh = next(pool)
    if wh == webhooks[0]:
        with open("webhooks.json") as whs:
            webhooks = json.loads(whs.read())
        pool = cycle(webhooks)
        wh = next(pool)
    webhook_url = wh
    webhook = DiscordWebhook(url=webhook_url, content=f'{token}')
    webhook.execute()
    with open('tokens.txt', 'a') as t:
        t.write(token + '\n')
    genned += 1

def GenerateToken(workerID):
    while True:
        try:
            proxy = proxy_processor.GetProxy()
            print("[{}] Used proxy: {}".format(workerID, proxy))
            gen = TokenGenerator(verbose, proxy, workerID)
            res = gen.GenerateToken()
            if 'token' in res:
                generatedToken = res["token"]
                print(("[{}] Generated Token: " + generatedToken).format(workerID))
                SendToken(generatedToken)
                break
            else: 
              print(res)
              print("[{}] Fail to get token, we get em next time".format(workerID))
        except Exception as e: #rate limit lmaooo
          print("[{}] Fail: {}".format(workerID,e))
          continue # https://cdn.discordapp.com/attachments/741160342595305596/911980859203129344/caption.gif
#[img]https://media.discordapp.net/attachments/741160342595305596/911980859203129344/caption.gif[/img]

def main():
    thread_list = []
    worker = 20
    print("Max Thread: " + str(worker))
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
      ra = range(15)#how many token you need
      ralen = len(ra)
      print("Generating: "+str(ralen))
      if(ralen == 1): #peak code optimization
        GenerateToken(1)#debug in main thread, wtf killed
        return #dont execute next line, wait does return exit the executor ?
      for i in ra: #ye i think so
        executor.submit(GenerateToken, i)# how come its not generating any tokens it should be
      print("Done generating task")

    """
    for i in range(300):
        thread = threading.Thread(target=GenerateToken, args=(), daemon=True)
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()
    """

if __name__ == '__main__':
  print("sanity check")
  t1 = threading.Thread(target=main)
  t1.start()# there got it to work
  while True: #randomize proxy, idiot
    #print("minutely sanity check")#lies
    time.sleep(5)#dont exit
# ay it seems to be working the exit door is there