### IoT Voice Temperature Controller

In this repository, you will find source code to use in conjunction with the hardware from Google Voice Kit, AWS Lex and AWS IoT Core

**Google Voice Kit**
https://aiyprojects.withgoogle.com/voice/

**AWS Lex**
https://aws.amazon.com/lex/

**AWS IoT Core**
https://aws.amazon.com/iot-core/


### Google Voice Kit
On this kit, I installed Boto 3 to communicate with AWS services.

```
$ pip install boto3
```

Add your AWS credentials to `~/.aws/credentials`
It is good practice to create a new IAM user for this device from the AWS console.
```
[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET
```

and a default region to `~/.aws/config`
```
[default]
region=us-east-1
```

After setting up Boto 3, copy over the `VoiceBotController.py` file and run it

```
$ python3 VoiceBotController.py
```


### AWS Lambda

Lambda functions are serverless scripts that can executed by different triggers.
A very simple way to process and trigger services.

Add a Lambda function with the Python 3.7 runtime.

Copy `Lambda_setMachineTemperature.py` into the function code.

Remember to update the policy to interact with IoT topics by modifying the role.

A sample of the policy I used can be found in `Lamda_IoT_policy.json`


### AWS Lex

This is used to create voice chat bots that will take a recording of your voice and turn it into text.

Set up a Bot by importing `Lex_Bot_MachineTemperature.json` into AWS Lex and add the Fulfillment to an AWS Lambda function that was created.

Build and Publish the bot. Use `prod` when prompted to create an alias.


### AWS IoT Core

The IoT service from AWS allows you to connect different devices together.

As the Lambda will publish an event to the 'iot/temperature/machines' topic, you will need to set up devices to subscribe to these topics and then act on the data from within the event.

A simple way to achive this is to use the sdk which have sample code that you can use.

**aws-iot-device-sdk-python**
https://github.com/aws/aws-iot-device-sdk-python

A simple publish and subscription sample code:
https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/basicPubSub/basicPubSub.py

When setting up the IoT device, remember to change the Thing policy so that it can subscribe to the 'iot/temperature/machines' topic.