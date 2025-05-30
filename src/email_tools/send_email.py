"""This file includes an AWS Agent Lambda implementation which enables web search"""
from typing import Dict, Any
import boto3
import os

# Create SNS Client
sns = boto3.client('sns')

def send_email(content: str) -> str:

    # Get the file schedule.txt from the bucket name stored in the environment variable bucket
    s3_response = sns.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Message=content,
    )

def handler(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    """The handler for the lambda function"""
    print("Event:", event)
    try:
        content = event['parameters'][0]['value']
        if not content:
            raise ValueError("No content provided")
        
        send_email(content)
        
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
                            "body": "Email sent",
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
