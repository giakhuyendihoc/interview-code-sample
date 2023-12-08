import datetime
from collections import OrderedDict
from typing import List

from dateutil.relativedelta import relativedelta

from main import config
from main.enum import RequestStatus
from main.models.ooo_request import RequestModel
from main.models.user import UserModel


def get_ooo_report_data():
    year = datetime.datetime.now().year
    data = []
    for user in UserModel.query.all():
        days_off_in_month = OrderedDict(
            {
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
        )
        for month in days_off_in_month:
            ooo_requests = [
                *get_ooo_requests_in_month_case1(user.id, year, month),
                *get_ooo_requests_in_month_case2(user.id, year, month),
                *get_ooo_requests_in_month_case3(user.id, year, month),
                *get_ooo_requests_in_month_case4(user.id, year, month),
            ]
            days_off_in_month[month] += count_days_off(ooo_requests, month)

        data.append([user.name, *days_off_in_month.values()])

    return data


def get_ooo_requests_in_month_case1(user_id, year, month):
    """
    When month_of_start_date = month and month_of_end_date = month
    """
    first_date_of_month = get_first_date_of_month(year, month)
    first_date_of_next_month = get_first_date_of_next_month(year, month)
    return RequestModel.query.filter(
        RequestModel.user_id == user_id,
        RequestModel.status == RequestStatus.APPROVED,
        RequestModel.start_date >= first_date_of_month,
        RequestModel.start_date < first_date_of_next_month,
        RequestModel.end_date < first_date_of_next_month,
    ).all()


def get_ooo_requests_in_month_case2(user_id: int, year: int, month: int):
    """
    When month_of_start_date = month, and month < month_of_end_date
    """
    first_date_of_month = get_first_date_of_month(year, month)
    first_date_of_next_month = get_first_date_of_next_month(year, month)
    return RequestModel.query.filter(
        RequestModel.user_id == user_id,
        RequestModel.status == RequestStatus.APPROVED,
        RequestModel.start_date >= first_date_of_month,
        RequestModel.start_date < first_date_of_next_month,
        RequestModel.end_date >= first_date_of_next_month,
    ).all()


def get_ooo_requests_in_month_case3(user_id: int, year: int, month: int):
    """
    When month_of_start_date < month, month = month_of_end_date
    """
    first_date_of_month = get_first_date_of_month(year, month)
    first_date_of_next_month = get_first_date_of_next_month(year, month)
    return RequestModel.query.filter(
        RequestModel.user_id == user_id,
        RequestModel.status == RequestStatus.APPROVED,
        RequestModel.start_date < first_date_of_month,
        RequestModel.end_date >= first_date_of_month,
        RequestModel.end_date < first_date_of_next_month,
    ).all()


def get_ooo_requests_in_month_case4(user_id: int, year: int, month: int):
    """
    When month_of_start_date < month, month > month_of_end_date
    """
    return RequestModel.query.filter(
        RequestModel.user_id == user_id,
        RequestModel.status == RequestStatus.APPROVED,
        RequestModel.start_date < get_first_date_of_month(year, month),
        RequestModel.end_date >= get_first_date_of_next_month(year, month),
    ).all()


def count_days_off(
    ooo_requests: List[RequestModel],
    month: int,
):
    today = datetime.datetime.now()
    year = today.year
    days_off_count = 0
    for ooo_request in ooo_requests:
        k = (ooo_request.end_date - ooo_request.start_date).days
        for i in range(0, k + 1):
            date = ooo_request.start_date + datetime.timedelta(days=i)
            if date > today or date.month != month:
                continue

            # Ignore weekend
            if date.weekday() > 4:
                continue

            if str(date) not in config.HOLIDAYS[year][month]:
                days_off_count += 1

    return days_off_count


def get_first_date_of_month(year, month):
    return datetime.datetime(year, month, 1)


def get_first_date_of_next_month(year, month):
    return get_first_date_of_month(year, month) + relativedelta(months=1)
