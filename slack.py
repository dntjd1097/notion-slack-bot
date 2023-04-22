from slack_sdk import WebClient
from configure import MY_TOKEN
import os


async def post_message(channel, isToday, title, start_date, end_date, position, url):
    """슬랙 메시지 전송"""
    client = WebClient(token=MY_TOKEN)

    # 이전 메시지들을 확인하여 파일 업로드 이전에 메시지를 먼저 보냄

    response = client.chat_postMessage(
        channel=channel,
        text="fallback text message",
        blocks=[
            {
                "type": "header",
                "text": {"type": "plain_text", "text": isToday + title, "emoji": True},
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": "*🕘* " + start_date + end_date}
                ],
            },
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn", "text": position + " "}},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "@channel"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Notion", "emoji": True},
                    "value": "click_me_123",
                    "url": url,
                    "action_id": "button-action",
                },
            },
        ],
    )
    latest_ts = None
    conversation_history = client.conversations_history(channel=channel)
    for message in conversation_history["messages"]:
        if "ts" in message:
            latest_ts = message["ts"]
        if "bot_id" in message:
            break
    # 파일을 업로드함
    file_path = title + ".ics"
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
            response = client.files_upload_v2(
                channel=channel,
                file=file_content,
                filename=title + ".ics",
                thread_ts=latest_ts,
                # initial_comment='iCal 파일입니다.'
            )

        # os.remove(file_path)
    except FileNotFoundError as e:
        print("Error: %s : %s" % ("my_calendar.ics", e.strerror))
    except UnboundLocalError as e:
        print(e)
    except OSError as e:
        print("Error: %s : %s" % (file_path, e.strerror))
