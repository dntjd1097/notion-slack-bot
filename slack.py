from slack_sdk import WebClient
from configure import MY_TOKEN

def post_message(channel, isToday, title, start_date, end_date, position,url):
    """슬랙 메시지 전송"""
    client = WebClient(token=MY_TOKEN)
    response = client.chat_postMessage(
        channel=channel, # Channel ID
        text= "fallback text message",
        blocks= [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": isToday+title,
				"emoji": True
			}
		},
        {
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "*🕘* "+ start_date+end_date
				}
			]
		},
		{
			"type": "divider"
		},
		
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": position+" "
			}
		},

		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "@channel"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Notion",
					"emoji": True
				},
				"value": "click_me_123",
				"url": url,
				"action_id": "button-action"
			}
		}
	]
    )
    
