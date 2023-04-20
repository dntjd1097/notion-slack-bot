import datetime
from icalendar import Calendar, Event

# create a new calendar
cal = Calendar()

# create a new event
event = Event()

# set the event details
event.add('summary', 'My Event')
event.add('dtstart', datetime.datetime(2023, 4, 22, 10, 0, 0))
event.add('dtend', datetime.datetime(2023, 4, 22, 12, 0, 0))

# add the event to the calendar
cal.add_component(event)

# save the calendar to a file
with open('my_event.ics', 'wb') as f:
    f.write(cal.to_ical())