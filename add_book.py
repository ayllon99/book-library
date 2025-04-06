from taipy.gui import Markdown, Gui, State
import pandas as pd
import os
from database import DatabaseConnect
import psycopg2
from datetime import datetime
# from gui import *    

############################################3
# Filter criteria
isbn_filter = ""
title_filter = ""
author_filter = ""
genre_filter = ""
filtered_df = pd.DataFrame()

FILTER_BOOKS = """
<|container|
# DELETE Book

**Filter Criteria**
<|layout|columns=1 1 1|
<|
ISBN: <|{isbn_filter}|input|>  
|>
<|
Title: <|{title_filter}|input|>  
|>
<|
Author: <|{author_filter}|input|>  
|>
<|
Genre: <|{genre_filter}|input|>  
|>
<|
Quantity: <|{quantity_filter}|input|>  
|>
|>
<|Filter|button|on_action=filter_books|>
|>
"""

FILTERED_DF = """
**Last books registrated**  
<|{filtered_df}|table|page_size=10|>
"""

############################################
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

new_author = {
    "first_name": None,
    "last_name": None,
    "birth_date": None,
    "nationality": None
}
author_status = ""

new_publisher = {
    "publisher_name": None,
    "publisher_address": None,
    "publisher_phone": None,
    "publisher_website": None
}
publisher_status =""

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

ADD_BOOK = """
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
Author: <|{new_book.author}|selector|lov={AUTHOR_OPTIONS}|dropdown|class_name=dropdown-half|>  
|>
<|
Publisher: <|{new_book.publisher}|selector|lov={PUBLISHER_OPTIONS}|dropdown|class_name=dropdown-half|>  
|>
<|
<|layout|columns=1 3|class_name=align-center|

<|container-toggle|
Available: <|{new_book.available}|toggle|width=100%|class_name=vertical-center|>  
|>
<|Refresh|button|on_action=refresh_book|class_name=vertical-center|>
|>

|>
|>

<|Add Book|button|on_action=add_book_to_db|>  
<|{add_status}|text|class_name=status|>  
|>
"""

ADD_AUTHOR = """
<|part|render={selected_author == "ADD"}|
<|container|
##### Add author
<|
First name: <|{new_author.first_name}|input|width=100%|class_name=input-field|>
|>
<|
Last name: <|{new_author.last_name}|input|width=100%|class_name=input-field|>
|>
<|
Birth date: <|{new_author.birth_date}|date|width=100%|class_name=input-field|>
|>
<|
Nacionality: <|{new_author.nationality}|input|width=100%|class_name=input-field|>
|>
<|layout|columns=3 1|
<|
<|Add author|button|on_action=add_author|>
|>
<|
<|Refresh|button|on_action=refresh_author|>
|>
|>
<|{author_status}|text|class_name=status|>  
|>
|>
"""

UPDATE_AUTHOR = """
<|part|render={selected_author == "UPDATE"}|
<|container|
##### UPDATE author
<|
First name: <|{new_author.first_name}|input|width=100%|class_name=input-field|>
|>
<|
Last name: <|{new_author.last_name}|input|width=100%|class_name=input-field|>
|>
<|
Birth date: <|{new_author.birth_date}|date|width=100%|class_name=input-field|>
|>
<|
Nacionality: <|{new_author.nationality}|input|width=100%|class_name=input-field|>
|>
<|layout|columns=3 1|
<|
<|Add author|button|on_action=add_author|>
|>
<|
<|Refresh|button|on_action=refresh_author|>
|>
|>
<|{author_status}|text|class_name=status|>  
|>
|>
"""

ADD_PUBLISHER = """
<|container|
##### Add publisher
<|
Publisher's name: <|{new_publisher.publisher_name}|input|width=100%|class_name=input-field|>
|>
<|
Address: <|{new_publisher.publisher_address}|input|width=100%|class_name=input-field|>
|>
<|
Phone: <|{new_publisher.publisher_phone}|input|width=100%|class_name=input-field|>
|>
<|
Website: <|{new_publisher.publisher_website}|input|width=100%|class_name=input-field|>
|>
<|layout|columns=3 1|
<|
<|Add publisher|button|on_action=add_publisher|>
|>
<|
<|Refresh|button|on_action=refresh_publisher|>
|>
|>
<|{publisher_status}|text|class_name=status|>  
|>
"""

selected_author = "ADD"
TOGGLE_AUTHOR = """
<|{selected_author}|toggle|lov=ADD;UPDATE;REMOVE|>

"""

AUTHOR_SELECTION = """

"""

ADD_BOOK_PAGE = F"""
<|layout|columns=1 1|
<|container|
{ADD_BOOK}
<|container|
<|layout|columns=1 1|
<|
<|layout|columns=1 1 1|
<| |>
{TOGGLE_AUTHOR}
<| |>
|>
<|{ADD_AUTHOR}|>
<|{UPDATE_AUTHOR}|>
|>
<|{ADD_PUBLISHER}|>
|>
|>
|>

<|container|
{FILTERED_DF}
{FILTER_BOOKS}
|>
|>

"""

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

    h5 {
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

    .align-center {
        display: flex;
        align-items: center;
    }

    .vertical-center {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
    }

    /* Responsive adjustments */
    @media (max-width: 640px) {
        .container {
            margin: 1rem;
            padding: 1rem;
        }
    }

"""

def add_author(state: State) -> None:
    new_author = state.new_author.__dict__['_dict']
    print(new_author)
    try:
        connection = DatabaseConnect()
        connection.connect()
        connection.add_new_author(new_author)
        connection.close_connection()

        state.author_status = "✅ Author added successfully!"

        state.new_author['first_name'] = None
        state.new_author['last_name'] = None
        state.new_author['birth_date'] = None
        state.new_author['nationality'] = None
        refresh_authors_options(state)
    except Exception as e:
        state.author_status = f"❌ Error: {str(e)}"

def add_publisher(state: State) -> None:
    new_publisher = state.new_publisher.__dict__['_dict']
    print(new_publisher)
    try:
        connection = DatabaseConnect()
        connection.connect()
        connection.add_new_publisher(new_publisher)
        connection.close_connection()

        state.publisher_status = "✅ Publisher added successfully!"

        state.new_publisher['publisher_name'] = None
        state.new_publisher['publisher_address'] = None
        state.new_publisher['publisher_phone'] = None
        state.new_publisher['publisher_website'] = None
        refresh_publishers_options(state)
    except Exception as e:
        state.publisher_status = f"❌ Error: {str(e)}"

def add_book_to_db(state: State):
    # print('inside add')
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
    finally:
        get_books(state)

def refresh_publisher(state: State):
    # print('refresh publisher')
    state.publisher_status = None
    
    state.new_publisher["name"] = None
    state.new_publisher["address"] = None
    state.new_publisher["phone"] = None
    state.new_publisher["website"] = None

def refresh_author(state: State):
    # print('refresh author')
    state.author_status = None
    
    state.new_author["first_name"] = None
    state.new_author["last_name"] = None
    state.new_author["birth_date"] = None
    state.new_author["nationality"] = None

def refresh_book(state: State):
    print('refresh book')
    print(state.new_book["publication_year"])
    refresh_publishers_options(state)
    refresh_authors_options(state)
    state.add_status = None
    
    state.new_book["isbn"] = None
    state.new_book["title"] = None
    state.new_book["description"] =None
    state.new_book["edition"] =None
    state.new_book["publication_year"] = datetime.today().year
    state.new_book["genre"] = None
    state.new_book["language"] = "English"
    state.new_book["author"] = None
    state.new_book["publisher"] = None
    state.new_book["available"] = True

def refresh_publishers_options(state: State):
    connection = DatabaseConnect()
    connection.connect()
    state.PUBLISHER_OPTIONS = connection.get_publishers()
    connection.close_connection()

def refresh_authors_options(state: State):
    connection = DatabaseConnect()
    connection.connect()
    state.AUTHOR_OPTIONS = connection.get_authors()
    connection.close_connection()

def get_books(state):
    connection = DatabaseConnect()
    connection.connect()
    df = connection.get_all_books()
    connection.close_connection()
    state.filtered_df = df

def on_init(state):
    print('on_init')
    refresh_authors_options(state)
    refresh_publishers_options(state)
    get_books(state)

if __name__ == "__main__":
    gui = Gui()
    gui.add_page("add_book", page=ADD_BOOK_PAGE, style=ADD_BOOK_STYLE)
    gui.run(title="Library Admin", port=5000, watermark='', flask_secret_key=SECRET_KEY)
