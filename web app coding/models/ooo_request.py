from main import db
from main.models.base import TimestampMixin


class RequestModel(
    db.Model,
    TimestampMixin,
):
    __tablename__ = "ooo_request"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pic_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    purpose = db.Column(db.String(1500), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="approval_waiting")
    reject_reason = db.Column(db.String(1500), nullable=False, default="null")
    contact_methods = db.Column(db.String(1500), nullable=True, default="null")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # @property
    # def contact_methods(self):
    #     self.contact_methods = json.loads(self.contact_methods)
    #     return self.contact_methods


# model = RequestModel()
# model.contact_methods # ['slack']
