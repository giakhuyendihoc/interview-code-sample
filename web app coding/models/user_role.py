from main import db
from main.models.base import TimestampMixin


class UserRoleModel(db.Model, TimestampMixin):
    __tablename__ = "user_role"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable="False")
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable="False")
    status = db.Column(db.String(32), nullable=False, default="active")

    user = db.relationship("UserModel")
    role = db.relationship("RoleModel")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
