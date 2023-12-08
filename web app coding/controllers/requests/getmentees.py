from flask import jsonify

from main import app
from main.commons.decorators import access_token_required, user_role_authenticate
from main.engines.user import get_ooo_requests_mentees_with_id
from main.enum import Role
from main.models.user import UserModel


@app.get("/users/me/mentees/ooo-requests")
@access_token_required
@user_role_authenticate(Role.LEADER)
def get_ooo_requests_mentees(user_id):
    request_data = get_ooo_requests_mentees_with_id(user_id)

    return jsonify(
        sorted(
            [
                {
                    "id": mentee_request.id,
                    "start_date": mentee_request.start_date.date(),
                    "end_date": mentee_request.end_date,
                    "pic_id": mentee_request.pic_id,
                    "purpose": mentee_request.purpose,
                    "user_id": mentee_request.user_id,
                    "status": mentee_request.status,
                    "reject_reason": mentee_request.reject_reason,
                    "user": {
                        "name": UserModel.query.filter_by(id=mentee_request.user_id)
                        .first()
                        .name,
                        "id": mentee_request.user_id,
                    },
                }
                for mentee_request in request_data
            ],
            key=lambda d: d["start_date"],
            reverse=True,
        )
    )
