import pandas as pd
import taipy as tp
from taipy.gui import Gui, Markdown
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip



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
page = Markdown("""
<|container|
# Book Inventory Filter

**Filter Criteria**
  
ISBN: <|{isbn_filter}|input|>  
Title: <|{title_filter}|input|>  
Author: <|{author_filter}|input|>  
Genre: <|{genre_filter}|input|>  
Quantity: <|{quantity_filter}|input|>  

<|Filter|button|on_action=filter_books|>

**Filtered Books**  
<|{filtered_df}|table|page_size=10|show_all|>
|>
""")

local_ip = get_local_ip()
print(f"\n=== Application running at: http://{local_ip}:80 ===")
print("Users on the same network can access this URL using the above address")

gui = Gui()
gui.add_page("main", page)
gui.run(
    host="0.0.0.0", 
    port=80,
    title="Shared Book Inventory",
    run_browser=False,  # Prevent automatic browser opening
    single_client=False
)
