import sqlite3

# Connect to the SQLite database.
# The database file is created automatically if it does not exist.
conn = sqlite3.connect("buko_pie_system.db")
cursor = conn.cursor()


def create_tables():
    """Create the inventory and orders tables if they do not exist."""

    # Stores the available ingredients/materials.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
    """)

    # Stores each completed Buko Pie order.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total_cost REAL NOT NULL,
        order_status TEXT NOT NULL,
        order_date TEXT NOT NULL
    )
    """)

    conn.commit()


# Create the required tables when this module is imported.
create_tables()
