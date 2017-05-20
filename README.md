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

## MassTimes API
Here is a link to the API information: http://apiv4.updateparishdata.org/Default.htm
 
### Some caveats:
* The API key is not needed.  Don’t put one in.
* Query church “header” data by http://apiv4.updateparishdata.org/Churchs/109590 (where 109590 is church legacy ID)
* You have to append a `“&pg=1”` to get the 30 results per the 2nd sample (lat/long)
* Currently the API is using a legacy church ID; we’re going to create another API that uses a new church ID but we will continue to support the current API.ppend a `“&pg=1”` to get the 30 results per the 2nd sample (lat/long)
* Currently the API is using a legacy church ID; we’re going to create another API that uses a new church ID but we will continue to support the current API.
