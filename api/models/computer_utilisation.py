from datetime import datetime
from shared import db

## SQLAlchemy model for Odin's computer utilisation stats
class ComputerUtilisation(db.Model):
    __tablename__ = 'odin_computer_utilisation'

    ## Primary Key
    identifier = db.Column(db.Integer, primary_key=True)
    ## Model specific
    mac_address = db.Column(db.String(255), unique=True, nullable=False)
    seen_count_current = db.Column(db.Integer, unique=False, nullable=False, default=0)
    seen_count_highest = db.Column(db.Integer, unique=False, nullable=False, default=0)
    os_count_windows = db.Column(db.Integer, unique=False, nullable=False, default=0)
    os_count_linux = db.Column(db.Integer, unique=False, nullable=False, default=0)
    os_count_mac = db.Column(db.Integer, unique=False, nullable=False, default=0)
    os_count_unknown = db.Column(db.Integer, unique=False, nullable=False, default=0)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ## Meta
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @property
    def serialize(self):
        return {
            'id': self.identifier,
            'mac_address': self.mac_address,
            'seen_count_current': self.seen_count_current,
            'seen_count_highest': self.seen_count_highest,
            'os_count_windows': self.os_count_windows,
            'os_count_linux': self.os_count_linux,
            'os_count_mac': self.os_count_mac,
            'os_count_unknown': self.os_count_unknown,
            'last_seen': self.last_seen
        }
