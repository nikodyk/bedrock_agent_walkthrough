"""This file includes an AWS Agent Lambda implementation which enables web search"""
from aws_lambda_powertools.event_handler import BedrockAgentResolver

import json
import requests
from duckduckgo_search import DDGS
from typing import Dict, Any

app = BedrockAgentResolver()

def handler(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    """The handler for the lambda function"""
    print("Event:", event)
    try:
        search_query = event['parameters'][0]['value']
        if not search_query:
            raise ValueError("Search query is required")

        search_results = search_web(search_query)
        print("Search results:", search_results)
        session_attributes = event.get('sessionAttributes')
        prompt_session_attributes = event.get('promptSessionAttributes')
        response = {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup'),
                "function": event.get('function'),
                "sessionId": event.get('sessionId'),
                "inputText": search_query,
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps(search_results),
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
                "inputText": search_query,
                "functionResponse": {
                    "responseState": "FAILURE"
                }
            },
            "session_attributes": session_attributes,
            "prompt_session_attributes": prompt_session_attributes
        }

def search_web(search_query: str) -> Dict[str, Any]:
    """Search the web using DuckDuckGo"""
    response = DDGS().text(search_query, max_results=5)

    return response