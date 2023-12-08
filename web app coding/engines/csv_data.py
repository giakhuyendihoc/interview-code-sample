import datetime
from calendar import monthrange

from sqlalchemy import and_

from config.base import BaseConfig
from main.models.ooo_request import RequestModel
from main.models.user import UserModel

global year
year = 2022


def get_ooo_request_data():
    data = dict()
    for user in UserModel.query.all():
        days_off_in_month = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
        }
        for mon in range(1, 13):
            total_days_off = (
                get_days_off_in_month_case1(user.id, mon)
                + get_days_off_in_month_case2(user.id, mon)
                + get_days_off_in_month_case3(user.id, mon)  # case 3 oke
                + get_days_off_in_month_case4(user.id, mon)
            )
            days_off_in_month[mon] += total_days_off
        data[user.id] = days_off_in_month
    return data


def first_date_of_month(month):
    d = datetime.date(year, month, 1)
    return str(d)


def last_date_of_month(month):
    any_day = datetime.date(year, month, 1)
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return str(next_month - datetime.timedelta(days=next_month.day))


def number_of_days_in_month(m):
    return monthrange(year, m)[1]


def is_weekend(day: datetime.date):
    return day.weekday() > 4


# dem so ngay nghi
def count_days_off(start_date: datetime.date, end_date: datetime.date, mon: int):
    k = (end_date - start_date).days
    days_off_count = 0
    for i in range(0, k + 1):
        date = start_date + datetime.timedelta(days=i)
        if not (
            str(date) in BaseConfig.HOLIDAYS[str(year)][str(mon)] or is_weekend(date)
        ):
            days_off_count += 1
    return days_off_count


# case 1: 1st < start_date < end_date < 31st
def get_days_off_in_month_case1(user_id, mon):
    filter_rule = and_(
        RequestModel.start_date >= first_date_of_month(mon),
        RequestModel.end_date <= last_date_of_month(mon),
    )
    ooo_requests = (
        RequestModel.query.filter(RequestModel.user_id == user_id)
        .filter(filter_rule)
        .all()
    )
    total_days_off = 0
    for ooo_request in ooo_requests:
        total_days_off += count_days_off(
            ooo_request.start_date.date(), ooo_request.end_date.date(), mon
        )
    return total_days_off


# case 2: start_date < 1st < end_date < 31st
def get_days_off_in_month_case2(user_id, mon):
    filter_rule = and_(
        RequestModel.start_date <= first_date_of_month(mon),
        RequestModel.end_date <= last_date_of_month(mon),
        RequestModel.end_date >= first_date_of_month(mon),
    )
    ooo_requests = (
        RequestModel.query.filter(RequestModel.user_id == user_id)
        .filter(filter_rule)
        .all()
    )
    total_days_off = 0
    for ooo_request in ooo_requests:
        d = count_days_off(
            str_to_date(first_date_of_month(mon)), ooo_request.end_date.date(), mon
        )
        total_days_off += d
    return total_days_off


# case 3: 1st < start_date < 31st < end_date
def get_days_off_in_month_case3(user_id, mon):
    filter_rule = and_(
        RequestModel.start_date >= first_date_of_month(mon),
        RequestModel.end_date >= last_date_of_month(mon),
        RequestModel.start_date <= last_date_of_month(mon),
    )
    ooo_requests = (
        RequestModel.query.filter(RequestModel.user_id == user_id)
        .filter(filter_rule)
        .all()
    )
    total_days_off = 0
    for ooo_request in ooo_requests:
        d = count_days_off(
            ooo_request.start_date.date(), str_to_date(last_date_of_month(mon)), mon
        )
        total_days_off += d
    return total_days_off


# case 4: start_date < 1st < 31st < end_date
def get_days_off_in_month_case4(user_id, mon):
    filter_rule = and_(
        RequestModel.start_date <= first_date_of_month(mon),
        RequestModel.end_date >= last_date_of_month(mon),
    )
    ooo_requests = (
        RequestModel.query.filter(RequestModel.user_id == user_id)
        .filter(filter_rule)
        .all()
    )
    total_days_off = 0
    for ooo_request in ooo_requests:
        total_days_off += number_of_days_in_month(mon)
    return total_days_off


def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
