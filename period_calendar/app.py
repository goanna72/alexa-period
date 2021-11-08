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
import json

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import UserEvent
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective, SpeakItemCommand,
    AutoPageCommand, HighlightMode)

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
        return is_intent_name("NextPeriod")(handler_input) or \
            (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and
                len(list(handler_input.request_envelope.request.arguments)) > 0 and
                list(handler_input.request_envelope.request.arguments)[0] == 'nextButton')

    def handle(self, handler_input):
        
        try:
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
                aplString = "There is no data. "
                endDateString = ""
                nextString = ""
            else :
                records = data["Items"]
                records.sort(key=lambda x:datetime.strptime(x["period_date"], '%Y-%m-%d'),reverse=True)
                max_date = records[0]['period_date']
                datetime_object = datetime.strptime(max_date, '%Y-%m-%d')
                end_date = datetime_object + timedelta(days=28)
                date_time = end_date.strftime('%Y-%m-%d')
                date_format = "%Y-%m-%d"
                a = datetime.strptime(datetime.today().strftime(date_format),date_format)
                b = datetime.strptime(date_time, date_format)
                numDays = b - a
                if numDays.days > 1:
                    strDay = "days"
                else:
                    strDay = "day"
                speech_text = "Your next period is " + date_time + ". You have " + str(numDays.days) + " " + strDay + " until your next period."
                aplString = "Number of days until next period: " + str(numDays.days)
                endDateString = end_date.strftime('%d-%b-%Y')
                nextString = "Your next period is:  "


        except BaseException as e:
            print(e)
            raise(e)
        
        handler_input.response_builder.speak(speech_text).set_card(SimpleCard('Hello', speech_text)).add_directive(
            RenderDocumentDirective(
                document= {
    "type": "APL",
    "version": "1.0",
    "theme": "dark",
    "import": [],
    "resources": [],
    "styles": {
      "headerStyle": {
        "values": [{
          "color": "#008080",
          "fontSize": "38",
          "fontWeight": 900
        }]
      },
      "textBlockStyle": {
        "values": [{
          "color": "indianred",
          "fontSize": "32"
        }]
      },
      "footerStyle": {
        "values": [{
          "fontSize": "20",
          "fontStyle": "italic"
        }]
      }
    },
    "layouts": {},
    "mainTemplate": {
        "items": [
            {
                "type": "Container",
                "items": [
                    {
                      "type": "Container",
                      "height": "400vh",
                      "width": "400vw",
                      "items": [
                        {
                          "type": "Container",
                          "paddingBottom": "70dp",
                          "paddingLeft": "40dp",
                          "paddingTop": "50dp",
                          "items": [{
                            "type": "Text",
                            "text": aplString,
                            "style": "headerStyle"
                          }]
                        }, {
                          "type": "Container",
                          "direction": "row",
                          "paddingBottom": "30dp",
                          "paddingLeft": "50dp",
                          "text-align": "center",
                          "vertical-align": "middle",
                          "items": [{
                            "type": "Text",
                            "text": nextString + " ",
                            "style": "headerStyle"
                          }]
                        }, {
                            "type": "Container",
                          "direction": "row",
                          "paddingBottom": "10dp",
                          "paddingLeft": "300dp",
                          "text-align": "center",
                          "vertical-align": "middle",
                          "items": [{
                            "type": "Text",
                            "text": " " + endDateString,
                            "style": "headerStyle"
                          }]
                        }, {
           
                          "type": "Container",
                          "position": "absolute",
                          "bottom": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": "This is footer block. Try APL.",
                            "style": "footerStyle"
                          }]
                      }]
                    }
                ]
            }
        ]
    }
},
                datasources={
                    'deviceTemplateData': {
                        'type': 'object',
                        'objectId': 'deviceSample',
                        'properties': {
                            'hintString': 'try and buy more devices!'
                        },
                        'transformers': [
                            {
                                'inputPath': 'hintString',
                                'transformer': 'textToHint'
                            }
                        ]
                    }
                }
            )
        ).set_should_end_session(False)
        return handler_input.response_builder.response    

class LastPeriodIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("LastPeriod")(handler_input) or \
              (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and
                len(list(handler_input.request_envelope.request.arguments)) > 0 and
                list(handler_input.request_envelope.request.arguments)[0] == 'lastButton')

    def handle(self, handler_input):
        
        try:
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
                speech_text = "There is no data."
                endString = "There is no data"
            else :
                records = data["Items"]
                records.sort(key=lambda x:datetime.strptime(x["period_date"], '%Y-%m-%d'),reverse=True)
            
                max_date = records[0]['period_date']
                datetime_object = datetime.strptime(max_date, '%Y-%m-%d')
                end_date = datetime_object
                date_time = end_date.strftime('%Y-%m-%d')
                speech_text = "Your most recent period was on " + date_time
                endString = end_date.strftime('%d-%b-%Y')
                            
                  
        except BaseException as e:
            print(e)
            raise(e)
        
        handler_input.response_builder.speak(speech_text).set_card(SimpleCard('Hello', speech_text)).add_directive(
            RenderDocumentDirective(
                document= {
    "type": "APL",
    "version": "1.0",
    "theme": "dark",
    "import": [],
    "resources": [],
    "styles": {
      "headerStyle": {
        "values": [{
          "color": "#008080",
          "fontSize": "38",
          "fontWeight": 900
        }]
      },
      "textBlockStyle": {
        "values": [{
          "color": "indianred",
          "fontSize": "32"
        }]
      },
      "footerStyle": {
        "values": [{
          "fontSize": "20",
          "fontStyle": "italic"
        }]
      }
    },
    "layouts": {},
    "mainTemplate": {
        "items": [
            {
                "type": "Container",
                "items": [
                    {
                      "type": "Container",
                      "height": "400vh",
                      "width": "400vw",
                      "items": [
                        {
                          "type": "Container",
                          "paddingBottom": "70dp",
                          "paddingLeft": "40dp",
                          "paddingTop": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": " ",
                            "style": "headerStyle"
                          }]
                        }, {
                          "type": "Container",
                          "direction": "row",
                          "paddingBottom": "30dp",
                          "paddingLeft": "50dp",
                          "text-align": "center",
                          "vertical-align": "middle",
                          "items": [{
                            "type": "Text",
                            "text": "Your most recent period was on:  ",
                            "style": "headerStyle"
                          }]
                        }, {
                            "type": "Container",
                          "direction": "row",
                          "paddingBottom": "10dp",
                          "paddingLeft": "300dp",
                          "text-align": "center",
                          "vertical-align": "middle",
                          "items": [{
                            "type": "Text",
                            "text": " " + endString,
                            "style": "headerStyle"
                          }]
                        }, {
           
                          "type": "Container",
                          "position": "absolute",
                          "bottom": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": "This is footer block. Try APL.",
                            "style": "footerStyle"
                          }]
                      }]
                    }
                ]
            }
        ]
    }
},
                datasources={
                    'deviceTemplateData': {
                        'type': 'object',
                        'objectId': 'deviceSample',
                        'properties': {
                            'hintString': 'try and buy more devices!'
                        },
                        'transformers': [
                            {
                                'inputPath': 'hintString',
                                'transformer': 'textToHint'
                            }
                        ]
                    }
                }
            )
        ).set_should_end_session(False)
        return handler_input.response_builder.response    


class DeleteAPLPeriodIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and
                len(list(handler_input.request_envelope.request.arguments)) > 0 and
                list(handler_input.request_envelope.request.arguments)[0] == 'deleteButton')

    def handle(self, handler_input):
        
        
        speech_text = "Are you sure"
        handler_input.response_builder.speak(speech_text).set_card(SimpleCard('Hello', speech_text)).add_directive(
            RenderDocumentDirective(
                document= {
     "type": "APL",
    "version": "1.0",
    "theme": "dark",
    "import": [
        {
        "name": "alexa-layouts",
        "version": "1.4.0"
      }
    ],
    "resources": [],
    "styles": {
      "headerStyle": {
        "values": [{
          "color": "#008080",
          "fontSize": "38",
          "fontWeight": 900
        }]
      },
      "textBlockStyle": {
        "values": [{
          "color": "indianred",
          "fontSize": "32"
        }]
      },
      "footerStyle": {
        "values": [{
          "fontSize": "20",
          "fontStyle": "italic"
        }]
      }
    },
    "layouts": {},
    "mainTemplate": {
        "items": [
            {
                "type": "Container",
                "items": [
                    {
                      "type": "Container",
                      "height": "400vh",
                      "width": "400vw",
                      "items": [
                        {
                          "type": "Container",
                          "paddingBottom": "70dp",
                          "paddingLeft": "40dp",
                          "paddingTop": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": " ",
                            "style": "headerStyle"
                          }]
                        }, {
                          "type": "Container",
                          "direction": "row",
                          "paddingBottom": "100dp",
                          "paddingLeft": "20dp",
                          "text-align": "center",
                          "vertical-align": "left",
                          "items": [{
                            "type": "Text",
                            "text": "Delete Data - Are You Sure?   ",
                            "style": "headerStyle"
                          }]
                        }, {
                            "type": "Container",
                          "direction": "row",
                          "paddingBottom": "10dp",
                          "paddingLeft": "180dp",
                          "text-align": "center",
                          "vertical-align": "middle",
                          "items": [
                          {
                            "type": "AlexaButton",
                            "buttonText": "YES",
                            "id": "${data.id}_${exampleType}",
                            "buttonStyle": "${data.buttonStyle}",
                            "touchForward": "${touchForwardSetting}",
                            "primaryAction": {
                            "type": "SendEvent",
                            "arguments": [
                                "YesButton"
                            ]
                        }
                        } ,
                          {
                            "type": "AlexaButton",
                            "buttonText": "NO",
                            "id": "${data.id}_${exampleType}",
                            "buttonStyle": "${data.buttonStyle}",
                            "touchForward": "${touchForwardSetting}",
                            "primaryAction": {
                            "type": "SendEvent",
                            "arguments": [
                                "NoButton"
                            ]
                        }
                        }
                          ]
                        }, {
           
                          "type": "Container",
                          "position": "absolute",
                          "bottom": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": "This is footer block. Try APL.",
                            "style": "footerStyle"
                          }]
                      }]
                    }
                ]
            }
        ]
    }
},
                datasources={
                    'deviceTemplateData': {
                        'type': 'object',
                        'objectId': 'deviceSample',
                        'properties': {
                            'hintString': 'try and buy more devices!'
                        },
                        'transformers': [
                            {
                                'inputPath': 'hintString',
                                'transformer': 'textToHint'
                            }
                        ]
                    }
                }
            )
        ).set_should_end_session(False)
        return handler_input.response_builder.response   
   

class DeletePeriodIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("DeletePeriod")(handler_input) or \
        (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and
        len(list(handler_input.request_envelope.request.arguments)) > 0 and
        list(handler_input.request_envelope.request.arguments)[0] == 'YesButton') or \
        (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and
        len(list(handler_input.request_envelope.request.arguments)) > 0 and
        list(handler_input.request_envelope.request.arguments)[0] == 'NoButton')

    def handle(self, handler_input):
        
        try:
            if  (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and
            len(list(handler_input.request_envelope.request.arguments)) > 0 and
            list(handler_input.request_envelope.request.arguments)[0] == 'YesButton'):
                confirm_status ='CONFIRMED'
            elif  (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and
            len(list(handler_input.request_envelope.request.arguments)) > 0 and
            list(handler_input.request_envelope.request.arguments)[0] == 'NoButton'):
                speech_text = "No deletion of data actioned "
                confirm_status = "NONE"
            else:
                confirm_status = handler_input.request_envelope.request.intent.confirmation_status.value
            if confirm_status == 'CONFIRMED':
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
                    speech_text = "There is no data to delete."
                else :
                    records = data["Items"]

                    for r in range(len(records)):
                        session_id = records[r]['SessionID']
                        table.delete_item(
                        Key={
                        'UserID': user_id,
                        'SessionID': session_id
                        }
                    )
                    speech_text = "Your data has been deleted"
                            
                  
        except BaseException as e:
            print(e)
            raise(e)
        
        handler_input.response_builder.speak(speech_text).set_card(SimpleCard('Hello', speech_text)).add_directive(
            RenderDocumentDirective(
                document= {
    "type": "APL",
    "version": "1.0",
    "theme": "dark",
    "import": [],
    "resources": [],
    "styles": {
      "headerStyle": {
        "values": [{
          "color": "#008080",
          "fontSize": "38",
          "fontWeight": 900
        }]
      },
      "textBlockStyle": {
        "values": [{
          "color": "indianred",
          "fontSize": "32"
        }]
      },
      "footerStyle": {
        "values": [{
          "fontSize": "20",
          "fontStyle": "italic"
        }]
      }
    },
    "layouts": {},
    "mainTemplate": {
        "items": [
            {
                "type": "Container",
                "items": [
                    {
                      "type": "Container",
                      "height": "400vh",
                      "width": "400vw",
                      "items": [
                        {
                          "type": "Container",
                          "paddingBottom": "70dp",
                          "paddingLeft": "40dp",
                          "paddingTop": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": " ",
                            "style": "headerStyle"
                          }]
                        }, {
                          "type": "Container",
                          "direction": "row",
                          "paddingBottom": "30dp",
                          "paddingLeft": "50dp",
                          "text-align": "center",
                          "vertical-align": "middle",
                          "items": [{
                            "type": "Text",
                            "text": "Deletion of period data :  ",
                            "style": "headerStyle"
                          }]
                        }, {
                            "type": "Container",
                          "direction": "row",
                          "paddingBottom": "10dp",
                          "paddingLeft": "200dp",
                          "text-align": "center",
                          "vertical-align": "middle",
                          "items": [{
                            "type": "Text",
                            "text": " " + speech_text,
                            "style": "headerStyle"
                          }]
                        }, {
           
                          "type": "Container",
                          "position": "absolute",
                          "bottom": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": "This is footer block. Try APL.",
                            "style": "footerStyle"
                          }]
                      }]
                    }
                ]
            }
        ]
    }
},
                datasources={
                    'deviceTemplateData': {
                        'type': 'object',
                        'objectId': 'deviceSample',
                        'properties': {
                            'hintString': 'try and buy more devices!'
                        },
                        'transformers': [
                            {
                                'inputPath': 'hintString',
                                'transformer': 'textToHint'
                            }
                        ]
                    }
                }
            )
        ).set_should_end_session(False)
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
            
            dyndb = boto3.resource('dynamodb', region_name='ap-southeast-2')
            table = dyndb.Table('Menstruation')
            trans = {}
            trans['UserID'] = user_id
            trans['SessionID'] = str(uuid.uuid4())
            trans['period_date'] = period_date
            datetime_object = datetime.strptime(period_date, '%Y-%m-%d')
            trans['add_date'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            table.put_item(Item=trans)  
                            
                  
        except BaseException as e:
            print(e)
            raise(e)
        
        speech_text = "You added your period date " + period_date
        
        handler_input.response_builder.speak(speech_text).set_card(SimpleCard('Hello', speech_text)).add_directive(
            RenderDocumentDirective(
                document= {
    "type": "APL",
    "version": "1.0",
    "theme": "dark",
    "import": [],
    "resources": [],
    "styles": {
      "headerStyle": {
        "values": [{
          "color": "#008080",
          "fontSize": "38",
          "fontWeight": 900
        }]
      },
      "textBlockStyle": {
        "values": [{
          "color": "indianred",
          "fontSize": "32"
        }]
      },
      "footerStyle": {
        "values": [{
          "fontSize": "20",
          "fontStyle": "italic"
        }]
      }
    },
    "layouts": {},
    "mainTemplate": {
        "items": [
            {
                "type": "Container",
                "items": [
                    {
                      "type": "Container",
                      "height": "400vh",
                      "width": "400vw",
                      "items": [
                        {
                          "type": "Container",
                          "paddingBottom": "70dp",
                          "paddingLeft": "40dp",
                          "paddingTop": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": " ",
                            "style": "headerStyle"
                          }]
                        }, {
                          "type": "Container",
                          "direction": "row",
                          "paddingBottom": "30dp",
                          "paddingLeft": "50dp",
                          "text-align": "center",
                          "vertical-align": "middle",
                          "items": [{
                            "type": "Text",
                            "text": "You added your period date:  ",
                            "style": "headerStyle"
                          }]
                        }, {
                            "type": "Container",
                          "direction": "row",
                          "paddingBottom": "10dp",
                          "paddingLeft": "300dp",
                          "text-align": "center",
                          "vertical-align": "middle",
                          "items": [{
                            "type": "Text",
                            "text": " " + datetime_object.strftime('%d-%b-%Y'),
                            "style": "headerStyle"
                          }]
                        }, {
           
                          "type": "Container",
                          "position": "absolute",
                          "bottom": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": "This is footer block. Try APL.",
                            "style": "footerStyle"
                          }]
                      }]
                    }
                ]
            }
        ]
    }
},
                datasources={
                    'deviceTemplateData': {
                        'type': 'object',
                        'objectId': 'deviceSample',
                        'properties': {
                            'hintString': 'try and buy more devices!'
                        },
                        'transformers': [
                            {
                                'inputPath': 'hintString',
                                'transformer': 'textToHint'
                            }
                        ]
                    }
                }
            )
        ).set_should_end_session(False)
        return handler_input.response_builder.response   
        
class ShowPeriodIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ShowPeriod")(handler_input)

    def handle(self, handler_input):
   
        speech_text = "Period dashboard "
        
        handler_input.response_builder.speak(speech_text).set_card(SimpleCard('Hello', speech_text)).add_directive(
         RenderDocumentDirective(
        document= {
    "type": "APL",
    "version": "1.0",
    "theme": "dark",
    "import": [
        {
        "name": "alexa-layouts",
        "version": "1.4.0"
      }
    ],
    "resources": [],
    "styles": {
      "headerStyle": {
        "values": [{
          "color": "#008080",
          "fontSize": "38",
          "fontWeight": 900
        }]
      },
      "textBlockStyle": {
        "values": [{
          "color": "indianred",
          "fontSize": "32"
        }]
      },
      "footerStyle": {
        "values": [{
          "fontSize": "20",
          "fontStyle": "italic"
        }]
      }
    },
    "layouts": {},
    "mainTemplate": {
        "items": [
            {
                "type": "Container",
                "items": [
                    {
                      "type": "Container",
                      "height": "400vh",
                      "width": "400vw",
                      "items": [
                        {
                          "type": "Container",
                          "paddingBottom": "70dp",
                          "paddingLeft": "40dp",
                          "paddingTop": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": " ",
                            "style": "headerStyle"
                          }]
                        }, {
                          "type": "Container",
                          "direction": "row",
                          "paddingBottom": "100dp",
                          "paddingLeft": "20dp",
                          "text-align": "center",
                          "vertical-align": "left",
                          "items": [{
                            "type": "Text",
                            "text": "Period Dashboard :  ",
                            "style": "headerStyle"
                          }]
                        }, {
                            "type": "Container",
                          "direction": "row",
                          "paddingBottom": "10dp",
                          "paddingLeft": "180dp",
                          "text-align": "center",
                          "vertical-align": "middle",
                          "items": [
                          {
                            "type": "AlexaButton",
                            "buttonText": "Last Period",
                            "id": "${data.id}_${exampleType}",
                            "buttonStyle": "${data.buttonStyle}",
                            "touchForward": "${touchForwardSetting}",
                            "primaryAction": {
                            "type": "SendEvent",
                            "arguments": [
                                "lastButton"
                            ]
                        }
                        } ,
                          {
                            "type": "AlexaButton",
                            "buttonText": "Next Period",
                            "id": "${data.id}_${exampleType}",
                            "buttonStyle": "${data.buttonStyle}",
                            "touchForward": "${touchForwardSetting}",
                            "primaryAction": {
                            "type": "SendEvent",
                            "arguments": [
                                "nextButton"
                            ]
                        }
                        },
                          {
                            "type": "AlexaButton",
                            "buttonText": "Delete Data",
                            "id": "${data.id}_${exampleType}",
                            "buttonStyle": "${data.buttonStyle}",
                            "touchForward": "${touchForwardSetting}",
                            "primaryAction": {
                            "type": "SendEvent",
                            "arguments": [
                                "deleteButton"
                            ]
                        }
                }
                          ]
                        }, {
           
                          "type": "Container",
                          "position": "absolute",
                          "bottom": "20dp",
                          "items": [{
                            "type": "Text",
                            "text": "This is footer block. Try APL.",
                            "style": "footerStyle"
                          }]
                      }]
                    }
                ]
            }
        ]
    }
},
                datasources={
                    'deviceTemplateData': {
                        'type': 'object',
                        'objectId': 'deviceSample',
                        'properties': {
                            'hintString': 'try and buy more devices!'
                        },
                        'transformers': [
                            {
                                'inputPath': 'hintString',
                                'transformer': 'textToHint'
                            }
                        ]
                    }
                }
            )
        ).set_should_end_session(False)
        return handler_input.response_builder.response   

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(AddPeriodIntentHandler())
sb.add_request_handler(NextPeriodIntentHandler())
sb.add_request_handler(DeletePeriodIntentHandler())
sb.add_request_handler(LastPeriodIntentHandler())
sb.add_request_handler(ShowPeriodIntentHandler())
sb.add_request_handler(DeleteAPLPeriodIntentHandler())



def lambda_handler(event, context):
    return sb.lambda_handler()(event, context)

if __name__ == "__main__":

    fake_event = """{
	"version": "1.0",
	"session": {
		"new": false,
		"sessionId": "amzn1.echo-api.session.b87ac02f-cf3b-4266-97ab-b5df93bac683",
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
				"canRotate": false,
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
					"canRotate": false,
					"canResize": false
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
			"apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5mZS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjM1OGU1NmU2LTIzMGUtNDE3ZS1iZWMxLTBmODg1MjVlOGJhZSIsImV4cCI6MTYzNTQwNjUyOCwiaWF0IjoxNjM1NDA2MjI4LCJuYmYiOjE2MzU0MDYyMjgsInByaXZhdGVDbGFpbXMiOnsiY29udGV4dCI6IkFBQUFBQUFBQXdBMEl5YTFidTVhNlY2M3hTV2JEK3N6S2dFQUFBQUFBQUNtTHZ2VlZHb0RVSWlreXR2WlFpc0lWS3U4RDJWTzlRaktQNnBCQ21WTUdhT08vbkZXWkYweGE1TWNOa3B0dnJJVWhFMXV3bkF2anc5Yi85UUtnb3NkRWlWemJ0am9WaE5ZaHl5ZW5MYXJYWGpxaW8vTmhpamhsSnE3NFgvU0tNaVRnWEtOOWJNVHN5SCtiM3hzaE9lNjRwNXFmakxJV1l0WUtPOW9UNkozZ2drQ0Q5YkVnV2swZUxUaWVMOXFYVzE1TllwSFRqa0lrYkYxdDQ5eGYyMk5iRWZ4T1BUYUZiMUpoT2wwakY5d0M5cFUrWUFXV0dQMUZ3YmwzZ3Voakt1Nnp0ZGdISXRwWHkwVVVsU0tWaWVsRUxOdG9zZGtPZVgwNW5raTN1WEJEcEZ5UnEwVGVSZGJHVllpOVU3eU1xQUJVNTRVWWNKMnFOL2djeHZQeGQ3djVqY09sYTdYSHhLM1hMU2VzQjhGZkNITU9FV1JadzdPM1NXMjFDZWxuQ1U2dnUwc1duak1pekJEIiwiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUhaTjNCSTJaUzVPWkNTNFZXRlVLVFVWUFVKTkZSR1ZPUTVJNVM3SEVIQ1Y2QkIzVTJDSEQ2VTZDVlpHTlA0R05FTEZOWFhDVVRORDUyUVRXMlZPREJIUDY3TlZCWEtDVE00RFJQSlpCWllNUlNWQ0ZBVFdUSVdaUTJZNjI2N0xSNEhGQjNEUTNFRlRUSVc0TVVMT1hZRklSRTYzVzZRMkJTMzY3RUhNNlM1TlJaU0NEWVU3NiIsInVzZXJJZCI6ImFtem4xLmFzay5hY2NvdW50LkFINVJWRVRYTjVYMjNHV1hSWlpONlJGS1JFUk0yWFpQVkZLVFlRRlNPSkVUTVRJNUxJM0ZHRlVLRENGRFlJTVpJWFpZQlpSREs0NTZTS00yV1FCRTdLR09EVUdJS1lWSUZPVkpBWUlLTEtPU01TM1ZTRVFIU1pHVk1FUUJXWEJLQ1VYVU1MUDNBTk5RMlFMWUhMSlFLWDdCRFlUWkM1Q1JDV0xZSEszTkUyQllYWTMzUlpQSlVMVlkyQ0RGRk9LNU5JV1AzTUtaN1lCNUhCSSJ9fQ.Z1wUXS2od3PvZVkA7gW34RsZEI1lINQiyuRiZaI_xVtLxlE4zdn7-agIwOCy731mVXfk5lPN1ry5yKGgYuNZLDlxACNXpLDBAMf7LdA4uOXhKkUz3cQ9SBEDThOqfxuQB5LxQNajzP2Yor9gUD4cVsGOLde9x8FxlcHtADuyU90gYYj5Rb2FGjkJUktqrnDRMprGUjBWkE4jY7cEbfFuDH7r6qCryKAZ8O699LerdONFI7fFCfhn4r-DMjaPeksdFg_XZm08LHtU0BnNlaEONj8XwWCCEJiZIIUp5ze8nfXpcc4KTZzTMwRB5fUusMcAQ-elZJuWctaGeaPifY035A"
		}
	},
	"request": {
		"type": "IntentRequest",
		"requestId": "amzn1.echo-api.request.d130214b-f58d-4e54-83d6-54c453b92da0",
		"locale": "en-US",
		"timestamp": "2021-10-28T07:30:28Z",
		"intent": {
			"name": "ShowPeriod",
			"confirmationStatus": "CONFIRMED",
			"slots": {
				"period": {
					"name": "period",
					"confirmationStatus": "NONE",
					"value" : "2021-10-15",
					"source": "USER"
				}
			}
		},
		"dialogState": "COMPLETED"
	}
}"""

    sb.lambda_handler()(json.loads(fake_event), None)
