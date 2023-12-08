from flask import jsonify

from main import app
from main.commons.decorators import access_token_required
from main.models.ooo_request import RequestModel
from main.models.user import UserModel


@app.get("/users/me/ooo-requests")
@access_token_required
def get_ooo_request_self(user_id):

    return jsonify(
        sorted(
            [
                {
                    "id": request.id,
                    "start_date": request.start_date.date(),
                    "end_date": request.end_date,
                    "pic_id": request.pic_id,
                    "purpose": request.purpose,
                    "status": request.status,
                    "reject_reason": request.reject_reason,
                    "user": {
                        "name": UserModel.query.filter_by(id=request.user_id)
                        .first()
                        .name,
                        "id": request.user_id,
                    },
                }
                for request in RequestModel.query.filter_by(user_id=user_id)
            ],
            key=lambda d: d["start_date"],
            reverse=True,
        )
    )
