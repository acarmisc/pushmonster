from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Text, \
    DateTime, create_engine

import uuid

engine = create_engine('sqlite:///pushmonster.db', echo=False)
Base = declarative_base()


class Db(object):

    def init(self):
        Base.metadata.create_all(engine)

    def get_session(self):
        from sqlalchemy.orm import sessionmaker
        session = sessionmaker()
        session.configure(bind=engine)
        return session()


class Application(Base):

    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    key = Column(String)
    description = Column(String)
    platform = Column(String)
    active = Column(Boolean, default=True)
    cert_file = Column(Text)
    cert_key = Column(Text)
    android_key = Column(Text)
    debug = Column(Boolean, default=False)

    def __repr__(self):
        return "<Application (name='%s')>" % self.name

    def get_by_id(self, id=None):
        if id:
            self.id = id

        s = Db().get_session()

        apps = s.query(Application).filter(Application.id == self.id).all()

        if len(apps) == 0:
            return None

        return apps[0]

    def auth(self, key=None):
        if key: self.key = key

        s = Db().get_session()

        apps = s.query(Application).filter(Application.key == self.key).all()

        if len(apps) == 0:
            return None

        return apps[0]

    def create(self):
        s = Db().get_session()
        s.add(self)
        s.commit()
        s.flush()

    def generate_key(self):
        s = Db().get_session()
        app = s.query(Application).filter(Application.id == self.id).one()
        app.key = uuid.uuid4().__str__()

        s.add(app)
        s.commit()

        s.flush()

        return self


class Notification(Base):

    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    application = Column(Integer)
    recipient = Column(String)
    sent_at = Column(DateTime)

    def __repr__(self):
        return "<Notification (name='%s')>" % self.id

    def create(self):
        s = Db().get_session()
        s.add(self)
        s.commit()


if __name__ == '__main__':
    db = Db()

    app = Application(name='test123')
    app.create()
