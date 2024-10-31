from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.db.Models.models import *


#todo: can be converted to env variable via os.environ.get('DB_URL')
connection_url = db_url = "postgresql://admin:1234@localhost:5437/missions_db"
engine = create_engine(connection_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

def init_db():
    Base.metadata.create_all(bind=engine)
