import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

NAME_DATABASE = 'sales_books'
USER_DATABASE = 'postgres'
PASS_USER_DATABASE = 'postgres'
HOST_NAME = '10.0.2.15'  # 'localhost'
PORT_HOST = '5432'

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':

    # инициализация подключения через строку провайдера DSN
    DSN = "postgresql://" + USER_DATABASE + ":" + PASS_USER_DATABASE + \
        "@" + HOST_NAME + ":" + PORT_HOST + "/" + NAME_DATABASE
    engine = sq.create_engine(DSN)
    create_tables(engine)

    # инициализация сессии
    Session = sessionmaker(bind=engine)
    session = Session

    # publisher = Publisher(name="Издатель")
    # print(publisher.id, publisher.name)
