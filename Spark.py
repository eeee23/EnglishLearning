from SparkApi import *
appid = "8a41eee4"
api_secret = "NWUwYTY3ZmU5ZWI0ZTU3Mjk2YTI4MWE3"
api_key ="ce27261e0616d4fb2fd70714d50b1ff8"

domain = "generalv3"
#云端环境的服务地址
Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"


text =[]

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    


# if __name__ == '__main__':
#     text.clear
#     while(1):
#         Input = input("\n" +"我:")
#         question = checklen(getText("user",Input))
#         SparkApi.answer =""
#         print("星火:",end = "")
#         SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
#         getText("assistant",SparkApi.answer)
#         print(str(text))

