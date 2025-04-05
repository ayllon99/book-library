import psycopg2
import pandas as pd
from variables import config
import bcrypt


class DatabaseConnect:
    def __init__(self) -> None:
        # Variables to access to data
        self.postgres_database = config['postgres_database']
        self.postgres_host = config['postgres_host']
        self.postgres_user = config['postgres_user']
        self.postgres_pass = config['postgres_pass']
        self.conn = None
        self.cur = None
    
    def connect(self) -> None:
        """
        Create the connection to the PostgreSQL database.

        """
        self.conn = psycopg2.connect(
            dbname=self.postgres_database,
            host=self.postgres_host,
            user=self.postgres_user,
            password=self.postgres_pass
        )
        self.cur = self.conn.cursor()

    def close_connection(self) -> None:
        """
        Closes the connection to the PostgreSQL database.

        Closes the cursor and connection objects to free up system resources.
        """
        self.cur.close()
        self.conn.close()

    def _get_pass(self, username: str) -> str:
        try:
            sql = "SELECT pass_hash FROM library.admins WHERE username = %s"
            self.cur.execute(sql, (username,))
            user = pd.DataFrame(self.cur.fetchone())
            user_pass = user[0][0]

        except Exception as e:
            print('Error getting pass from database ', e)
            user_pass = None

        return user_pass
    
    def authenticate(self, username: str, password: str) -> bool:
        user_pass = self._get_pass(username)
        authenticated = user_pass and bcrypt.checkpw(password.encode("utf-8"),
                                                     user_pass.encode("utf-8"))
        return authenticated
    
    def add_new_book(self, new_book: dict) -> None:
        self.cur.execute("""
            INSERT INTO library.books (isbn, title, publication_year, genre, lang, available)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                new_book["isbn"],
                new_book["title"],
                new_book["publication_year"],
                new_book["genre"],
                new_book["language"],
                new_book["available"]
            ))
        self.conn.commit()





