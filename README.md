
# AWS Bedrock Agent walkthrough
This project provides some basic tools to demonstrate how to leverage the Amazon Bedrock Agent by leveraging lambda functions to supply new capabilities.

This project leverages the AWS CDK in order to deploy resources to the aws account the AWS Bedrock Agent operates in.

## Installation

### Prerequisits
- AWS CDK
- Python

### Setting up environment

```bash
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```bash
source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```bash
.venv\Scripts\activate.bat
```

### Install dependencies
Once the virtualenv is activated, you can install the required dependencies.

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

# Walkthrough Steps

## 1. Deploy the project
The first step is to deploy the project in the account by running the following command:
```bash
cdk deploy
```

## 2. Add Content

1. Copy the file schedule.csv to your stack's S3 bucket, which name will begin with "awsagenttoolsstack"

2. Subscribe your email to the stack's sns topic, with a name starting with "AwsAgentToolsStack". Ensure you confirm the subscription in your email.

## 2. Create the Bedrock Agent
1. Create the bedrock agent by going to the
[Bedrock Agent Page](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/agents).

2. Click the "Create Agent" button and give your agent a name, then click "Create".

## 3. Add the ability to search the internet
1. Scroll down to "Action groups" and click the "Add" button

2. Name the first action group **"WebSearch"**

3. Scroll to "Action group invocation" and select "Select an existing Lambda function".

4. In the lambda dropdown select the **"AwsAgentToolsStack-WebSearchLambda"** with the extra characters at the end and select it. [Code for function](./src/websearch/web_search.py)

5. Scroll to "Action group function 1" and name it **"WebSearch"**. The provide the description:

```
Searches the web using duckduckgo in order to find information
```

6. Scroll to the "Paramters" section then click the pencil for the first parameter's name, the type in **"search_query"**. Supply the following as the parameter's description:

```
The query to use to search the internet
```

7. Click the "Save and Exit" button

## 4. Add the ability to retrieve a webpage
1. Scroll down to "Action groups" and click the "Add" button

2. Name the first action group **"GetWebUrl"**

3. Scroll to "Action group invocation" and select "Select an existing Lambda function".

4. In the lambda dropdown select the **"AwsAgentToolsStack-WebGetLambda"** with the extra characters at the end and select it. [Code for function](./src/websearch/web_get.py)

5. Scroll to "Action group function 1" and name it **"GetWebpage"**. The provide the description:

```
Uses a web url in order to retrieve a webpage content
```

6. Scroll to the "Paramters" section then click the pencil for the first parameter's name, the type in **"url"**. Supply the following as the parameter's description:

```
The url of the webpage to get
```

7. Click the "Save and Exit" button

## 5. Add the ability to retrieve the "Schedule"

1. In the chatbot, go to the "Action groups" and click the "add" button

2. Name the first action group **"GetSchedule"**

3. Scroll to "Action group invocation" and select "Select an existing Lambda function".

4. In the lambda dropdown select the **"AwsAgentToolsStack-GetSchedule"** with the extra characters at the end and select it. [Code for function](./src/email_tools/get_meetings.py)

5. Scroll to "Action group function 1" and name it **"GetSchedule"**. The provide the description:

```
Gets the calendar schedule for the current user
```

6. Click the "Save and Exit" button

## 6. Add the ability to send an email

1. In the chatbot, go to the "Action groups" and click the "add" button

2. Name the first action group **"SendEmail"**

3. Scroll to "Action group invocation" and select "Select an existing Lambda function".

4. In the lambda dropdown select the **"AwsAgentToolsStack-SendEmail"** with the extra characters at the end and select it. [Code for function](./src/email_tools/send_email.py)

5. Scroll to "Action group function 1" and name it **"SendEmail"**. The provide the description:
```
Sends an email with the content supplied to the person in the chat
```

6. Scroll to the parameters and add one named **"content"** with a description of:
```
The content to send in the email
```

7. Click the "Save and Exit" button

## 7. Give instructions to the agent

1. Scroll to the "Instructions for the Agent"

2. Provide the following instructions.
```
You are a sales person working for AWS and tasked with researching companies in order to breif solution architects.
```

## 8. Click Prepare if available

If the Prepare button is available click it, otherwise click the save button.

## 9. Test the agent

In the agent chat area, to the right of the configuration area, type in:

```
Look at my schedule and put together briefings on my upcoming meetins. This should include a summary of the customer, which technology domains I should get up to speed on, what skillsets they are hiring for, and some of the challenges the customer is facing.
```
