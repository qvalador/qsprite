import time
import os
import asyncio
from conf import debug, basedir

while True:
    if debug:
        n = 0
    else:
        n = 5
    os.system("python3 " + basedir + "\\bot.py")
    print("the bot died, restarting in 5")
    time.sleep(n)