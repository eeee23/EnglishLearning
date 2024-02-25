import jieba
import requests
import tkinter
import json
import hashlib
import uuid
import time
import os
from lists import *
from Spark import *
def sha256_hash(message):
    sha256 = hashlib.sha256()
    sha256.update(message.encode('utf-8'))
    hash_value = sha256.hexdigest()
    return hash_value
def translate(inp):
    if inp == "":
        return "请输入字符！"
    else:
        utf8_inp = inp.encode('utf-8')
        muuid = uuid.uuid4()
        time_curtime = int(time.time())
        data = {
            'q':utf8_inp,
            'from':"auto",
            'to':"zh-CHS",
            'appKey':'22acb47021df3744',
            'salt':muuid,
            'sign':sha256_hash("22acb47021df3744"+inp+str(muuid)+str(time_curtime)+"3iEiyiP8Fj8KHmUmUkriMG8T62dxzI9I"),   # 签名
            'signType':"v3",
            'curtime':time_curtime,
        }
        r = requests.get("https://openapi.youdao.com/api",params=data).json()
        return "翻译为："+r["translation"][0]