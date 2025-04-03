import bcrypt
from taipy.gui import Gui, Markdown, State
import pandas as pd
import testing_db
# Initialize Taipy GUI
gui = Gui()

# -------------------------------------
# Login Page
# -------------------------------------
username=""
password=""
authenticated = ""
login_error = ""


def on_login(state: State) -> State:
    username = str(state.username).strip() 
    password = str(state.password).strip()
    conn = testing_db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pass_hash FROM library.admins WHERE username = %s", (username,))
    user = pd.DataFrame(cursor.fetchone())
    # print('user:', user)
    
    conn.close()
    
    if len(user) > 0 and bcrypt.checkpw(password.encode("utf-8"), user[0][0].encode("utf-8")):
        state.authenticated = True  # Store auth status in Taipy state
        state.login_error = ""
        print('LOGGED IN')
        return state
    else:
        state.login_error = "Invalid username or password."
        print('logging error')
        return state
    
login_page = """
    <|layout|columns=1|class_name=container|
    <|card|
    ### Library Admin Login
    <|{username}|input|label=Username|>  
    <|{password}|input|label=Password|password|>
    <|layout|class_name=button-container|
    <|Login|button|on_action=on_login|>
    |>
    <|{login_error}|text|class=error|>
    |>
    |>
"""
style = """
    .container {
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    card {
        padding: 2rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 350px;
    }

    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 1rem; /* Optional: Add spacing above the button */
    }

"""


# -------------------------------------
# Run the App with Auth Check
# -------------------------------------

if __name__ == "__main__":
    gui.add_page("login", login_page, style=style)
    gui.run(title="Library Admin", port=5000, watermark='')
