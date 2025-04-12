"""This file includes an AWS Agent Lambda implementation which enables web search"""
from typing import Dict, Any
import boto3
import os

# Create s3 client
s3 = boto3.client('s3')

def get_schedule() -> str:

    # Get the file schedule.txt from the bucket name stored in the environment variable bucket
    s3_response = s3.get_object(Bucket=os.environ['BUCKET_NAME'], Key='schedule.csv')

    # Extract text from the response
    text = s3_response['Body'].read().decode('utf-8')
    return text

def handler(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    """The handler for the lambda function"""
    print("Event:", event)
    try:
        schedule_results = get_schedule()
        print("Search results:", schedule_results)
        session_attributes = event.get('sessionAttributes')
        prompt_session_attributes = event.get('promptSessionAttributes')
        response = {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup'),
                "function": event.get('function'),
                "sessionId": event.get('sessionId'),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": schedule_results,
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
                "functionResponse": {
                    "responseState": "FAILURE"
                }
            },
            "session_attributes": event.get('sessionAttributes'),
            "prompt_session_attributes": event.get('promptSessionAttributes')
        }
