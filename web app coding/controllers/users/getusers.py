from flask import jsonify

from main import app
from main.commons.decorators import access_token_required
from main.models.user import UserModel


@app.get("/users")
@access_token_required
def get_users(user_id):
    response = sorted(
        [
            {"id": user.id, "name": user.name}
            for user in UserModel.query.filter(UserModel.id != user_id)
        ],
        key=lambda d: d["name"],
    )
    response.insert(0, dict())
    return jsonify(response)
