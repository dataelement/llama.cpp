import random
from http import HTTPStatus
from dashscope import Generation
import dashscope
import json

dashscope.api_key = "sk-dummy"


def get_response(messages, tools):
    response = Generation.call(
        model='qwen-max',
        messages=messages,
        tools=tools,
        # seed=1234,
        temperature=0,
        stop=['✿RESULT✿', '✿RESULT✿:', '✿RESULT✿:\n'],
        result_format='message' # 将输出设置为message形式
    )
    return response


def test_qwen(input_file):
    body = json.load(open(input_file))
    response = get_response(body["messages"], body["tools"])
    print(response)


# test_qwen('./round1.json')
test_qwen('./round2.json')