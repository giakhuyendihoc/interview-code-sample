from typing import Optional

from main import db
from main.libs.password import generate_hashed_password
from main.models.ooo_request import RequestModel
from main.models.user import UserModel
from main.models.user_role import UserRoleModel


def create_user(email: str, password: str) -> UserModel:
    user = UserModel(
        email=email,
        hashed_password=generate_hashed_password(password),
    )

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email: str) -> Optional[UserModel]:
    return UserModel.query.filter(
        UserModel.email == email,
    ).one_or_none()


def get_user_by_id(id: int) -> Optional[UserModel]:
    return UserModel.query.filter(
        UserModel.id == id,
    ).one_or_none()


def get_ooo_requests_mentees_with_id(leader_id):

    mentees = []
    for mentee in UserModel.query.filter_by(leader_id=leader_id):
        mentees.append(mentee.id)

    request_data = []
    for mentee in mentees:
        for mentee_request in RequestModel.query.filter_by(user_id=mentee):
            request_data.append(mentee_request)

    return request_data


def get_list_role(user_id):
    user_roles = UserRoleModel.query.filter(UserRoleModel.user_id == user_id).all()
    roles = []
    if user_roles:
        roles = [user_role.role.title for user_role in user_roles]
    return roles
