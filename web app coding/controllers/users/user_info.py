from flask import jsonify

from main import app
from main.commons import exceptions
from main.commons.decorators import access_token_required
from main.engines.user import get_list_role, get_user_by_id
from main.models.user import UserModel


@app.get("/users/me")
@access_token_required
def get_my_information(user_id):
    user = get_user_by_id(user_id)
    leader = UserModel.query.filter_by(id=user.leader_id).one_or_none()
    if user:
        return jsonify(
            {
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "lead_name": leader.name or None,
                "position": user.position,
                "roles": get_list_role(user.id),
            }
        )
    else:
        raise exceptions.NotFound(error_message="The user doesn't exist!")
