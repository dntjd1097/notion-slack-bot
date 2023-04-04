import requests, json
from mee6_py_api import API
import requests
from configure import api_key as api
from dateutil import parser
from dateutil import parser
from datetime import date, datetime, timezone, timedelta
 
def post_message( channel,title,start_date,end_date,position):
    """슬랙 메시지 전송"""
    myToken = api['slack_bot']
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+myToken},
        data={"channel": channel,"text":  ">*_Reminder_*\n"
                        +">*"+title+"*\n"
                        +">"+start_date
                        +end_date+"\n"
                        +">"+position+""
                        +"<!channel>"+"\n"
                        }
    )
def readDatabase(databaseId, ):
    headers = {
    "Authorization": "Bearer " + api["notion_token"],
    "Notion-Version": "2022-02-22"
    }
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.post(readUrl, headers=headers)
    datas = res.json()
    
            
    today = timezone(timedelta(hours=9))
    today = datetime.now(today)
    today = str(today)[:10]

    tommorrow = timezone(timedelta(hours=9))
    tommorrow = datetime.now(tommorrow)+ timedelta(1)
    tommorrow = str(tommorrow)[:10]

    week = timezone(timedelta(hours=9))
    week = datetime.now(week)+ timedelta(7)
    week = str(week)[:10]
   
    for data in datas['results']:
        try:
            title,start_date,end_date,position="","","",""
            title=data["properties"]["Name"]["title"][0]['plain_text']
            start_date=data["properties"]["Date"]['date']['start']
            end_date=data["properties"]["Date"]['date']['end']
            position=data["properties"]["Event Type"]["multi_select"][0]["name"]
            start_date = parser.parse(start_date)
            end_date = parser.parse(end_date)
            #print(end_date)
            
        except IndexError as e:
            if title=="":
                pass
            else:
                position=""
            if(not end_date):
                end_date=""
                #print(end_date)
            #print(e,title,start_date,end_date)
        except Exception:
            pass
            

        
        if (title!="" and start_date!=""):
            try:
                back=start_date[:10]
                #시간 계산
                if((start_date==tommorrow or back == tommorrow)
                   or(start_date==today or back == today)
                   or(start_date==week or back == week)
                   ):
                    #시작시간 = 2023-04-05
                    if(start_date ==start_date[:10]):
                        #print("?얘 머야?",title)
                        #end_date= " ~ "+end_date
                        post_message("#validator",title,start_date,end_date,position)
                    
                    else:
                        start_date=start_date[:16]
                        start_date=datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
                        start_date=start_date.strftime('%Y-%m-%d %I:%M %p')
                        if(end_date!=""):
                            type(end_date)
                            end_date=end_date[:16]
                            end_date=datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
                            end_date=" ~ "+str(end_date.strftime('%Y-%m-%d %I:%M %p'))

                        post_message("#validator",title,start_date,end_date,position)
                
                back=""    
            except TypeError as e:
                pass
                
            
               
readDatabase(api["databaseId"])