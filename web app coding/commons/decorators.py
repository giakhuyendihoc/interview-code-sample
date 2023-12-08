from functools import wraps
from typing import Type

import marshmallow
import werkzeug.exceptions
from flask import request

from main.engines.user import get_list_role
from main.libs import access_token
from main.models.ooo_request import RequestModel
from main.models.user import UserModel

from . import exceptions


def get_request_args():
    if request.method == "GET":
        return request.args.to_dict()

    return request.get_json() or {}


def parse_args_with(schema: Type[marshmallow.Schema]):
    def parse_args_with_decorator(f):
        @wraps(f)
        def wrapper(**kwargs):
            try:
                request_args = get_request_args()
                parsed_args = schema().load(request_args)
                return f(**kwargs, args=parsed_args)

            except werkzeug.exceptions.BadRequest as e:
                raise exceptions.BadRequest(error_message=e.description)

            except marshmallow.ValidationError as e:
                raise exceptions.ValidationError(error_data=e.messages)

        return wrapper

    return parse_args_with_decorator


def access_token_required(f):
    @wraps(f)
    def wrapper(**kwargs):
        try:
            token = request.headers["Authorization"][len("Bearer ") :]
            user_id = access_token.decode(token)["sub"]
            kwargs["user_id"] = user_id
            return f(**kwargs)

        except werkzeug.exceptions.Unauthorized as e:
            raise exceptions.Unauthorized(error_message=e.description)

    return wrapper


def user_role_authenticate(user_role_required):
    def _user_role_authenticate(f):
        @wraps(f)
        def wrapper(**kwargs):
            roles = get_list_role(kwargs["user_id"])
            if user_role_required in roles:
                return f(**kwargs)
            else:
                raise exceptions.Forbidden(
                    error_message=f"You need to have {user_role_required} "
                    "role to perform this operation."
                )

        return wrapper

    return _user_role_authenticate


def authenticate_request_of_mentee():
    def authenticate_request_of_mentee_by_id(f):
        @wraps(f)
        def wrapper(**kwargs):
            request_id = kwargs["request_id"]
            ooo_request: RequestModel = RequestModel.query.filter_by(
                id=int(request_id)
            ).one_or_none()

            requester_id = ooo_request.user_id
            requester: UserModel = UserModel.query.filter_by(
                id=int(requester_id)
            ).one_or_none()

            if requester.leader_id == kwargs["user_id"]:
                return f(**kwargs)
            else:
                raise exceptions.Forbidden(
                    error_message="You are not the leader of "
                    "the user created the OOO request."
                )

        return wrapper

    return authenticate_request_of_mentee_by_id


def authenticate_request_of_user():
    def authenticate_request_of_user_by_id(f):
        @wraps(f)
        def wrapper(**kwargs):
            requests_id = [_request.id for _request in RequestModel.query.all()]
            if kwargs["request_id"] in requests_id:
                request_id = kwargs["request_id"]
                ooo_request: RequestModel = RequestModel.query.filter_by(
                    id=int(request_id)
                ).one_or_none()

                if ooo_request.user_id == kwargs["user_id"]:
                    return f(**kwargs)
                else:
                    raise exceptions.Forbidden()
            else:
                raise exceptions.NotFound(error_message="OOO-request not found")

        return wrapper

    return authenticate_request_of_user_by_id
