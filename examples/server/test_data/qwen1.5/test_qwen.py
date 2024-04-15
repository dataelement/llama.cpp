import json
from openai import OpenAI

def test1(round):
    client = OpenAI(
        api_key="dummy",
        base_url="http://34.87.129.78:9301/v1")

    system_prompt = open("./qwen1.5_system.txt").read()
    u1 = "What is the capital of France?"
    a1 = 'The capital of France is Paris.'
    u2 = "What is the capital of Germany?"
    a2 = 'The capital of Germany is Berlin.'
    uf = open('./qwen1.5_u{}.txt'.format(round)).read()
    completion = client.chat.completions.create(
        model="qwen1.5-32b-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": u1},
            {"role": "assistant", "content": a1},
            {"role": "user", "content": u2},
            {"role": "assistant", "content": a2},
            {"role": "user", "content": uf}
        ],
        stop=['✿RESULT✿', '✿RESULT✿:', '✿RESULT✿:\n']
    )

    print('\n---Dailog round {}---'.format(round))
    print(">>>Q: {}\n>>>Bot: {}".format([uf], [completion.choices[0].message.content]))


def test2(round):
    client = OpenAI(
        api_key="dummy",
        base_url="http://34.87.129.78:9301/v1")
        
    body = json.load(open('./round{}_message.txt'.format(round)))
    completion = client.chat.completions.create(
        model="qwen1.5-32b-chat",
        messages=body["messages"],
        tools=body["tools"],
        # tool_choice="none",
    )

    print('\n---Dailog round {}---'.format(round))
    print(">>>Q: xxx\n>>>Bot: {}".format([completion.choices[0].message]))


def test_qwen_round(round):
    client = OpenAI(
        api_key="dummy",
        base_url="http://34.87.129.78:9301/v1")

    system_prompt = open("./qwen1.5_system.txt").read()
    user_prompt = open('./qwen1.5_u{}.txt'.format(round)).read()
    completion = client.chat.completions.create(
        model="qwen1.5-32b-chat",
        messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
        ],
        stop=['✿RESULT✿', '✿RESULT✿:', '✿RESULT✿:\n']
    )

    print('\n---Dailog round {}---'.format(round))
    print(">>>Q: {}\n>>>Bot: {}".format([user_prompt], [completion.choices[0].message.content]))


def test4(input_file):
    client = OpenAI(
        api_key="dummy",
        base_url="http://34.87.129.78:9301/v1")
        
    body = json.load(open(input_file))
    completion = client.chat.completions.create(
        model="qwen1.5-72b-chat",
        messages=body["messages"],
        tools=body["tools"],
        temperature=0,
        # tool_choice="none",
    )

    print('\n---Dailog round---')
    print(">>>Q: xxx\n>>>Bot: {}".format([completion.choices[0].message]))

# test1(1)
# test1(2)

# test2(1)
# test2(2)
# test2(3)

# test_qwen_round(1)
# test_qwen_round(2)
# test_qwen_round(3)
# test4('./round1.json')
test4('./round2.json')