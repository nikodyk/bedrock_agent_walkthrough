import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_agent_tools.aws_agent_tools_stack import AwsAgentToolsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_agent_tools/aws_agent_tools_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsAgentToolsStack(app, "aws-agent-tools")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
