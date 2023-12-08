from flask import jsonify

from main import app, db
from main.commons import exceptions
from main.commons.decorators import (
    access_token_required,
    authenticate_request_of_mentee,
    parse_args_with,
    user_role_authenticate,
)
from main.engines.user import get_ooo_requests_mentees_with_id
from main.enum import RequestStatus, Role
from main.models.ooo_request import RequestModel
from main.models.user import UserModel
from main.schemas.requests.accept_reject import Accept_Reject_RequestSchema


@app.put("/users/me/mentees/ooo-requests/<string:request_id>")
@access_token_required
@parse_args_with(Accept_Reject_RequestSchema)
@user_role_authenticate(Role.LEADER)
@authenticate_request_of_mentee()
def change_the_status(user_id, args, request_id):

    mentee_request = RequestModel.query.filter_by(id=int(request_id)).one_or_none()

    if mentee_request.status == RequestStatus.APPROVAL_WAITING:
        mentee_request.status = args["status"]
        if args["status"] == RequestStatus.REJECTED:
            mentee_request.reject_reason = args["reject_reason"]

        db.session.commit()

        return jsonify(
            sorted(
                [
                    {
                        "id": mentee_request.id,
                        "start_date": mentee_request.start_date.date(),
                        "end_date": mentee_request.end_date,
                        "pic_id": mentee_request.pic_id,
                        "purpose": mentee_request.purpose,
                        "status": mentee_request.status,
                        "reject_reason": mentee_request.reject_reason,
                        "contact_methods": mentee_request.contact_methods,
                        "user": {
                            "name": UserModel.query.filter_by(id=mentee_request.user_id)
                            .first()
                            .name,
                            "id": mentee_request.user_id,
                        },
                    }
                    for mentee_request in get_ooo_requests_mentees_with_id(user_id)
                ],
                key=lambda d: d["start_date"],
                reverse=True,
            )
        )

    else:
        raise exceptions.BadRequest
