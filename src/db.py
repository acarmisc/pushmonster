from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Text, create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///pushmonster.db', echo=True)
Base = declarative_base()


class Db(object):

    def init(self):
        Base.metadata.create_all(engine)


class Application(Base):

    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    code_name = Column(String)
    description = Column(String)
    platform = Column(String)
    active = Column(Boolean)
    cert_file = Column(Text)
    cert_key = Column(Text)
    debug = Column(Boolean)

    def __repr__(self):
        return "<User(name='%s')>" % self.name
