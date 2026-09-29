
import sqlite3
from schemas import User, UserInDB

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def setup_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        full_name TEXT,
        email TEXT,
        disabled BOOLEAN,
        hashed_password TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            description TEXT NOT NULL
        );
        
    CREATE TABLE IF NOT EXISTS cart (
            product_id INTEGER UNIQUE NOT NULL REFERENCES products(id)
        );

    CREATE INDEX IF NOT EXISTS users_username_index ON users (username);

    """)
    
    conn.commit()
    conn.close()
    
setup_db()


def create_user(username, full_name, email,hashed_password):

    conn = get_db()
    c = conn.cursor()

    c.execute("INSERT INTO users (username, full_name, email, hashed_password) VALUES (?, ?, ?, ?)", (username, full_name, email, hashed_password))
    
    conn.commit()
    conn.close()
    
def get_user(username):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))

    user = c.fetchone()

    conn.close()

    return User(**user)

def get_users():
    conn = get_db()
    c = conn.cursor()
    users_raw_list= list(c.execute("SELECT * FROM users").fetchall())
    
    return [User(**user) for user in users_raw_list]    

def delete_user_by_id(id:int):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()  
    
def get_user_by_id(id:int):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE id = ?", (id,))

    user = c.fetchone()

    conn.close()

    return User(**user)
    
def get_user_with_password(username:str):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))

    user = c.fetchone()
    return UserInDB(**user)
    
    