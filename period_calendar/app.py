import boto3
from datetime import datetime,timedelta
from boto3.dynamodb.conditions import Key, Attr
import uuid
#ddb = boto3.client("dynamodb")
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from datetime import datetime, date

    
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Welcome to period tracker").set_should_end_session(False)
        return handler_input.response_builder.response    

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print(exception)
        handler_input.response_builder.speak("Sorry, there was some problem. Please try again")
        return handler_input.response_builder.response

class NextPeriodIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NextPeriod")(handler_input)

    def handle(self, handler_input):
        
        try:
            #if datetime.strptime(period_date1, '%Y-%m-%d %H:%M:%S') > datetime.today():
                #raise Exception('Period Date greater than todays date')
            import ask_sdk_core
            user_id = ask_sdk_core.utils.request_util.get_user_id(handler_input)    
            dyndb = boto3.resource('dynamodb', region_name='ap-southeast-2')
            table = dyndb.Table('Menstruation')           

            data = table.query(
                KeyConditions={
                'UserID': {
                'AttributeValueList': [user_id],
                'ComparisonOperator': 'EQ'
                },
            })

            if data['Count'] == 0:
                speech_text = "There is no data. Please add a previous period date to forecast your next period."
            else :
                records = data["Items"]
                records.sort(key=lambda x:datetime.strptime(x["period_date"], '%Y-%m-%d'),reverse=True)
            
                max_date = records[0]['period_date']
                datetime_object = datetime.strptime(max_date, '%Y-%m-%d')
                end_date = datetime_object + timedelta(days=28)
                date_time = end_date.strftime('%Y-%m-%d')
                speech_text = "Your next period is " + date_time
                            
                  
        except BaseException as e:
            print(e)
            raise(e)
        
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response    


class AddPeriodIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AddPeriod")(handler_input)

    def handle(self, handler_input):
        period_date = handler_input.request_envelope.request.intent.slots['period'].value
        try:
            import ask_sdk_core
            user_id = ask_sdk_core.utils.request_util.get_user_id(handler_input)
            period_date1 = "2021-11-03 00:00:00"
            #if datetime.strptime(period_date1, '%Y-%m-%d %H:%M:%S') > datetime.today():
             #   raise BaseException('Period Date greater than todays date')
            dyndb = boto3.resource('dynamodb', region_name='ap-southeast-2')
            table = dyndb.Table('Menstruation')
            trans = {}
            trans['UserID'] = user_id
            trans['SessionID'] = str(uuid.uuid4())
            trans['period_date'] = period_date
            trans['add_date'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            table.put_item(Item=trans)  
                            
                  
        except BaseException as e:
            print(e)
            raise(e)
        
        speech_text = "You added your period date " + period_date
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response   

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(AddPeriodIntentHandler())
sb.add_request_handler(NextPeriodIntentHandler())

def lambda_handler(event, context):
    return sb.lambda_handler()(event, context)

if __name__ == "__main__":

    fake_event = {
        "version": "1.0",
        "session": {
            "new": False,
            "sessionId": "amzn1.echo-api.session.efbf53be-7355-4c40-ac9e-ee450bf6adbe",
            "application": {
                "applicationId": "amzn1.ask.skill.358e56e6-230e-417e-bec1-0f88525e8bae"
            },
            "attributes": {},
            "user": {
                "userId": "amzn1.ask.account.AH5RVETXN5X23GWXRZZN6RFKRERM2XZPVFKTYQFSOJETMTI5LI3FGFUKDCFDYIMZIXZYBZRDK456SKM2WQBE7KGODUGIKYVIFOVJAYIKLKOSMS3VSEQHSZGVMEQBWXBKCUXUMLP3ANNQ2QLYHLJQKX7BDYTZC5CRCWLYHK3NE2BYXY33RZPJULVY2CDFFOK5NIWP3MKZ7YB5HBI"
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
                    "applicationId": "amzn1.ask.skill.358e56e6-230e-417e-bec1-0f88525e8bae"
                },
                "user": {
                    "userId": "amzn1.ask.account.AH5RVETXN5X23GWXRZZN6RFKRERM2XZPVFKTYQFSOJETMTI5LI3FGFUKDCFDYIMZIXZYBZRDK456SKM2WQBE7KGODUGIKYVIFOVJAYIKLKOSMS3VSEQHSZGVMEQBWXBKCUXUMLP3ANNQ2QLYHLJQKX7BDYTZC5CRCWLYHK3NE2BYXY33RZPJULVY2CDFFOK5NIWP3MKZ7YB5HBI"
                },
                "device": {
                    "deviceId": "amzn1.ask.device.AHZN3BI2ZS5OZCS4VWFUKTUVPUJNFRGVOQ5I5S7HEHCV6BB3U2CHD6U6CVZGNP4GNELFNXXCUTND52QTW2VODBHP67NVBXKCTM4DRPJZBZYMRSVCFATWTIWZQ2Y6267LR4HFB3DQ3EFTTIW4MULOXYFIRE63W6Q2BS367EHM6S5NRZSCDYU76",
                    "supportedInterfaces": {}
                },
                "apiEndpoint": "https://api.fe.amazonalexa.com",
                "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5mZS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjM1OGU1NmU2LTIzMGUtNDE3ZS1iZWMxLTBmODg1MjVlOGJhZSIsImV4cCI6MTYzNTIxNTkzMCwiaWF0IjoxNjM1MjE1NjMwLCJuYmYiOjE2MzUyMTU2MzAsInByaXZhdGVDbGFpbXMiOnsiY29udGV4dCI6IkFBQUFBQUFBQXdBTGxiMVBWSTE0WkZxMzBKdzZ3Yk1XS2dFQUFBQUFBQURuQkZxZlNRSEMzT0k0eVJ3K01Ibi9RZW9VU0VkbUNIcis2dTJ0bngxUWxQWSttdldpSnZrelc3OHcxTWMwUHVPY1psNlA1NjFUSUxOZVAxY3JTQVEvM2QyRlBua0F6V3FsTkRQZW44ZEJCSHRycVN3b1hldml6SEp3cEs2QVdIZFk5SVNqTEUxYkZhbHBpcjJGMTdMN2tTL2kvK0F3WC9jWUlSeFR6R3ZBNU9KbnlnNE9OVEl1TW8yUnNTZGY1WllKTlN5WUptQlUvczRIYXU4T0E2b2xsM0NGYVB2WkdOcENVdFBlaW9nMmZmcFIvNHhjNloxeEEzbWpjWXYyYUphMTNGWmtGN01CaHgvdXNwcFhuL1JqQkdZRWJ0cVJFS1h3ZDMrcU5LTmFiYXJ4bFJkdXFGQ2FHaWFveDg4aGkwN0JiZTc0cWJyZHdoSWo0RFVNeUNjVHFaMkl2c0RNTkhXdGM0d2Z5NCtVSWlaN0oreWtaSWRiS0gyN2Y5NE45SkRTMDNCQmJEZ054b25XIiwiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUhaTjNCSTJaUzVPWkNTNFZXRlVLVFVWUFVKTkZSR1ZPUTVJNVM3SEVIQ1Y2QkIzVTJDSEQ2VTZDVlpHTlA0R05FTEZOWFhDVVRORDUyUVRXMlZPREJIUDY3TlZCWEtDVE00RFJQSlpCWllNUlNWQ0ZBVFdUSVdaUTJZNjI2N0xSNEhGQjNEUTNFRlRUSVc0TVVMT1hZRklSRTYzVzZRMkJTMzY3RUhNNlM1TlJaU0NEWVU3NiIsInVzZXJJZCI6ImFtem4xLmFzay5hY2NvdW50LkFINVJWRVRYTjVYMjNHV1hSWlpONlJGS1JFUk0yWFpQVkZLVFlRRlNPSkVUTVRJNUxJM0ZHRlVLRENGRFlJTVpJWFpZQlpSREs0NTZTS00yV1FCRTdLR09EVUdJS1lWSUZPVkpBWUlLTEtPU01TM1ZTRVFIU1pHVk1FUUJXWEJLQ1VYVU1MUDNBTk5RMlFMWUhMSlFLWDdCRFlUWkM1Q1JDV0xZSEszTkUyQllYWTMzUlpQSlVMVlkyQ0RGRk9LNU5JV1AzTUtaN1lCNUhCSSJ9fQ.yBc6qpt4uNnhrr-pur9QC6pbsa4xQCjiGCxlKmOlf254yUmg1mzPvCWa5luGsw7sCOSKDaEJXSxtt_mB-bWree4OhhOo49JwwKFoWfGDnorH0WS_VlBU_vQqKjfamnBJTk1UxzV_xOIFCnYo7iksyHINA0JC1WfdUX3_P6y5oFFn_CCrcBs2OupklUDBSSr2J9o3aczTtrFNygAKyt9y5KV2QPFazb4A-snjwvvdTOJ8Aso0VVfGuh6kuTXNRmOYc5F_mwtAe_ceSxIJKkXo-uUBkEKs97bejBiCxoxi8OsmhXnvMbjf0Cyu_upGHQgT1wA3AGoAbZH932f_swnprg"
            }
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "amzn1.echo-api.request.8aa0e913-b8b1-452b-b58e-573e2a504fc6",
            "locale": "en-US",
            "timestamp": "2021-10-26T02:33:50Z",
            "intent": {
                "name": "NextPeriod",
                "confirmationStatus": "NONE",
                "slots": {
                    "period": {
                        "name": "period",
                        "value": "2021-10-21",
                        "confirmationStatus": "NONE",
                        "source": "USER"
                    }
                }
            }
        }
    }

    sb.lambda_handler()(fake_event, None)
