import logging
import os
from fastapi import APIRouter
import boto3
from langchain.llms.bedrock import Bedrock
from typing import Any, Dict
from langchain.prompts import PromptTemplate
import json
from .fastapi_request import (Request,
                              Text2TextModelName,
                              )



logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()


TEXT2TEXT_MODEL_ID = os.environ.get('TEXT2TEXT_MODEL_ID')
BEDROCK_SERVICE = os.environ.get('BEDROCK_SERVICE')


router = APIRouter()
bedrock_client = boto3.client('bedrock-runtime')


@router.post("/text2text") 
def text2text_handler(req: Request) -> Dict[str, Any]:
    # dump the received request for debugging purposes
    logger.info(f"req={req}")
    # boto3_bedrock = boto3.client('bedrock-runtime')
    prompt_template = '''\n\nHuman: You are an AI assitant,please answer the question inside the <q></q> XML tags.
    
    <q>{question}</q>
    
    Please remember do not show the question in the answer and do not show any XML tags in the answer. If you don't know the answer or if the answer is not in the context say "Sorry, I don't know."

    Assistant:'''
    
    claude_template = PromptTemplate(template=prompt_template,
                               input_variables=["question"])
    prompt = claude_template.format(question=f"{req.q}")
    
    payload = {
        "prompt": prompt,
        "max_tokens_to_sample": req.maxTokenCount,
        "stop_sequences": req.stopSequences,
        "temperature": req.temperature,
         "top_k": req.top_k,
        "top_p": req.top_p
        }
    body = json.dumps(payload)
    response = bedrock_client.invoke_model(
        modelId=TEXT2TEXT_MODEL_ID, body=json.dumps(payload)
        )
    response_body = json.loads(response["body"].read())
    answer = response_body["completion"]
   
    
    endpoint_name = req.text_generation_model
    logger.info(f"ModelId: 'anthropic.claude-instant-v1', Bedrock Model: {BEDROCK_SERVICE}")

    session_id = req.user_session_id
   

    logger.info(f"answer received from llm,\nquestion: \"{req.q}\"\nanswer: \"{answer}\"")
    resp = {'question': req.q, 'answer': answer,'session_id': req.user_session_id,"top_k":req.top_k,"top_p":req.top_p,"max_length":req.max_length,"temperature":req.temperature}


    return resp
    

