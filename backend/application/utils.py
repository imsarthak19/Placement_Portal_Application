from datetime import datetime
from zoneinfo import ZoneInfo
import json
from application.extensions import redis_client
IST = ZoneInfo("Asia/Kolkata")

def ist_now():
    return datetime.now(IST)


# I have creaed this file cause earlier the time stamps were in UTC and I had to convert them to IST every time I wanted to display them. Now, with this utility function, I can directly get the current time in IST whenever I need it.

# Redis configurartnion and utility functions for caching
def get_cache(key):
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print(f"REDIS GET ERROR: {e}")
    return None

def set_cache(key, value, expiry=60):
    try:
        redis_client.setex(key, expiry, json.dumps(value))
    except Exception as e:
        print(f"REDIS SET ERROR: {e}")