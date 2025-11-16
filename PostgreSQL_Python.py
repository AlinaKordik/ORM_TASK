import psycopg2

# Connected to db
conn = psycopg2.connect(
    database="clients_db",
    user="postgres",
    password="alinka293001")


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        
        CREATE TABLE IF NOT EXIST client(
            client_id SERIAL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            surname VARCHAR(20) NOT NULL,
            email VARCHAR(60) NOT NULL
            );
        """)

        cur.execute('''

        CREATE TABLE IF NOT EXIST phone(
            phone_id SERIAL PRIMARY KEY,
            client_id INT NOT NULL,
            phone_number VARCHAR(100),
            FOREIGN KEY (client_id) REFERENCE client(client_id)
            );
        ''')
        conn.commit()


def add_client(conn, first_name, last_name, email, phones=None):
    conn.first_name = first_name
    conn.last_name = last_name
    conn.phones = phones
    conn.email = email

    first_name = int('Put your name: ')
    last_surname = int('Put your name: ')
    email = int('Put your email: ')

    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(name, surname, email) 
        VALUES ('{first_name}', '{last_name}', '{email}')
        """)


def add_phone(conn, client_id, phones):
    conn.client_id = client_id
    conn.phones = phones
    phones = int('Put your phone numbers: ')

    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone(phone_number) 
        VALUES ('{phones}')
        """)


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    conn.client_id = client_id
    conn.first_name = first_name
    conn.last_name = last_name
    conn.email = email
    conn.phones = phones

    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client SET first_name = %s WHERE id=%s;
        """)


def delete_phone(conn, client_id, phones):
    conn.client_id = client_id
    conn.phones = phones


with conn.cursor() as cur:
    cur.execute("""
        DELETE FROM phone WHERE id=%s;
        """)


def delete_client(client_id):
    conn.client_id = client_id


with conn.cursor() as cur:
    cur.execute("""
        DELETE FROM client WHERE id=%s;
        """)


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if conn.first_name == first_name:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT * FROM client;
            """)
            print(cur.fatchall())


# Close the connection
conn.close()
