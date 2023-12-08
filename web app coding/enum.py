class EnumBase:
    @classmethod
    def get_list(cls):
        return [getattr(cls, attr) for attr in dir(cls) if attr.isupper()]


class ContactMethod(EnumBase):
    SLACK = "slack"
    PHONE = "phone"
    EMAIL = "email"


class RequestStatus(EnumBase):
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    APPROVAL_WAITING = "approval_waiting"


class Role(EnumBase):
    USER = "user"
    ADMIN = "admin"
    LEADER = "leader"
