import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Sale, Stock, Book, Shop, Publisher

DSN = 'postgresql://postgres:alinka293001@localhost:5432/netology_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

#INSERT DATA FROM TASK 1
publisher_1 = Publisher(name = 'Пушкин')

book_1 = Book(title = 'Капитанская дочка', publisher = publisher_1)
book_2 = Book(title = 'Руслан и Людмила', publisher = publisher_1)
book_3 = Book(title = 'Евгений Онегин ', publisher = publisher_1)

shop_1 = Shop(name = 'Буквоед')
shop_2 = Shop(name = 'Лабиринт')
shop_3 = Shop(name = 'Книжный дом')

stock_1 = Stock(count = 1, book = book_1, shop = shop_1)
stock_2 = Stock(count = 2, book = book_2, shop = shop_1)
stock_3 = Stock(count = 3, book = book_3, shop = shop_3)
stock_4 = Stock(count = 4, book = book_1, shop = shop_1)

sale_1 = Sale(price = 600, data_sale = '09-11-2022', count = 1, stock = stock_1)
sale_2 = Sale(price = 500, data_sale = '08-11-2022', count = 2, stock = stock_2)
sale_3 = Sale(price = 580, data_sale = '05-11-2022', count = 3, stock = stock_3)
sale_4 = Sale(price = 490, data_sale = '02-11-2022', count = 4, stock = stock_4)
sale_5 = Sale(price = 600, data_sale = '26-11-2022', count = 1, stock = stock_1)

session.add_all([shop_1, shop_2, shop_3, stock_1, stock_2, stock_3, stock_4, sale_1, sale_2, sale_3, sale_4])
session.commit()


author_surname = input('Enter Author Surname and we will show you his available books: ')
for i in session.query(Sale).filter(Publisher.name == str(author_surname)).all():
    print(i)

session.close()