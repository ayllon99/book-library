from dotenv import load_dotenv
import os


load_dotenv()

config = {
    'postgres_host': os.getenv('DB_HOST'),
    'postgres_database': os.getenv('DB_NAME'),
    'postgres_user': os.getenv('DB_USER'),
    'postgres_pass': os.getenv('DB_PASSWORD'),
    'unprotected_pages': [a.strip() for a in 
                          os.getenv('UNPROTECTED_PAGES').split(',')]
}
