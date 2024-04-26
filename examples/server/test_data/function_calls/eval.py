from openai import OpenAI
import argparse
import json
from tqdm import tqdm
import os
import requests


def infer(body, api_url, model_name):
    client = OpenAI(api_key="dummy", base_url=api_url)

    completion = client.chat.completions.create(
        model=model_name,
        messages=body['messages'],
        tools=body['tools'],
        tool_choice='none',
        temperature=0.3)
    
    message = completion.choices[0].message
    return message 


def post_infer(body, api_url, model_name):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_OPENAI_API_KEY_HERE"
    }
    payload = dict(
        model=model_name,
        messages=body['messages'],
        tools=body['tools'],
        tool_choice='none',
        temperature=0.3
    )
    ep = '/chat/completions'
    response = requests.post(api_url + ep, json=payload, headers=headers)
    print(response.text)

    return response


def trans_conv_oai_request(dialogs, filter_system=False):
    tools = dialogs['tools']
    messages = dialogs['messages']
    # messages cates: user, system, assistant, assistant with tool calls, tool result message
    # abbreviate: u, s, a, f, t
    # diag split logic: case 1. suau -> f case2. suauft -> a 
    requests = []
    request = {}
    request['tools'] = tools
    request['messages'] = []
    one_round_messages = []
    for m in messages:
        if filter_system and m['role'] == 'system':
            continue

        if m['role'] in ['user', 'system', 'tool']:
            one_round_messages.append(m)
        elif m['role'] == 'assistant':
            request['messages'] = one_round_messages[:]
            requests.append(request)
            one_round_messages.append(m)
            request = {}
            request['tools'] = tools
            request['messages'] = []

    return requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model-name', type=str, required=False, default='command-r-plus-104b', help='model name')
    parser.add_argument('-u', '--api-url', type=str, required=False, default='http://127.0.0.1:9100/v1', help='api url')
    parser.add_argument('-d', '--test-data', type=str, required=False, default='./function_call_agent_dataset', help='test data')
    
    # step 1. process the data
    convs_out_file = './outputs/func_call_ageent_oai_convs.jsonl'
    args = parser.parse_args()
    files = os.listdir(args.test_data)
    print('files:', files)
    all_bodys = []
    for file in files:
        file_path = os.path.join(args.test_data, file)
        dialogs = json.load(open(file_path))       
        bodys = trans_conv_oai_request(dialogs, True)
        all_bodys.extend(bodys)

    print('Total requests: {}'.format(len(all_bodys)))
    # with open(convs_out_file, 'w') as f:
    #     for body in tqdm(all_bodys):
    #         f.write(json.dumps(body, ensure_ascii=False) + '\n')

    # step 2. infer the data
    result_file = './outputs/func_call_ageent_pred_local_command_r_plus_v2.jsonl'
    outs = []
    for body in tqdm(all_bodys):
        response = infer(body, args.api_url, args.model_name)
        outs.append(response.dict())

    with open(result_file, 'w') as f:
        for out in tqdm(outs):
            f.write(json.dumps(out, ensure_ascii=False) + '\n')


if __name__ == '__main__':
   main()