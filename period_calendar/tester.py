items_array =  [
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
                    "text": "Your period dates:  ",
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
                    "text": " fake title",
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

items_array[0]['items'][0]['items'].append({
                    "type": "Text",
                    "text": " fake title 2",
                    "style": "headerStyle"
                    })

print(items_array)