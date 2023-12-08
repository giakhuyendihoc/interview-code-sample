from main import app
from main.commons import exceptions
from main.commons.decorators import parse_args_with
from main.engines.user import get_user_by_email
from main.libs import access_token
from main.libs.password import is_valid_password
from main.schemas.users.auth import UserSignInSchema


@app.post("/users/sign-in")
@parse_args_with(UserSignInSchema)
def user_sign_in(args):
    email = args["email"]
    user = get_user_by_email(email)
    if user is None:
        raise exceptions.Unauthorized

    if not is_valid_password(args["password"], user.hashed_password):
        raise exceptions.BadRequest

    return {
        "access_token": access_token.encode(user.id),
    }
