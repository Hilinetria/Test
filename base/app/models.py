from sqlalchemy import (
    MetaData, Table, Column,
    Integer, DateTime
)

meta = MetaData()

activation = Table(
    'activation', meta,

    Column('id', Integer, primary_key=True),
    Column('is_activated', Integer, nullable=False),
    Column('pub_date', DateTime, nullable=False)
)
