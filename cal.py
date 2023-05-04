from icalendar import Calendar, Event, Timezone
from datetime import datetime, timedelta
import pytz


# 캘린더 생성
def calender(title, start, end, url):
    try:
        if start == start[:10]:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date() + timedelta(1)
        else:
            start_date = start[:16]
            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
            end_date = end[:16]
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

        cal = Calendar()
        cal.add("prodid", "-//My Calendar//example.com//EN")
        cal.add("version", "2.0")
        cal.add("method", "PUBLISH")
        KST = pytz.timezone("Asia/Seoul")
        # 이벤트 생성
        event = Event()
        event.add("uid", "dntjd1097@gmail.com")
        event.add("summary", title)

        event.add("dtstamp", datetime.now(tz=KST))
        event.add("dtstart", start_date)
        event.add("dtend", end_date)

        event.add("description", url)
        cal.add_component(event)

        # 타임존 생성
        timezone = Timezone()
        timezone.add("tzid", "Asia/Seoul")
        timezone.add("x-lic-location", "Asia/Seoul")
        cal.add_component(timezone)

        # 캘린더 파일 저장
        with open(title + ".ics", "wb") as f:
            f.write(cal.to_ical())
    except Exception as e:
        print(e)
        pass


# calender()
