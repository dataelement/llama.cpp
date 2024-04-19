from openai import OpenAI
import cohere
import requests
import json


def test1():
  client = OpenAI(
    api_key="DUMMY_API_KEY",
    base_url="http://127.0.0.1:9100/v1")

  completion = client.chat.completions.create(
    model="command-r-plus-104b",
    messages=[
      {"role": "user", "content": "Hello, how are you?"}
    ],
    temperature=0.3)

  print(completion.choices[0].message)


def test2(prompt_file):
  client = OpenAI(api_key="dummy", base_url="http://127.0.0.1:9100/v1")
  prompt = open(prompt_file).read()
  comp = client.completions.create(
    model="command-r-plus-104b",
    prompt=prompt,
    temperature=0.3
  )
  print('Bot: {}'.format([comp.content]))


def test30():
  url = 'http://127.0.0.1:9100/v1/chat'
  payload = dict(
    model="command-r-plus-104b",
    chat_history=[
      {"role": "USER", "message": "Who discovered gravity?"},
      {"role": "CHATBOT", "message": "The man who is widely credited with discovering gravity is Sir Isaac Newton"}
    ],
    message="What year was he born?",
    stream=False,
  )
  response = requests.post(url, json=payload)
  print(response.text)


def test3():
  co = cohere.Client('DUMMY_API_KEY', base_url='http://127.0.0.1:9100/v1')
  response = co.chat(
    model="command-r-plus-104b",
    chat_history=[
      {"role": "USER", "message": "Who discovered gravity?"},
      {"role": "CHATBOT", "message": "The man who is widely credited with discovering gravity is Sir Isaac Newton"}
    ],
    message="What year was he born?",
  )

  print(response)


def test4(input_file):
    client = OpenAI(
        api_key="dummy",
        base_url="http://127.0.0.1:9100/v1")
        
    body = json.load(open(input_file))
    completion = client.chat.completions.create(
        model="command-r-plus-104b",
        messages=body["messages"],
        tools=body["tools"],
        temperature=0.3,
        # tool_choice="none",
    )

    print('\n---Dailog round---')
    print(">>>Q: xxx\n>>>Bot: {}".format([completion.choices[0].message]))

#test1()
#test2('raw_prompt1.txt')
#test2('raw_prompt2.txt')
#test2('raw_prompt3.txt')

#test30()
#test3()

test4('./oai_round1_message.txt')   
test4('./oai_round2_message.txt')   
# test4('./oai_round3_message.txt')