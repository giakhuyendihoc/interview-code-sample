import json

from flask import jsonify

from main import app, db
from main.commons.decorators import access_token_required, parse_args_with
from main.models.ooo_request import RequestModel
from main.models.user import UserModel
from main.schemas.requests.create_ooo_request import CreateRequestSchema


@app.post("/ooo-requests")
@access_token_required
@parse_args_with(CreateRequestSchema)
def create_ooo_request(args, user_id):

    ooo_request = RequestModel(
        start_date=args["start_date"],
        end_date=args["end_date"],
        pic_id=args["pic_id"] if "pic_id" in args else None,
        purpose=args["purpose"],
        user_id=user_id,
        contact_methods=json.dumps(args["contact_methods"]),
    )
    db.session.add(ooo_request)
    db.session.commit()

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
                    "contact_methods": json.loads(request.contact_methods),
                    "user": {
                        "name": UserModel.query.filter_by(id=request.user_id)
                        .first()
                        .name,
                        "id": request.user_id,
                    },
                }
                for request in RequestModel.query.filter_by(user_id=ooo_request.user_id)
            ],
            key=lambda d: d["start_date"],
            reverse=True,
        )
    )
