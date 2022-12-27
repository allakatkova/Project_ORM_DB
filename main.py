import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import json
import datetime

NAME_DATABASE = 'sales_books'
USER_DATABASE = 'postgres'
PASS_USER_DATABASE = 'postgres'
HOST_NAME = '10.0.2.15'
PORT_HOST = '5432'

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey(
        "publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="books")


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship(Book, backref='stocks')
    shop = relationship(Shop, backref='stocks')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref='sales')


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def search_db(criterion):
    print("название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки")
    if criterion[0] == 1:
        result = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale, Sale.count).join(
            Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.id == criterion[1]).all()
        for record in result:
            print(f'{record.title} | {record.name} | '
                  f'{str(record.price)} | {record.date_sale.date()}')
    elif criterion[0] == 2:
        result = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale, Sale.count).join(
            Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name == criterion[1]).all()
        for record in result:
            print(f'{record.title} | {record.name} | '
                  f'{str(record.price)} | {record.date_sale.date()}')


if __name__ == '__main__':

    # инициализация подключения через строку провайдера DSN
    DSN = "postgresql://" + USER_DATABASE + ":" + PASS_USER_DATABASE + \
        "@" + HOST_NAME + ":" + PORT_HOST + "/" + NAME_DATABASE
    engine = sq.create_engine(DSN)
    create_tables(engine)

    # инициализация сессии
    Session = sessionmaker(bind=engine)
    session = Session()

    with open('fixtures/tests_data.json', encoding='utf-8') as file:
        file_content = json.loads(file.read())

    for line in file_content:
        if line['model'] == 'publisher':
            publisher = Publisher(id=line['pk'], name=line['fields']['name'])
            session.add(publisher)
        if line['model'] == 'book':
            book = Book(id=line['pk'], title=line['fields']['title'],
                        id_publisher=line['fields']['id_publisher'])
            session.add(book)
        if line['model'] == 'shop':
            shop = Shop(id=line['pk'], name=line['fields']['name'])
            session.add(shop)
        if line['model'] == 'stock':
            stock = Stock(id=line['pk'], id_shop=line['fields']['id_shop'], id_book=line['fields']['id_book'],
                          count=line['fields']['count'])
            session.add(stock)
        if line['model'] == 'sale':
            sale = Sale(id=line['pk'], price=line['fields']['price'], date_sale=line['fields']['date_sale'],
                        count=line['fields']['count'], id_stock=line['fields']['id_stock'])
            session.add(sale)
        else:
            pass
    session.commit()

    id_criterion = int(input("""Выберите из предложенных пунктов:
    1. Поиск по идентификатору издателя
    2. Поиск по имени издателя
    """))
    while True:
        if id_criterion == 1:
            question_text = "Введите идентификатор издателя: "
            break
        elif id_criterion == 2:
            question_text = "Введите имя издателя: "
            break
        else:
            "Введенные данные не удалось распознать"
    criterion = input(question_text)
    search_db([id_criterion, criterion])
