from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from wtl.config import get_settings

engine = create_engine(str(get_settings().database_url))

@lru_cache
def create_session() -> scoped_session:
  Session = scoped_session(
      sessionmaker(autocommit=False, autoflush=False, bind=engine)
  )
  return Session

def create_cursor(session:scoped_session):
  return session.connection().connection.cursor()

