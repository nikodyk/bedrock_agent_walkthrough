from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    Duration
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_iam as iam
import aws_cdk.aws_sns as sns

from constructs import Construct

class AwsAgentToolsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # A lambda that searches the web and leverages "web_search.py" as its handler
        search_web = PythonFunction(
            self, 
            "WebSearchLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            entry="./src/websearch",
            index="web_search.py",
            handler="handler",
            timeout=Duration.seconds(30),
            memory_size=128
        )
        search_web.add_permission("bagent", principal=iam.ServicePrincipal("bedrock.amazonaws.com"), action="lambda:InvokeFunction", source_arn=f"arn:aws:bedrock:{self.region}:{self.account}:*")

        get_website = PythonFunction(
            self, 
            "WebGetLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            entry="./src/websearch",
            index="web_get.py",
            handler="handler",
            timeout=Duration.seconds(30),
            memory_size=128
        )
        get_website.add_permission("bagent", principal=iam.ServicePrincipal("bedrock.amazonaws.com"), action="lambda:InvokeFunction", source_arn=f"arn:aws:bedrock:{self.region}:{self.account}:*")

        bucket = s3.Bucket(self, "agent_bucket", block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        get_schedule = PythonFunction(
            self, 
            "GetSchedule",
            runtime=lambda_.Runtime.PYTHON_3_9,
            entry="./src/email_tools",
            index="get_meetings.py",
            handler="handler",
            timeout=Duration.seconds(30),
            memory_size=128,
            environment={
                "BUCKET_NAME": bucket.bucket_name
            }
        )
        get_schedule.add_permission(
            "bagent", 
            principal=iam.ServicePrincipal("bedrock.amazonaws.com"), 
            action="lambda:InvokeFunction", 
            source_arn=f"arn:aws:bedrock:{self.region}:{self.account}:*"
        )
        bucket.grant_read(get_schedule)

        topic = sns.Topic(self, "EmailTopic")
        send_email = PythonFunction(
            self, 
            "SendEmail",
            runtime=lambda_.Runtime.PYTHON_3_9,
            entry="./src/email_tools",
            index="send_email.py",
            handler="handler",
            timeout=Duration.seconds(30),
            memory_size=128,
            environment={
                "SNS_TOPIC_ARN": topic.topic_arn
            }
        )
        send_email.add_permission(
            "bagent", 
            principal=iam.ServicePrincipal("bedrock.amazonaws.com"), 
            action="lambda:InvokeFunction", 
            source_arn=f"arn:aws:bedrock:{self.region}:{self.account}:*"
        )
        topic.grant_publish(send_email)
