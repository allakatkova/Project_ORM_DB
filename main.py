import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

NAME_DATABASE = 'sales_books'
USER_DATABASE = 'postgres'
PASS_USER_DATABASE = 'postgres'
HOST_NAME = 'localhost'
PORT_HOST = '5432'

Base = declarative_base()


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':

    DSN = "postgresql://" + USER_DATABASE + ":" + PASS_USER_DATABASE + \
        "@" + HOST_NAME + ":" + PORT_HOST + "/" + NAME_DATABASE
    engine = sq.create_engine(DSN)

    print(sqlalchemy.__version__)
