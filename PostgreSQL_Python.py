import psycopg2
from psycopg2.sql import SQL, Identifier


#Function to create new tables
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                name VARCHAR(40) NOT NULL,
                surname VARCHAR(40) NOT NULL,
                email VARCHAR(320) UNIQUE NOT NULL,
                CONSTRAINT proper_email CHECK (email ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$')
            );
        """)

        cur.execute('''

        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            number INTEGER UNIQUE NOT NULL,
            client INTEGER NOT NULL REFERENCES client(id) ON DELETE CASCADE
            );
        ''')

        conn.commit()

# Function to add new client
def add_client(first_name, last_name, email, phones=None):

    with conn.cursor() as cur:
        cur.execute("""
            SELECT email
            FROM client
            WHERE email = &s;
            """, (email,))
        if len(cur.fetchall()) > 0:
            print('Client with this email already exists')
            return
        
    with conn.cursor() as cur:
        cur.execute("""
        INSERT into CLIENTS (name, surname, email)
        VALUES (%s, %s, %s) RETURNING id;
        """, (first_name, last_name, email))
    print(f'ID created client: ', cur.fetchone())

#Function to add phone numbers for existing clients

def add_phone(conn, client, number):

    with conn.cursor() as cur:
        cur.execute("""
            SELECT number
            FROM phone
            WHERE number = &s;
            """, (number,))
        if len(cur.fetchall()) > 0:
            print('This number already exists')
            return
        
        
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id
            FROM client
            WHERE id = &s;
            """, (client,))
        if len(cur.fetchall()) == 0:
            print('This client does not exist on the system')
            return
        
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phones (number, client)
        VALUES (%s, %s) RETURNING id;
        """, (number, client))
    print(f'ID created client number: ', cur.fetchone())

#Function to change client information

def change_client(client_id, first_name=None, last_name=None, email=None, phones=None):
 
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id
            FROM client
            WHERE id = &s;
            """, (client_id,))
        if len(cur.fetchall()) == 0:
            print('Client with this id not exists')
            return
        
    atributes_client = {'name': first_name, 'surname': last_name, 'email': email}
    for key, value in atributes_client.items():
        if value:
            with conn.cursor() as cur:
                cur.execute(SQL('UPDATE clients SET {} = $s WHERE id = $s').format(Identifier(key)), (value, client_id))
                conn.commit()

            with conn.cursor() as cur:
                  cur.execute("""
                    SELECT id
                    FROM client
                    WHERE id = &s;
                     """, (client_id,))
            print('Updated client:', cur.fetchone())
            return
                
#Function to delete a phone number

def delete_phone(client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT number
            FROM phones
            WHERE number = %s and client = %s;
            """, (number, client_id))
        if len(cur.fetchall()) == 0:
            print('This account doesnt exist on the system')
            return
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone 
                WHERE =%s and client = %s;
        """, (client_id, number))
        conn.commit()
        print(f'Phone {number} from client {client_id} has been deleted')

#Function to delete a cleint

def delete_client(client_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id
            FROM clients
            WHERE id = %s;
            """, (client_id))
        if len(cur.fetchall()) == 0:
            print(f'Client with this id does not exist')
            return
    
    with conn.cursor() as cur:
        cur.execute("""
             DELETE FROM client
                WHERE =%s;
        """, (client_id,))
        conn.commit()
        print(f'Client {client_id} and his numbers are deleted')

#Function to find client with his information (name, surname, email or phone)

def find_client(first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.*, t.number
            FROM client c
            FULL OUTER JOIN phones t ON c.id = t.client
            WHERE (fira_name = %(first_name)s or %(first_name)s is NULL)
                    and (last_name = %(last_name)s or %(last_name)s is NULL)
                    and (number = %(number)s or %(number)s is NULL)
                    and (email = %(email)s or %(email)s is NULL);
""", {'first_name': first_name, 'last_name': last_name, 'email': email, 'number': number})
    print(f'Client founded:', cur.fetchall())

    conn.close()


if __name__ == '__main__':

    with psycopg2.connect(database="clients_db", user="postgres", password="alinka293001") as conn:

        create_db(conn)

add_client('Ivan', 'Ivanov', 'iivanov@ya.ru')

add_client('Petr', 'Petrov', 'ppetrov@ya.ru')

add_client('Nikolay', 'Petrov', 'npetrov@ya.ru')

add_phone('777', 1)

add_phone('888', 1)

add_phone('999', 2)

change_client(2, name='Степан', surname=None, email='spetrov@ya.ru')

delete_phone(1, 777)

delete_client(1)

find_client(None,'Petrov', None, None)