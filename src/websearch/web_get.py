"""This file includes an AWS Agent Lambda implementation which enables web search"""
from aws_lambda_powertools.event_handler import BedrockAgentResolver

import json
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

app = BedrockAgentResolver()

def get_web(url: str) -> str:
    """Search the web using DuckDuckGo"""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Extract text from the response
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()  # Return the text content of the page

def handler(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    """The handler for the lambda function"""
    print("Event:", event)
    try:
        url = event['parameters'][0]['value']
        if not url:
            raise ValueError("Url is required")

        web_results = get_web(url)
        print("Search results:", web_results)
        session_attributes = event.get('sessionAttributes')
        prompt_session_attributes = event.get('promptSessionAttributes')
        response = {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup'),
                "function": event.get('function'),
                "sessionId": event.get('sessionId'),
                "inputText": url,
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": web_results,
                        }
                    }
                }
            },
            "session_attributes": session_attributes,
            "prompt_session_attributes": prompt_session_attributes
        }
        print("Response:", response)
        return response
    except Exception as e:
        print("Error", e)
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup'),
                "function": event.get('function'),
                "sessionId": event.get('sessionId'),
                "inputText": url,
                "functionResponse": {
                    "responseState": "FAILURE"
                }
            },
            "session_attributes": event.get('sessionAttributes'),
            "prompt_session_attributes": event.get('promptSessionAttributes')
        }
