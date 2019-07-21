import json
import boto3

client = boto3.client('iot-data', region_name='eu-west-1')

def lambda_handler(event, context):

    Temperature = event['currentIntent']['slots']['temperature']
    Machine = event['currentIntent']['slots']['machine']

    if Temperature and Machine:
        client.publish(
            topic='iot/temperature/machines',
            qos=0,
            payload=json.dumps({"machine": Machine, "temperature": Temperature})
        )

    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "PlainText",
              "content": "Machine "+str(Machine)+" is set to " + str(Temperature) + " degrees"
            }
        }
    }
