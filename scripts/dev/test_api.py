
import threading
import requests
import time

def test1():
  from openai import OpenAI
  client = OpenAI(
    api_key="DUMMY_API_KEY",
    base_url="http://127.0.0.1:9300/v1")
  
  completion = client.chat.completions.create(
    #model="qwen1.5-110b-chat",
    model="command-r-plus",
    messages=[
      {"role": "system", "content": "You are a helpful assistant"},
      {"role": "user", "content": "你是谁"}
    ],
    temperature=0.85,
    top_p=0.8)

  print(completion.choices[0].message)


def test2():
    api_key = "DUMMY"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = dict(
      model="qwen1.5-72b-chat",
      # model="command-r-plus-104b",
      messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "你是谁"}
      ],
      temperature=0.85, # 如果没有额外指定，请设置这个参数为0.85
      top_p=0.8)        # 如果没有额外指定，请设置这个参数为0.8


    internal_url = 'http://127.0.0.1:9300/v1/chat/completions'
    response = requests.post(internal_url, json=data, headers=headers)
    print(response.json())


def perf():
    threads = []
    for i in range(0, 10):
        threads.append(threading.Thread(target=test2))
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


#test1()
# test2()
perf()
