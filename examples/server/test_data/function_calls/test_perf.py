import threading
from openai import OpenAI
import argparse
import json


def batch_call(bodys, api_url, model_name):
    client = OpenAI(
    api_key="dummy",
    base_url=api_url)

    for body in bodys:
        print(json.dumps(body, ensure_ascii=False, indent=2))
        print('\n---')
        print(">>>Q: {}".format(body['messages']))

        completion = client.chat.completions.create(
            model=model_name,
            messages=body['messages'],
            tools=body['tools'],
            temperature=0.3)

        print(">>>A: {}".format(completion.choices[0].message.content))
        print(">>>Tools: {}".format(completion.choices[0].message.tool_calls))


def trans_conv_oai_request(conv):
    requests = []
    tools = []
    for tool in json.loads(conv['tools']):
        name = tool['name']
        desc = tool['description']
        parameters = {}
        parameters['type'] = 'object'
        parameters['properties'] = {}
        for prop_key, prop_value in tool['parameters']['properties'].items():
            if prop_value['type'] in ['string', 'number', 'boolean', 'array', 'integer', 'int', 'float']:
                parameters['properties'][prop_key] = prop_value
            elif prop_value['type'] == 'array':
                parameters['properties'][prop_key] = prop_value
            elif prop_value['type'] == 'object':
                # flatten the nested object for the command-r func call
                # not support the nested nested object parameter
                for sub_prop_key, sub_prop_value in prop_value['properties'].items():
                    if sub_prop_value['type'] == 'object':
                        print('ERROR: not support the nested nested object parameter')
                        continue

                    parameters['properties'][sub_prop_key] = sub_prop_value
            else:
                pass

        tool_def = {"type": "function", "function": {"name": name, "description": desc, "parameters": parameters}}
        tools.append(tool_def)

    request = {}
    request['tools'] = tools
    request['messages'] = []
    
    for diag in conv['conversations']:
        role, value = diag['from'], diag['value']
        if role == 'human':
            request['messages'].append({'role': 'user', 'content': value})
        elif role == 'gpt':
            request['messages'].append({'role': 'assistant', 'content': value})
        elif role == 'function_call':
            requests.append(request)
            break

    return requests

def perf(test_data, api_url, model_name, num_parallel):
    if num_parallel == 1:
        conversations = json.load(open(test_data))
        for coversation in conversations[50:100]:
            bodys = trans_conv_oai_request(coversation)
            batch_call(bodys, api_url, model_name)
    else:
        n = len(conversations)
        batch_size = (n + 1) // num_parallel
        threads = []
        for i in range(0, n, batch_size):
            threads.append(
                threading.Thread(target=trans_conv_oai_request, args=((conversations[i: i + batch_size],)))
            )
        
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model-name', type=str, required=False, default='command-r-plus-104b', help='model name')
    parser.add_argument('-u', '--api-url', type=str, required=False, default='http://127.0.0.1:9100/v1', help='api url')
    parser.add_argument('-d', '--test-data', type=str, required=False, default='glaive_toolcall_10k.json', help='test data')
    parser.add_argument('-n', '--num-parallel', type=int, required=False, default=1, help="num parallel")
    
    args = parser.parse_args()
    perf(args.test_data, args.api_url, args.model_name, args.num_parallel)

if __name__ == '__main__':
   main()