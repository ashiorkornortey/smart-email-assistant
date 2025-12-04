
from datetime import datetime, timedelta

TEMPLATES = {
    "Meeting": "Hi, I can meet {time1} or {time2}. Do either work for you?",
    "Request": "Thanks for your request. I will review and get back to you soon.",
    "Follow-up": "Sorry for the delay. I’ll get back to you by tomorrow.",
}

def suggest_times():
    now = datetime.utcnow()
    t1 = (now + timedelta(days=1, hours=2)).strftime("%Y-%m-%d %H:%M UTC")
    t2 = (now + timedelta(days=2, hours=3)).strftime("%Y-%m-%d %H:%M UTC")
    return t1, t2

def generate_reply(category):
    if category == "Meeting":
        t1, t2 = suggest_times()
        return TEMPLATES[category].format(time1=t1, time2=t2)
    return TEMPLATES.get(category, "")
