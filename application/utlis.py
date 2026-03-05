from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

def ist_now():
    return datetime.now(IST)


# Ihave creaed this file cause earlier the time stamps were in UTC and I had to convert them to IST every time I wanted to display them. Now, with this utility function, I can directly get the current time in IST whenever I need it.
