from taipy.gui import Gui, State, navigate
import database
import os
from variables import config


SECRET_KEY = os.urandom(24).hex()
unprotected_pages = config['unprotected_pages']
print(unprotected_pages)
# -------------------------------------
# Login Page
# -------------------------------------
username=""
password=""
login_error = ""
logged_in_user = ""

def on_login(state: State) -> State:
    """
    Check username and password in the database for user authentication.

    """

    username = str(state.username).strip() 
    password = str(state.password).strip()
    connection = database.DatabaseConnect()
    connection.connect()
    authenticated = connection.authenticate(username, password)
    connection.close_connection()

    if authenticated:
        state.logged_in_user = state.username
        state.username = ""
        state.password = ""
        state.login_error = ""
        return navigate(state, "private")
    else:
        state.login_error = "Invalid username or password."
        return state


def on_logout(state: State):
    state.logged_in_user = ""
    navigate(state, "login")


def on_navigate(state: State, page_name: str) -> str:
    # For the protected page, check if user is logged in
    print('page_name: ', page_name)
    if page_name in unprotected_pages or state.logged_in_user:
        print('here we go')
        return page_name
    else:
        print('else')
        return "login"


LOGIN_PAGE = """
<|layout|columns=1|class_name=container|
<|navbar|>
<|card|
### Library Admin Login
<|{username}|input|label=Username|on_action=on_login|>  
<|{password}|input|label=Password|password|on_action=on_login|>
<|layout|class_name=button-container|
<|Login|button|on_action=on_login|>
|>
<|{login_error}|text|class=error|>
|>
|>
"""
LOGIN_STYLE = """
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
        margin-top: 1rem; /* Add spacing above the button */
    }

"""


# -------------------------------------
# Run the App with Auth Check
# -------------------------------------

if __name__ == "__main__":
    gui = Gui()
    gui.add_page("login", LOGIN_PAGE, style=LOGIN_STYLE)
    gui.add_page("private", "# Private page")
    gui.run(title="Library Admin", port=5000, watermark='', flask_secret_key=SECRET_KEY)