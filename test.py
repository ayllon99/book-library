from taipy.gui import Markdown, Gui
import pandas as pd
import os
from database import DatabaseConnect
import psycopg2
from datetime import datetime

SECRET_KEY = os.urandom(24).hex()

# Initialize variables
new_book = {
    "isbn": None,
    "title": None,
    "description":None,
    "edition":None,
    "publication_year": datetime.today().year,
    "genre": None,
    "language": "English",
    "author": None,
    "publisher": None,
    "available": True
}
add_status = ""

GENRE_OPTIONS = [
    "Fiction", "Non-Fiction", 
    "Science Fiction", "Fantasy", 
    "Mystery", "Biography"
]

LANGUAGE_OPTIONS = [
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Chinese",
    "Japanese",
    "Russian"
]

AUTHOR_OPTIONS = []

PUBLISHER_OPTIONS = []

ADD_BOOK_STYLE = """
    /* Main container */
    .container {
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        background: #2c3e50;
        color: #ecf0f1;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Segoe UI', Arial, sans-serif;
    }

    /* Header */
    h1 {
        color: #ecf0f1;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }

    /* Form elements container */
    .card {
        background: #f9f9f9;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }

    /* Input fields */
    input, .number-input, .selector {
        width: 100%;
        padding: 10px;
        margin-bottom: 1rem;
        border: 1px solid #ddd;
        border-radius: 6px;
        font-size: 14px;
        transition: border 0.3s;
    }

    input:focus, .number-input:focus {
        border-color: #3498db;
        outline: none;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }

    /* Labels */
    label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: #2c3e50;
    }

    /* Dropdown selectors */
    selector {
        margin-bottom: 1rem;
    }

    /* Toggle switch */
    toggle {
        margin: 0.5rem 0 1.5rem;
        --active-color: #3498db;
        --inactive-color: #95a5a6;
    }

    /* Buttons */
    button {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 16px;
        font-weight: 500;
        transition: background 0.3s;
        width: 100%;
        margin-top: 0.5rem;
    }

    button:hover {
        background-color: #2980b9;
    }

    /* Status message */
    .status {
        margin-top: 1rem;
        padding: 10px;
        border-radius: 6px;
        text-align: center;
        font-weight: 500;
    }

    .status.success {
        background-color: #d4edda;
        color: #155724;
    }

    .status.error {
        background-color: #f8d7da;
        color: #721c24;
    }
    /* Center toggle container */
    .toggle-container {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    /* Adjust toggle alignment */
    .toggle-container toggle {
        margin: 0 auto; /* Center horizontally */
    }

    /* Responsive adjustments */
    @media (max-width: 640px) {
        .container {
            margin: 1rem;
            padding: 1rem;
        }
    }

"""

ADD_BOOK_PAGE = Markdown("""
<|container|
# PRIVATE Add New Book

<|layout|columns=2 1 1|class_name=input-row|
<|
Title: <|{new_book.title}|input|width=100%|class_name=input-field-title|>
|>
<|
ISBN: <|{new_book.isbn}|input|width=100%|class_name=input-field|>
|>
<|
Year: <|{new_book.publication_year}|number|width=100%|min=1900|max={datetime.date.today().year}|class_name=input-field|>
|>
|>
<|
Description: <|{new_book.description}|input|width=100%|class_name=input-field|>
|>
<|layout|columns=1 1 1|class_name=dropdown-container|
<|
Edition: <|{new_book.edition}|input|width=100%|class_name=dropdown-half|>
|>
<|
Genre: <|{new_book.genre}|selector|lov={GENRE_OPTIONS}|multiple|dropdown|class_name=dropdown-half|>
|>
<|
Language: <|{new_book.language}|selector|lov={LANGUAGE_OPTIONS}|dropdown|class_name=dropdown-half|>
|>
|>
<|layout|columns=1 1 1|class_name=dropdown-container|
<|
Author: <|{new_book.author}|selector|lov={AUTHOR_OPTIONS}|multiple|dropdown|class_name=dropdown-half|>  
|>
<|
Publisher: <|{new_book.publisher}|selector|lov={PUBLISHER_OPTIONS}|multiple|dropdown|class_name=dropdown-half|>  
|>
<|toggle-container|
Available: <|{new_book.available}|toggle|>  
|>
|>
<|Add Book|button|on_action=add_book_to_db|>  
<|{add_status}|text|class_name=status|>  
|>
""")


def add_book_to_db(state):
    print('inside add')
    new_book = state.new_book.__dict__['_dict']
    
    try:
        connection = DatabaseConnect()
        connection.connect()
        connection.add_new_book(new_book)
        connection.close_connection()
        state.add_status = "✅ Book added successfully!"
        
        # Reset form
        state.new_book['title'] = None
        state.new_book['isbn'] = None
        state.new_book['description'] = None

    except Exception as e:
        state.add_status = f"❌ Error: {str(e)}"

if __name__ == "__main__":
    gui = Gui()
    gui.add_page("add_book", page=ADD_BOOK_PAGE, style=ADD_BOOK_STYLE)
    gui.run(title="Library Admin", port=5000, watermark='', flask_secret_key=SECRET_KEY)


