import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DATE

Base = declarative_base()


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), nullable=False)


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.Text, nullable=False)

    def __str__(self):
        return f'Publisher {self.id}: {self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String, nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f'Book {self.id}: ({self.title}, {self.publisher_id})'


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref='stock')

    def __str__(self):
        return f'Sale {self.id}: ({self.count}, {self.book_id}, {self.shop})'


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key = True)
    price = sq.Column(sq.Integer, nullable = False)
    data_sale = sq.Column(sq.DATE, nullable= False)
    count = sq.Column(sq.Integer, nullable = False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable= False)

    stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f'Sale {self.id}: ({self.price}, {self.data_sale}, {self.stock_id})'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)