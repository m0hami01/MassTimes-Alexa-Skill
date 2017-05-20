# MassTimes-Alexa-Skill

This is the code for an Alexa Skill to query mass times from www.masstimes.org. The goal of this project is to be able to get mass times by location and to get parishes by mass time and location. Sample invocations are:
> Ask Mass Times when is mass in Houston, Texas?

> Ask Mass Times where are parishes with an 8 am weekend mass in New York City, New York?

## Getting started

First create an Alexa Skill at https://developer.amazon.com/ using the Alexa Skills Kit. Enter the following into each tab:

### Skill Information
* Skill Type: Custom
* Language: English
* Name: `MassTimes.org`
* Invocation Name: `mass times`
### Interaction Model
* Intent Schema: *Use the contents of IntentSchema.txt at the root of this repository*
* Sample Utterances: *Use the contents of SampleUtterances.txt at the root of this repository*
### Configuration
* Endpoint: AWS Lambda ARN; North America *See the AWS Lambda section to creat a Lambda function and use its ARN into the field*
* Account Linking: No
* Permissions: Device Address -> Country & Postal Code Only

## AWS Lambda Function
Create a free account at aws.amazon.com and go into the Lambda page. Create a Python 2.7 Lambda Function. The ARN will be visible in the upper right of the page. Use this in the Configuration tab of the Getting Started guide. Enter the following into each tab:

### Code
*See _Upload Code to Lambda Function_ section below once the Lambda Function is setup*
### Configuration
* Runtime: Python 2.7
* Handler: `lambda_function.lambda_handler`
* Role: Choose and existing role
* Existing Role: `lambda_basic_execution_mass_times`
* Description: `Returns Mass Times and Church Information`
#### Advanced
* Memory (MB): 128
* Timeout: 0 min; 10 sec
* VPC: No VPC
### Triggers
This should be set up to use the Alexa Skills Kit already.

## Uploading Code to Lambda Function
First, zip your src folder in this project. On Mac/Linux run the following:
```
cd src
zip -r ../lambda.zip .
```
Then go into the Code tab of the Lambda Function and select Upload a .zip file and upload lambda.zip. Then select Save at the top of the page. 

*If anyone wants to make a script to automate this, please do this!*

## Test from the Alexa Skill page
Go to the Test tab and make sure the skill is Enabled for testing on your account. This will allow you to use any Alexa-enabled device on your account to test your skill.

Use the Service Simulator and enter the following phrase:

> When are mass times in Seattle Washington?

Click Ask MassTimes.org and you should receive a JSON response. If you ask your Alexa-enabled device "Ask Mass Times for mass times in Seattle, Washington" you should hear her respond with the `response.outputSpeech.text` from the JSON response.  

## MassTimes API
Here is a link to the API information: http://apiv4.updateparishdata.org/Default.htm
 
### Some caveats:
* The API key is not needed.  Don’t put one in.
* Query church “header” data by http://apiv4.updateparishdata.org/Churchs/109590 (where 109590 is church legacy ID)
* You have to append a `“&pg=1”` to get the 30 results per the 2nd sample (lat/long)
* Currently the API is using a legacy church ID; we’re going to create another API that uses a new church ID but we will continue to support the current API.ppend a `“&pg=1”` to get the 30 results per the 2nd sample (lat/long)
* Currently the API is using a legacy church ID; we’re going to create another API that uses a new church ID but we will continue to support the current API.
