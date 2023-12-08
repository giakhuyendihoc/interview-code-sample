import csv
from io import StringIO

from flask import make_response

from main import app
from main.engines.analytics import get_ooo_report_data


@app.get("/ooo-requests/csv")
def export():
    csv_file = StringIO()
    fieldnames = [
        "Name",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sept",
        "Oct",
        "Nov",
        "Dec",
    ]
    cw = csv.writer(csv_file)
    cw.writerow(fieldnames)
    cw.writerows(get_ooo_report_data())

    response = make_response(csv_file.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    response.headers["Content-type"] = "text/csv"
    return response
