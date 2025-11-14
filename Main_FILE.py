import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import create_tables, Sale, Stock, Book, Shop, Publisher

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD','alinka293001')
DB_NAME = os.getenv('DB_NAME', 'netology_db')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

DSN = 'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)


def load_test_data():
    Base.matada.drop_a(engine)
    Base.metada.creat_all(engine)
    session = Session()
    with open('tests_data.json', 'r', encoding='UTF-8') as f:
        data = json.load(f)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
    session.close()
    print('Tested files are successfully uploaded')

def find_purshases_by_publisher(publisher_input):

    with Session() as session:
        if publisher_input.isdigit():
            publisher_input = int(publisher_input)
            publisher_filter = Publisher.id == publisher_input
        else:
            publisher_filter = Publisher.name == publisher_input
        publisher = session.query(Publisher).filter(publisher_filter).one_or_none()

        if not publisher:
            print(f'Publisher {publisher_input} not founded.')
            return
        
        purchases_query = (
            session.query(Book.title, Shop.name, Sale.price, Sale.data_sale)
            .join(Stock, Stock.id_book == Book.id)
            .join(Sale, Sale.id_stock == Stock.id)
            .join(Shop, Stock.id_shop == Shop.id)
            .filter(Book.id_publisher == publisher.id)
            .order_by(Sale.data_sale)
        )

        print(f'Purchases from {publisher.name} publisher.')
        for title, shop_name, price, data_sale in purchases_query:
            print(f'{title} | {shop_name} | {price} | {data_sale.strftime('%D-%M-%Y')} ')

if __name__ == '__main__':
    print('1.Upload tested data')
    print('2.Find purchaces by publisher')
    choice = input('Choose action (1 or 2): ').strip()

    if choice == '1':
        load_test_data
    elif choice == '2':
        publisher_input = input("Type publisher name or publisher identificator: ").strip()
        find_purshases_by_publisher(publisher_input)
    else:
        print('Error. Programm is finished')