from main import db
from main.models.base import TimestampMixin


class RoleModel(db.Model, TimestampMixin):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key="True")
    title = db.Column(db.String(64), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
