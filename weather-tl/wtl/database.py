from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from req2df.config import get_settings

engine = create_engine(str(get_settings().database_url))

@lru_cache
def create_session() -> scoped_session:
  Session = scoped_session(
      sessionmaker(autocommit=False, autoflush=False, bind=engine)
  )
  return Session

