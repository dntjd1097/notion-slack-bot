import requests
import asyncio
from datetime import datetime, timezone, timedelta
from configure import NOTION_TOKEN
from channel import CHANNELS
from slack import post_message

from cal import calender

# from cal.create_event import create_event


def get_channel(positions):
    """Return Slack channel based on position"""

    # print(CHANNELS["channels"][0])
    channel = []
    for position in positions:
        if position in CHANNELS["channels"][0]:
            return CHANNELS["channels"][0][position]
        elif position in CHANNELS["channels"][1]:
            channel.append(CHANNELS["channels"][1][position])

    if positions == []:
        return ",".join(CHANNELS["channels"][2])
    return channel


def read_database(database_id):
    """Read events from Notion database and post reminders to Slack"""
    HEADERS = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-02-22",
    }
    response = requests.post(
        f"https://api.notion.com/v1/databases/{database_id}/query",
        headers=HEADERS,
    )

    datas = response.json()["results"]
    today = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    tomorrow = (datetime.now(timezone(timedelta(hours=9))) + timedelta(1)).strftime(
        "%Y-%m-%d"
    )
    week = (datetime.now(timezone(timedelta(hours=9))) + timedelta(7)).strftime(
        "%Y-%m-%d"
    )
    for data in datas:
        try:
            title = data["properties"]["Name"]["title"][0]["plain_text"]
            start_date = data["properties"]["Date"]["date"]["start"]
            end_date = data["properties"]["Date"]["date"].get("end")
            url = data["url"]
            positions = [
                p["name"] for p in data["properties"]["Event Type"]["multi_select"]
            ]

            channel = get_channel(positions)

        except Exception as e:
            # print(e,title)
            pass

        if title != "" and start_date != "":
            try:
                check = start_date[:10]
                # 시간 계산
                if (
                    (start_date == tomorrow or check == tomorrow)
                    or (start_date == today or check == today)
                    # or(start_date==week or check == week)
                ):
                    # print(title, start_date, end_date)
                    # 시작시간 = 2023-04-05
                    if end_date == None:
                        end_date = start_date
                        end = ""
                        # end_date ="빈값"
                    calender(title, start_date, end_date, url)
                    if start_date == start_date[:10]:  # 시작 날짜 = 년/월/일
                        if end_date:
                            end = " ~ " + end_date
                    else:
                        start_date = start_date[:16]

                        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
                        start_date = start_date.strftime("%Y-%m-%d %I:%M %p")
                        end_date = end_date[:16]
                        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
                        end_date = end_date.strftime("%Y-%m-%d %I:%M %p")

                        end = " ~ " + str(end_date)

                    if start_date == tomorrow or check == tomorrow:
                        isToday = "[내일] "
                    elif start_date == today or check == today:
                        isToday = "[오늘] "

                    positions = ", ".join(positions)
                    # print("전송중")
                    # print(title, start_date, end_date)

                    # print(type(positions),positions)
                    # create_event(title, start_date, end_date, url)
                    # print("전송")
                    if type(channel) == list:
                        for cn in channel:
                            post_message(
                                cn,
                                isToday,
                                title,
                                start_date,
                                end,
                                positions,
                                url,
                            )

                    else:
                        post_message(
                            channel,
                            isToday,
                            title,
                            start_date,
                            end,
                            positions,
                            url,
                        )

                    # post_message("#bot-lab",isToday,title,start_date,end_date,position)
                check = ""
            except TypeError as e:
                pass
