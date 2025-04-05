import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import bcrypt

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def create_database(username, password, pass_2):
    with open('library-database.sql', 'r') as file:
        sql = file.read()


    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""DROP SCHEMA IF EXISTS library CASCADE;""")
    cursor.execute(sql)
    
    # raise an error if constraints are violated
    cursor.execute("""INSERT INTO library.admins (username, pass_hash, first_name, last_name, email, phone, address, registration_date)
    VALUES 
    (%s, %s, 'Alice', 'Smith', 'alice@example.com', '+15559876543', '456 Book St', '2023-01-15');""",
    (username, password.decode()))
    cursor.execute("SELECT * FROM library.admins")
    df = pd.DataFrame(cursor.fetchall())
    print('admin_df: \n',df)


    cursor.execute("""INSERT INTO library.authors (first_name, last_name, birth_date, nationality)
    VALUES 
        ('Jane', 'Austen', '1775-12-16', 'British'),
        ('Ernest', 'Hemingway', '1899-07-21', 'American'),
        ('Gabriel', 'García Márquez', '1927-03-06', 'Colombian');""")
    cursor.execute("SELECT * FROM library.authors")
    df = pd.DataFrame(cursor.fetchall())


    cursor.execute("""INSERT INTO library.members 
    (first_name, last_name, email, phone, address, registration_date)
    VALUES 
    ('Emily', 'Davis', 'emily.d@example.com', '+15551112222', '789 Pine Road', CURRENT_DATE),
    ('David', 'Wilson', 'david.w@example.com', '+15553334444', '321 Elm Street', CURRENT_DATE),
    ('Jennifer', 'Lee', 'jennifer.l@example.com', '+15556667777', '654 Maple Lane', CURRENT_DATE);""")
    cursor.execute("SELECT * FROM library.members")
    df = pd.DataFrame(cursor.fetchall())



    cursor.execute("""INSERT INTO library.publishers (name, address, phone, website)
    VALUES 
        ('Hachette Livre', '43 Quai de Grenelle, Paris', '+33143924000', 'https://www.hachette.com'),
        ('Macmillan Publishers', '120 Broadway, New York, NY', '+16467412000', 'https://us.macmillan.com'),
        ('Simon & Schuster', '1230 Avenue of the Americas, New York, NY', '+12126989000', 'https://www.simonandschuster.com');""")
    cursor.execute("SELECT * FROM library.publishers")
    df = pd.DataFrame(cursor.fetchall())


    cursor.execute("""INSERT INTO library.books (
        isbn, 
        title, 
        publication_year, 
        edition, 
        lang, 
        description, 
        genre,
        publisher_id,
        author_id,
        registration_date, 
        available
    )
    VALUES (
        9780743273565,
        'The Great Gatsby',
        1925,
        'First Scribner Paperback Edition',
        'English',
        'A story of wealth, love, and the American Dream in the 1920s',
        ARRAY['Fiction', 'Classic'],
        1,
        1,
        CURRENT_DATE,
        true
    );""")
    cursor.execute("SELECT * FROM library.books")
    df = pd.DataFrame(cursor.fetchall())



    cursor.execute("""INSERT INTO library.loans (
        book_id,
        member_id,
        authorized_by,
        checkout_date,
        due_date,
        return_date
    )
    VALUES (
        1,
        1,
        1,
        CURRENT_DATE,
        '2023-05-15',
        '2023-05-14'  -- Returned early
    );""")
    cursor.execute("SELECT * FROM library.loans")
    df = pd.DataFrame(cursor.fetchall())

    cursor.execute("""INSERT INTO library.admins (username, pass_hash, first_name, last_name, email, phone, address, registration_date) VALUES('root', %s, 'jose', 'ayllon', 'jose@example.com', '+159876543', '45 Book St', CURRENT_DATE);""",[pass_2.decode()])
    cursor.execute("SELECT * FROM library.admins")
    df = pd.DataFrame(cursor.fetchall())
    print(df)
    

    conn.commit()
    conn.close()

    return


def more_books():
    conn = get_db_connection()
    cursor = conn.cursor()

    df = pd.read_csv('books.csv')
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO library.books (isbn, title, registration_date) VALUES (%s, %s, CURRENT_TIMESTAMP)",
            (row['ISBN'], row['Title'])
        )

    conn.commit()
    conn.close()

hashed_pw = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt())
hash_2 = bcrypt.hashpw("root".encode("utf-8"), bcrypt.gensalt())
create_database('ayllon', hashed_pw, hash_2)
more_books()

if '__name__' == '__main__':
    print('yeeeess')
    hashed_pw = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt())
    hash_2 = bcrypt.hashpw("root".encode("utf-8"), bcrypt.gensalt())
    create_database('ayllon', hashed_pw, hash_2)




