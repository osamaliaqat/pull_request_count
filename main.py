from fastapi import FastAPI, Form
import collections
from typing import List, Dict
from enum import Enum
from fastapi import FastAPI, Form
import requests
from fastapi.responses import ORJSONResponse
from datetime import date, datetime, timedelta, timezone
from dateutil.rrule import rrule, MONTHLY, MO, TU, WE, TH, FR , WEEKLY, DAILY, HOURLY

app = FastAPI()


class Interval(str, Enum):
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"


def calculate_datetimes_between(from_date: date, to_date: date, interval: Interval) -> List[datetime]:
    if interval == Interval.month:
        return list(rrule(MONTHLY, bymonthday=1, dtstart=from_date,until=to_date))
    if interval == Interval.week:
        return list(rrule(WEEKLY, byweekday=[MO], dtstart=from_date, until=to_date))
    if interval == Interval.day:
        return list(rrule(DAILY, dtstart=from_date, until=to_date))
    if interval == Interval.hour:
        return list(rrule(HOURLY, dtstart=from_date, until=to_date))


@app.get("/get_pull_request_count", response_class=ORJSONResponse)
async def get_pull_request(from_date: str = Form(...), to_date: str = Form(...),
                           interval: Interval = Form(...), repository: str = Form(...)):
    api_url = "https://api.github.com/repos/"+repository+"/pulls"
    response = requests.get(api_url)
    if response.status_code == 200:
        try:
            res = response.json()
            from_date = datetime.strptime(from_date, "%Y,%m,%d")
            to_date = datetime.strptime(to_date, "%Y,%m,%d")
            from_ = from_date
            to_ = to_date
            response_dates = []
            calculated_dates = calculate_datetimes_between(from_, to_, interval)
            for r in res:
                res = r['created_at']
                res = datetime.strptime(res, "%Y-%m-%dT%H:%M:%SZ")
                for cal in calculated_dates:
                    cal = cal
                    if res <= cal:
                        response_dates.append(res)
            count = collections.Counter(response_dates)
            result = [{'timestamp': k, 'count': v} for k, v in count.items()]
            return [{"result": result}]

        except (ValueError, Exception) as e:
            error = str(e)
            return [{"Message": error}]
    else:
        return [{"Message": "Repo does not exist or Request is not valid"}]

















