from sqlalchemy import Index

from main import db
from main.models.base import TimestampMixin


class UserModel(
    db.Model,
    TimestampMixin,
):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False)
    hashed_password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    phone = db.Column(db.String(32), nullable=False)
    position = db.Column(db.String(64), nullable=False)

    Index("idx_email", email, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leader_id = 1
        self.phone = "0723250535"
        self.position = "test person"
