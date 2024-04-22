
from openai import OpenAI
import json


def test_rag():
    client = OpenAI(
        api_key="dummy",
        base_url="http://127.0.0.1:9100/v1")
        
    documents = [
        { "title": "Tall penguins", "text": "Emperor penguins are the tallest growing up to 122 cm in height." }, 
        { "title": "Penguin habitats", "text": "Emperor penguins only live in Antarctica."}
    ]
    documents_str = json.dumps(documents, ensure_ascii=False)

    user_preamble = "## Task and Context\nYou help people answer their questions and other requests interactively. You will be asked a very wide array of requests on all kinds of topics. You will be equipped with a wide range of search engines or similar tools to help you, which you use to research your answer. You should focus on serving the user's needs as best you can, which will be wide-ranging.\n\n## Style Guide\nUnless the user asks for a different style of answer, you should answer in full sentences, using proper grammar and spelling."
    # instruct_str = "Carefully perform the following instructions, in order, starting each with a new line.\nFirstly, Decide which of the retrieved documents are relevant to the user's last input by writing 'Relevant Documents:' followed by comma-separated list of document numbers. If none are relevant, you should instead write 'None'.\nSecondly, Decide which of the retrieved documents contain facts that should be cited in a good answer to the user's last input by writing 'Cited Documents:' followed a comma-separated list of document numbers. If you dont want to cite any of them, you should instead write 'None'.\nThirdly, Write 'Answer:' followed by a response to the user's last input in high quality natural english. Use the retrieved documents to help you. Do not insert any citations or grounding markup.\nFinally, Write 'Grounded answer:' followed by a response to the user's last input in high quality natural english. Use the symbols <co: doc> and </co: doc> to indicate when a fact comes from a document in the search result, e.g <co: 0>my fact</co: 0> for a fact from document 0."
    instruct_str = "Write 'Answer:' followed by a response to the user's last input."
    system_content = "{}|<instruct>|{}||<documents>|{}".format(user_preamble, instruct_str, documents_str)
    conversation = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": "Whats the biggest penguin in the world?"}
    ]

    completion = client.chat.completions.create(
        model="command-r-plus-104b",
        messages=conversation,
        temperature=0.3,
        # tool_choice="none",
    )

    print('\n---Dailog round---')
    print(">>>Q: {}\n>>>Bot: {}".format(conversation[1]['content'],[completion.choices[0].message]))


test_rag()