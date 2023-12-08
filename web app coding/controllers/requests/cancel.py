import datetime

from flask import jsonify

from main import app, db
from main.commons import exceptions
from main.commons.decorators import (
    access_token_required,
    authenticate_request_of_user,
    parse_args_with,
)
from main.models.ooo_request import RequestModel
from main.schemas.requests.cancel_ooo_request import CancelRequestSchema


@app.put("/users/me/ooo-requests/<int:request_id>")
@access_token_required
@authenticate_request_of_user()
@parse_args_with(CancelRequestSchema)
def cancel_request(user_id, args, request_id):

    ooo_request = RequestModel.query.filter_by(id=int(request_id)).one_or_none()

    if ooo_request.start_date >= datetime.datetime.utcnow():
        ooo_request.status = args["status"]

        db.session.commit()

        return jsonify(
            sorted(
                [
                    {
                        "id": req.id,
                        "start_date": req.start_date.date(),
                        "end_date": req.end_date,
                        "pic_id": req.pic_id,
                        "purpose": req.purpose,
                        "user_id": req.user_id,
                        "status": req.status,
                        "reject_reason": req.reject_reason,
                    }
                    for req in RequestModel.query.filter_by(user_id=user_id)
                ],
                key=lambda d: d["start_date"],
                reverse=True,
            )
        )

    else:
        raise exceptions.BadRequest
