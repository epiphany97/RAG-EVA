from langchain.prompts import PromptTemplate
import boto3
import pprint
from botocore.client import Config
from langchain.llms.bedrock import Bedrock
import json
from retreival import get_bedrock_agent_client, retrieve

pp = pprint.PrettyPrinter(indent=2)
# ["cohere.command-text-v14", "ai21.j2-ultra-v1", "amazon.titan-text-express-v1", "amazon.titan-text-lite-v1", "ai21.j2-mid-v1", "anthropic.claude-v2:1"]
parameters = {
    "anthropic.claude-instant-v1":{},
    "anthropic.claude-v2:1":{},
    "anthropic.claude-v2":{},
    "anthropic.claude-3-sonnet-20240229-v1:0":{},
    "anthropic.claude-3-haiku-20240307-v1:0":{},
    "ai21.j2-mid-v1":{},
    "ai21.j2-ultra-v1":{},
    "amazon.titan-text-lite-v1":{},
    "amazon.titan-text-express-v1":{},
    "cohere.command-text-v14":{},
    "cohere.command-light-text-v14":{},
    "mistral.mistral-7b-instruct-v0:2":{},
    "meta.llama2-13b-chat-v1":{},
    "meta.llama2-70b-chat-v1":{}
    
}

titan_and_ai21_and_cohere_prompt_template = """
    You are an advisory AI system, and provides answers to questions by using fact based and statistical information when possible. 
    Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context_str}
    </context>

    <question>
    {query_str}
    </question>

    The response should be specific and stick to the context given when possible.
    """
llama_and_mistral_prompt_template = """
  "prompt": "You are an advisory AI system, and provides answers to questions by using fact based and statistical information when possible. 
  Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags. If you don't know the answer, 
  just say that you don't know, don't try to make up an answer.
    <context> {context_str} </context> 
    <question> {query_str} </question> 
    The response should be specific and stick to the context given when possible."

"""

claudev2_prompt_template = """\n\nHuman: 
    You are an advisory AI system, and provides answers to questions by using fact based and statistical information when possible. 
    Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context_str}
    </context>

    <question>
    {query_str}
    </question>

    The response should be specific and stick to the context given when possible.

    Assistant:"""
claude3_prompt_template ="""\n\nHuman: 
    You are an advisory AI system, and provides answers to questions by using fact based and statistical information when possible. 
    Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context_str}
    </context>

    <question>
    {query_str}
    </question>

    The response should be specific and stick to the context given when possible.

    Assistant:"""


        

PROMPT_TEMPLATES = {
    "amazon.titan-text-lite-v1": titan_and_ai21_and_cohere_prompt_template,
    "amazon.titan-text-express-v1": titan_and_ai21_and_cohere_prompt_template,
    "ai21.j2-mid-v1": titan_and_ai21_and_cohere_prompt_template,
    "ai21.j2-ultra-v1": titan_and_ai21_and_cohere_prompt_template,
    "cohere.command-text-v14": titan_and_ai21_and_cohere_prompt_template,
    "cohere.command-light-text-v14":titan_and_ai21_and_cohere_prompt_template,
    "anthropic.claude-v2:1":claudev2_prompt_template,
    "anthropic.claude-instant-v1":claudev2_prompt_template,
     "anthropic.claude-v2":claudev2_prompt_template,
    "anthropic.claude-3-sonnet-20240229-v1:0":claude3_prompt_template,
     "anthropic.claude-3-haiku-20240307-v1:0":claude3_prompt_template,
     "mistral.mistral-7b-instruct-v0:2":llama_and_mistral_prompt_template,
     
     "meta.llama2-13b-chat-v1":llama_and_mistral_prompt_template,
     "meta.llama2-70b-chat-v1":llama_and_mistral_prompt_template
}

# fetch context from the response
def get_contexts(retrievalResults):
    contexts = []
    for retrievedResult in retrievalResults: 
        contexts.append(retrievedResult['content']['text'])
    return contexts


def get_response(model_id, query, contexts, bedrock_client):
    bedrock_client = boto3.client('bedrock-runtime')

    prompt_template = PromptTemplate(template=PROMPT_TEMPLATES[model_id],
                               input_variables=["context_str","query_str"])

    prompt = prompt_template.format(context_str=contexts, 
                                 query_str=query)
    
    # print("the prompt is: ")
    # print(prompt)

    # generate response
    if  model_id.startswith("mistral"):
        body = {
                "prompt": prompt,
                "temperature": 0.5,
                # "top_p": 0.9,
                "max_tokens": 512,
            }
        response = bedrock_client.invoke_model(
                modelId=model_id, body=json.dumps(body)
            )

        response_body = json.loads(response["body"].read())
        outputs = response_body.get("outputs")
        # output_str = "".join(outputs)


        response = [output["text"] for output in outputs]
        response = ''.join(response)
    elif model_id.startswith("meta"):
        body = {
                "prompt": prompt,
                "temperature": 0.5,
                "top_p": 0.9,
                "max_gen_len": 512,
            }

        response = bedrock_client.invoke_model(
            modelId=model_id, body=json.dumps(body)
        )

        response_body = json.loads(response["body"].read())
        response = response_body["generation"]


    
        
    elif model_id.startswith("anthropic.claude-3") :
        message = {"role": "user","content": [{"type": "text", "text": prompt}]}
        messages = [message]

        prompt_config = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": messages,}
        #parameters system and stop_sequences are optional
        body = json.dumps(prompt_config)

        accept = "application/json"
        contentType = "application/json"

        response = bedrock_client.invoke_model(
            body=body, modelId=model_id, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())

        response = response_body.get("content")[0].get("text")
        

    
    elif model_id.startswith("cohere"):# cohere
        body = {
                "prompt": prompt,
                "temperature": 0.9,
                "p": 0.9,
                "max_tokens": 200,
                "k": 1
            }
        response = bedrock_client.invoke_model(
                modelId=model_id, body=json.dumps(body)
            )
        response_body = json.loads(response.get("body").read())
        response = response_body.get("generations")[0].get("text")
        
        
    elif model_id.startswith("ai21"):# ai21
        body = {
                "prompt": prompt,
                "temperature": 0.9,
                "topP": 0.9,
                "maxTokens": 200
            }
        response = bedrock_client.invoke_model(
                modelId=model_id, body=json.dumps(body)
            )
        response_body = json.loads(response["body"].read())
        response = response_body["completions"][0]["data"]["text"]

        
    elif  model_id.startswith("amazon"):#titan
        body = {
                "inputText": prompt,
                "textGenerationConfig":
                {
                "temperature": 0.9,
                "topP": 1,
                "maxTokenCount": 4096}

            }
        response = bedrock_client.invoke_model(
                modelId=model_id, body=json.dumps(body)
            )
        response_body = json.loads(response["body"].read())
        response = response_body["results"][0]["outputText"]
        # print(response_body)
    else: #claude2 &v1
        body = {
                "prompt": prompt,
                "max_tokens_to_sample": 200,
                "temperature": 0.5,
                "stop_sequences": ["\n\nHuman:"],
            }

        response = bedrock_client.invoke_model(
            modelId=model_id, body=json.dumps(body)
        )

        response_body = json.loads(response["body"].read())
        response = response_body["completion"]

    return response


if __name__  == "__main__":
    bedrock_client = boto3.client('bedrock-runtime')
    # model_id = "meta.llama2-13b-chat-v1"
    # model_id = "amazon.titan-text-express-v1"
    # model_id = "anthropic.claude-instant-v1"
    # model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    model_id = "ai21.j2-mid-v1"
    # model_id = "cohere.command-text-v14"
    # model_id = "mistral.mistral-7b-instruct-v0:2"
    
   
    # get retrieval results
    query = "What can I do to help with the sustainability goals?"

    kb_id = "NQCADJXYK5"

    # get retrieval results
    bedroc_agent_client = get_bedrock_agent_client()
    response = retrieve(bedroc_agent_client, query, kb_id, numberOfResults=5)

    retrievalResults = response['retrievalResults']

    # construct prompt
    contexts = get_contexts(retrievalResults)

    response = get_response(model_id, query, contexts, bedrock_client)
    print(response)
    print(type(response))