import requests
from configure import api_key as api
from dateutil import parser
from datetime import datetime, timezone, timedelta


myToken,notion_token,databaseID= api['GDSC_slack_bot'],api["GDSC_notion_token"],api["GDSC_databaseId"]
#myToken,notion_token,databaseID= api['WS_slack_bot'],api["WS_notion_token"],api["WS_databaseId"]
#myToken,notion_token,databaseID= api['GDSC_slack_bot'],api["GDSC_notion_token"],api["GDSC_databaseId"]

def post_message( channel,isToday,title,start_date,end_date,position):
    """슬랙 메시지 전송"""
    
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+myToken},
        data={"channel": channel,"text":  "*"+isToday+"_Reminder_*\n"
                        +">*"+title+"*\n"
                        +">"+start_date
                        +end_date+" *"+isToday+"*\n"
                        +">"+position+"\n"
                        +"><!channel>"+"\n"
                        }
    )
def readDatabase(databaseId, ):
    headers = {
    "Authorization": "Bearer " + notion_token,
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
            position=[]
            Events=data["properties"]["Event Type"]["multi_select"]
            for Event in Events:
                name=Event['name']
                position.append(name)
            channel=[]
            for pos in position:
                if(pos=='Academic' or pos=="Bi-Weekly Review" 
                    or pos=="Keynote" or pos=="Management" 
                    or pos=="Offline Event" or pos=="Online Event"):
                    channel.append("#event")
                    break
                if(pos=='Backend Event' and pos=='Client Event' 
                   and pos=='Design Event' and pos=='Fronted Event' 
                   and pos=='ML Event'):
                    channel.append("#event")
                    break
                if(pos=='Backend Event'):
                    channel.append("#position-backends")
                if(pos=='Client Event'):
                    channel.append("#position-client")
                if(pos=='Design Event'):
                    channel.append("#design")
                if(pos=='Frontend Event'):
                    channel.append("#position-frontends")
                if(pos=='ML Event'):
                    channel.append("#position-machine-learning")
            
            position=str(position)
            if(position=="[]"):
                channel.append("#event")
                position=""
            
        except IndexError as e:
            
            
            if title=="":
                pass
            else:
                position=""
            if(not end_date):
                
                end_date=""
            
        except Exception as e:
            pass
            

        
        if (title!="" and start_date!=""):
            try:
                
                check=start_date[:10]
                #시간 계산
                if((start_date==tommorrow or check == tommorrow)
                    or(start_date==today or check == today)
                    #or(start_date==week or check == week)
                    ):
                    
                    #시작시간 = 2023-04-05
                    if(start_date ==start_date[:10]):
                        
                        if(end_date):
                            end_date=" ~ "+end_date
                        else:
                            end_date=""
                    else:
                        #print(title)
                        
                        start_date=start_date[:16]
                        start_date=datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
                        start_date=start_date.strftime('%Y-%m-%d %I:%M %p')
                        
                        if(end_date!=None):
                            
                            end_date=end_date[:16]
                            end_date=datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
                            end_date=" ~ "+str(end_date.strftime('%Y-%m-%d %I:%M %p'))
                        else:
                            end_date=""
                            
                    
                    if((start_date==tommorrow or check == tommorrow)):
                        isToday = "[Tomorrow] "
                    elif(start_date==today or check == today):
                        isToday = "[Today] "
                    for cn in channel:
                        post_message(cn,isToday,title,start_date,end_date,position)
                        
                        #post_message("#bot-lab",isToday,title,start_date,end_date,position)
                check=""    
            except TypeError as e:
                #print(e,e.__class__)
                pass
                
readDatabase(databaseID)