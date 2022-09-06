import db
import datetime
import uuid

class JournalUserActions(db.Base):
    __tablename__ = "journal_user_actions"
    __table_args__ = {"schema": "medupdates"}

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    journal_id = db.Column(db.UUID(as_uuid=True))
    action_name = db.Column(db.Integer)
    action_by_userid = db.Column(db.UUID)
    action_by_usertype = db.Column(db.Integer)
    action_at = db.Column(db.DateTime, default=datetime.datetime.now)
    user_agent = db.Column(db.String)
