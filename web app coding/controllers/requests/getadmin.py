from flask import jsonify

from main import app
from main.commons.decorators import access_token_required, user_role_authenticate
from main.engines.user import get_list_role
from main.enum import Role
from main.models.ooo_request import RequestModel
from main.models.user import UserModel


@app.get("/ooo-requests")
@access_token_required
@user_role_authenticate(Role.ADMIN)
def get_ooo_requests_admin(**__):
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
                    "roles": get_list_role(request.user_id),
                    "user": {
                        "name": UserModel.query.filter_by(id=request.user_id)
                        .first()
                        .name,
                        "id": request.user_id,
                    },
                }
                for request in RequestModel.query.all()
            ],
            key=lambda d: d["start_date"],
            reverse=True,
        )
    )
