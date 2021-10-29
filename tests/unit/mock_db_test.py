"""
Example of using moto to mock out DynamoDB table
"""

import boto3
from moto import mock_dynamodb2

import pytest

from period_calendar import app

def test_hello():
  assert 1 == 1

# @mock_dynamodb2
# def test_write_into_table():
# 	"Test the write_into_table with a valid input data"
# 	dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
# 	table_name = 'Menstruation'
# 	table = dynamodb.create_table(TableName = table_name,
# 								KeySchema = [
# 								{'AttributeName': 'UserID', 'KeyType': 'HASH'},{'AttributeName': 'SessionID', 'KeyType': 'RANGE'}],
# 								AttributeDefinitions = [
# 								{'AttributeName': 'UserID', 'AttributeType': 'S'}, {'AttributeName': 'SessionID', 'AttributeType': 'S'}])
# 	data = {'UserID': 'ANNA',
# 			'SessionID': '123456', 'period_date': '2021-10-26', 'add_date': '2021-10-29 12:32:10'}
# 	table.put_item(Item=data)
# 	data = {'UserID': 'ANNA', 'SessionID' : '323232', 'period_date':'20-10-15', 
# 			'add_date': '2021-10-29 12:22:11'}
# 	table.put_item(Item=data)
	

# 	ret = app.lambda_handler(alexa_event(), "")
# 	assert 'Your next period is 2021-11-23' in ret['response']['outputSpeech']['ssml']


# 	# #response = table.get_item(Key={'MeasureName': data['MeasureName']})
# 	# response = table.get_item(Key={'MeasureName': "NT - Administration state - Daily increase doses recorded"})
# 	# actual_output = response['Item']
# 	# assert actual_output == data



def alexa_event():
    """ Generates Alexa Event"""

    return {
      "version": "1.0",
      "session": {
        "new": False,
        "sessionId": "amzn1.echo-api.session.xxxx",
        "application": {
          "applicationId": "amzn1.ask.skill.xxxx"
        },
        "attributes": {},
        "user": {
          "userId": "amzn1.ask.account.xxxx"
        }
      },
      "context": {
        "Viewports": [
          {
            "type": "APL",
            "id": "main",
            "shape": "RECTANGLE",
            "dpi": 213,
            "presentationType": "STANDARD",
            "canRotate": False,
            "configuration": {
              "current": {
                "mode": "HUB",
                "video": {
                  "codecs": [
                    "H_264_42",
                    "H_264_41"
                  ]
                },
                "size": {
                  "type": "DISCRETE",
                  "pixelWidth": 1280,
                  "pixelHeight": 800
                }
              }
            }
          }
        ],
        "Viewport": {
          "experiences": [
            {
              "arcMinuteWidth": 346,
              "arcMinuteHeight": 216,
              "canRotate": False,
              "canResize": False
            }
          ],
          "mode": "HUB",
          "shape": "RECTANGLE",
          "pixelWidth": 1280,
          "pixelHeight": 800,
          "dpi": 213,
          "currentPixelWidth": 1280,
          "currentPixelHeight": 800,
          "touch": [
            "SINGLE"
          ],
          "video": {
            "codecs": [
              "H_264_42",
              "H_264_41"
            ]
          }
        },
        "Extensions": {
          "available": {
            "aplext:backstack:10": {}
          }
        },
        "System": {
          "application": {
            "applicationId": "amzn1.ask.skill.xxx"
          },
          "user": {
            "userId": "amzn1.ask.account.xxxx"
          },
          "device": {
            "deviceId": "amzn1.ask.device.xxxx",
            "supportedInterfaces": {}
          },
          "apiEndpoint": "https://api.fe.amazonalexa.com",
          "apiAccessToken": ""
        }
      },
      "request": {
        "type": "IntentRequest",
        "requestId": "amzn1.echo-api.request.5b8f8478-b1e8-4ea1-96b2-52f404a262db",
        "locale": "en-US",
        "timestamp": "2021-10-19T04:57:36Z",
        "intent": {
          "name": "NextPeriodIntent",
          "confirmationStatus": "NONE",
          "slots": {
				    "delete": {
					  "name": "delete",
					  "confirmationStatus": "NONE",
					  "source": "USER"
				    }
			    }
        },
        "dialogState": "COMPLETED"
      }
    }

