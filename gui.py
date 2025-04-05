import pandas as pd
from taipy.gui import Gui, Markdown
from networking import LOCAL_IP
from authentication import LOGIN_PAGE, LOGIN_STYLE
from authentication import *

# Load CSV data
df = pd.read_csv('books.csv').fillna('')  # Replace with your CSV path

# Initial filtered DataFrame
filtered_df = df.copy()

# Filter criteria
isbn_filter = ""
title_filter = ""
author_filter = ""
genre_filter = ""
quantity_filter = ""

def filter_books(state):
    global df
    temp_df = df.copy()
    
    # Apply filters
    if state.isbn_filter:
        temp_df = temp_df[temp_df['ISBN'].astype(str).str.contains(state.isbn_filter, case=False)]
    if state.title_filter:
        temp_df = temp_df[temp_df['Title'].str.contains(state.title_filter, case=False)]
    if state.author_filter:
        temp_df = temp_df[temp_df['Author'].str.contains(state.author_filter, case=False)]
    if state.genre_filter:
        temp_df = temp_df[temp_df['Genre'].str.contains(state.genre_filter, case=False)]
    if state.quantity_filter:
        temp_df = temp_df[temp_df['Quantity'].astype(str).str.contains(state.quantity_filter, case=False)]
    
    state.filtered_df = temp_df

# Create GUI layout
find_book_page = Markdown("""
<|container|
# PRIVATE Book Inventory Filter

**Filter Criteria**
  
ISBN: <|{isbn_filter}|input|>  
Title: <|{title_filter}|input|>  
Author: <|{author_filter}|input|>  
Genre: <|{genre_filter}|input|>  
Quantity: <|{quantity_filter}|input|>  

<|Filter|button|on_action=filter_books|>
<|Logout|button|on_action=on_logout|>

**Filtered Books**  
<|{filtered_df}|table|page_size=10|show_all|>
|>
""")

PUBLIC_PAGE = Markdown("""
<|layout|columns=1|
<|navbar|>
**Welcome to the PUBLIC Library Admin Dashboard**  
<|Manage Books|button|on_action=manage_books|>
|>
""")

print(f"\n=== Application running at: http://{LOCAL_IP}:80 ===")
print("Users on the same network can access this URL using the above address")

gui = Gui()
gui.add_page("login", LOGIN_PAGE, style=LOGIN_STYLE)
gui.add_page("public", PUBLIC_PAGE)
gui.add_page("private", find_book_page)
gui.run(
    host="0.0.0.0", 
    port=80,
    title="Shared Book Inventory",
    run_browser=True,
    single_client=False,
    watermark=""
)
