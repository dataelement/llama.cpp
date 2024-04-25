import threading
from openai import OpenAI
import argparse
import json
from tqdm import tqdm


def batch_call(bodys, api_url, model_name, result_file):
    client = OpenAI(
    api_key="dummy",
    base_url=api_url)

    with open(result_file, 'w') as fout:
        for body in tqdm(bodys):
            # print('---\n', json.dumps(body, ensure_ascii=False, indent=2))
            completion = client.chat.completions.create(
                model=model_name,
                messages=body['messages'],
                tools=body['tools'],
                temperature=0.3)

            result = {'input': body, 'output': completion.choices[0].message.dict()}
            fout.write(json.dumps(result, ensure_ascii=False) + "\n")


def trans_conv_oai_request(conv):
    requests = []
    tools = []
    for tool in json.loads(conv['tools']):
        name = tool['name']
        desc = tool['description']
        parameters = {}
        parameters['type'] = 'object'
        parameters['properties'] = {}
        ori_required = tool['parameters'].get('required', [])
        required = []
        for prop_key, prop_value in tool['parameters']['properties'].items():
            if prop_value['type'] in ['string', 'number', 'boolean', 'integer', 'int', 'float']:
                parameters['properties'][prop_key] = prop_value
                if prop_key in ori_required:
                    required.append(prop_key)

            elif prop_value['type'] == 'array':
                # escape the nested object in array
                # todo: flattern the list[object] to list[k1], list[k2]
                if prop_value['items']['type'] in ['string', 'number', 'boolean', 'integer', 'int', 'float']:
                    parameters['properties'][prop_key] = prop_value
                    if prop_key in ori_required:
                        required.append(prop_key)

            elif prop_value['type'] == 'object':
                # flatten the nested object for the command-r func call
                # not support the nested nested object parameter
                # Special case: e.g. {'type': 'object', 'description': 'The graph represented as an adjacency matrix'}
                if 'properties' not in prop_value and 'description' in prop_value:
                    parameters['properties'][prop_key] = prop_value
                    if prop_key in ori_required:
                        required.append(prop_key)
                    continue
                # Normal case: e.g. {'type': 'object', 'properties': {'a': {'type': 'string', 'description': 'desc'}}}    
                for sub_prop_key, sub_prop_value in prop_value['properties'].items():
                    if sub_prop_value['type'] == 'object':
                        print('ERROR: not support the nested nested object parameter')
                        continue

                    parameters['properties'][sub_prop_key] = sub_prop_value
                    if sub_prop_key in prop_value.get('required', []):
                        required.append(sub_prop_key)
            else:
                pass
        
        if required:
            parameters['required'] = required

        tool_def = {"type": "function", "function": {"name": name, "description": desc, "parameters": parameters}}
        tools.append(tool_def)

    if not tools:
        return []
    
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

def perf(test_data, api_url, model_name, num_parallel, cnt, seed):
    conversations = json.load(open(test_data))[seed:seed + cnt]
    bodys = []
    for coversation in conversations:
        bodys.extend(trans_conv_oai_request(coversation))
    
    n = len(bodys)
    print('Total requests: {}'.format(n))
    if num_parallel == 1:
        bodys = bodys
        result_file = f'./outputs/result_single_{n}.txt'
        batch_call(bodys, api_url, model_name, result_file)
    else:
        batch_size = (n + 1) // num_parallel
        if batch_size == 0:
            batch_size = 1

        threads = []
        for i in range(0, n, batch_size):
            result_file = './outputs/result_batch_{0}_{1}.txt'.format(n, i)
            batch_bodys = bodys[i: i + batch_size]
            threads.append(threading.Thread(target=batch_call, args=(batch_bodys, api_url, model_name, result_file)))
        
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
    parser.add_argument('-c', '--cnt', type=int, required=False, default=1000, help="run count")
    parser.add_argument('-s', '--seed', type=int, required=False, default=0, help="seed")
    
    args = parser.parse_args()
    perf(args.test_data, args.api_url, args.model_name, args.num_parallel, args.cnt, args.seed)

if __name__ == '__main__':
   main()