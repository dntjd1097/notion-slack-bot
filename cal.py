from icalendar import Calendar, Event, Timezone
from datetime import datetime, timedelta
import pytz

# 캘린더 생성
def calender():
    cal = Calendar()
    cal.add('prodid', '-//My Calendar//example.com//EN')
    cal.add('version', '2.0')
    KST = pytz.timezone('Asia/Seoul')
    # 이벤트 생성
    event = Event()
    event.add('uid', '1234567890@example.com')
    event.add('summary', 'Meeting with John')
    event.add('location', 'Room 101')
    event.add('dtstamp', datetime.now(tz=KST))
    event.add('dtstart', datetime(2023, 4, 23, 9, 0, 0, tzinfo=KST))
    event.add('dtend', datetime(2023, 4, 23, 10, 0, 0,  tzinfo=KST))

    event.add('description', 'Discussing project status')
    cal.add_component(event)

    # 타임존 생성
    timezone = Timezone()
    timezone.add('tzid', 'Asia/Seoul')
    timezone.add('x-lic-location', 'Asia/Seoul')
    cal.add_component(timezone)

    # 캘린더 파일 저장
    with open('my_calendar.ics', 'wb') as f:
        f.write(cal.to_ical())
