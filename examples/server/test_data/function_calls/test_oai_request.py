from openai import OpenAI
import argparse
import json


def batch_call(bodys, api_url, model_name):
    client = OpenAI(api_key="dummy", base_url=api_url)

    for body in bodys:
        print(json.dumps(body, ensure_ascii=False, indent=2))
        print('\n---')
        print(">>>Q: {}".format(body['messages']))

        completion = client.chat.completions.create(
            model=model_name,
            messages=body['messages'],
            tools=body['tools'],
            tool_choice='none',
            temperature=0.3)

        print(">>>A: {}".format(completion.choices[0].message.content))
        print(">>>Tools: {}".format(completion.choices[0].message.tool_calls))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model-name', type=str, required=False, default='command-r-plus-104b', help='model name')
    parser.add_argument('-u', '--api-url', type=str, required=False, default='http://127.0.0.1:9100/v1', help='api url')
    parser.add_argument('-d', '--test-data', type=str, required=False, default='case1.json', help='test data')
    
    args = parser.parse_args()
    bodys = [json.load(open(args.test_data))]
    batch_call(bodys, args.api_url, args.model_name)


if __name__ == '__main__':
   main()