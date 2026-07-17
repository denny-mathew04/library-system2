from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



db_url = "postgresql+psycopg2://postgres:aleena%402004@localhost:5432/library-system2"
engine = create_engine(db_url)
LocalSession = sessionmaker(autocommit = False , autoflush = False , bind = engine)