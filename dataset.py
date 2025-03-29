import sqlite3

def setup_database():
    """
    Creates the SQLite database and the 'users' table if they don't exist.
    """
    try:
        conn = sqlite3.connect("dataset.sql")
        cursor = conn.cursor()
        # Create a table to store user credentials if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        print("Database setup completed successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred during database setup: {e}")
    finally:
        if conn:
            conn.close()

def validate_login(username, password):
    """
    Validates the login credentials against the database.

    Args:
        username (str): The username entered by the user.
        password (str): The password entered by the user.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    try:
        conn = sqlite3.connect("dataset.sql")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        if result:
            print(f"Login successful for user: {username}")
        else:
            print(f"Invalid credentials for user: {username}")
        return result is not None
    except sqlite3.Error as e:
        print(f"An error occurred during login validation: {e}")
        return False
    finally:
        if conn:
            conn.close()

def create_user(username, password):
    """
    Creates a new user in the database.

    Args:
        username (str): The username entered by the user.
        password (str): The password entered by the user.

    Returns:
        bool: True if the user was created successfully, False if the username already exists.
    """
    try:
        conn = sqlite3.connect("dataset.sql")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"User '{username}' created successfully.")
        return True
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists.")
        return False  # Username already exists
    except sqlite3.Error as e:
        print(f"An error occurred while creating user: {e}")
        return False
    finally:
        if conn:
            conn.close()

def save_to_dataset(username, password):
    """
    Saves the user details to a text file (dataset.txt).

    Args:
        username (str): The username entered by the user.
        password (str): The password entered by the user.
    """
    try:
        with open("dataset.txt", "a") as file:
            file.write(f"Username: {username}, Password: {password}\n")
        print(f"User '{username}' saved to dataset.txt.")
    except IOError as e:
        print(f"An error occurred while saving to dataset.txt: {e}")

# Example usage
if __name__ == "__main__":
    setup_database()
    create_user("user1", "password1")
    print(validate_login("user1", "password1"))  # Should print True
    save_to_dataset("user1", "password1")