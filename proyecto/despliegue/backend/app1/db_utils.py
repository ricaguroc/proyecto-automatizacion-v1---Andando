import sqlite3
from .ipfs_utils import remove_from_ipfs

DB_PATH = "pages.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            html_cid TEXT NOT NULL,
            css_cid TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(email, html_cid, css_cid):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pages (email, html_cid, css_cid) VALUES (?, ?, ?)', (email, html_cid, css_cid))
    conn.commit()
    conn.close()

def delete_page(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT html_cid, css_cid FROM pages WHERE email = ?', (email,))
    row = cursor.fetchone()
    if row:
        remove_from_ipfs(row[0])
        remove_from_ipfs(row[1])
        cursor.execute('DELETE FROM pages WHERE email = ?', (email,))
        conn.commit()
    conn.close()

def get_page_by_id(page_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT html_cid, css_cid FROM pages WHERE id = ?', (page_id,))
    page = cursor.fetchone()
    conn.close()
    return page
