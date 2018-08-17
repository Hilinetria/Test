from sqlalchemy import create_engine, MetaData
from settings import config
from models import activation


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=(activation,))


db_url = DSN.format(**config['postgres'])
engine = create_engine(db_url)
create_tables(engine)
