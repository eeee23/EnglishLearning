import requests

from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = '068152c763ca296d'
# 您的应用密钥
APP_SECRET = 'He98ZYN0sXW8dYz4Ry52exZQICWYlHwS'

# 合成音频保存路径, 例windows路径：PATH = "C:\\tts\\media.mp3"
PATH = '../python-pygame/media.mp3'

def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)


def saveFile(res):
    contentType = res.headers['Content-Type']
    if 'audio' in contentType:
        fo = open("../python-pygame/media.mp3", 'wb')
        fo.write(res.content)
        fo.close()
        print('save file path: ' + PATH)
    else:
        print(str(res.content, 'utf-8'))

def createRequest(que):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    q = que
    voiceName = 'youxiaoying'
    format = 'mp3'

    data = {'q': q, 'voiceName': voiceName, 'format': format}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/ttsapi', header, data, 'post')
    saveFile(res)