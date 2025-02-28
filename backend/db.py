import mysql.connector
from mysql.connector import Error

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="chatbot_user",
            password="password",  # Replace with your actual password
            database="chatbot_db"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_chat_history_table():
    """Create a table to store chat history."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),  -- Use session ID or actual user ID
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()

def save_chat_message(user_id, message, response):
    """Store user message and chatbot response in chat history."""
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO chat_history (user_id, message, response) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, message, response))
    connection.commit()
    cursor.close()
    connection.close()


def get_chat_history(user_id, limit=5):
    """Retrieve the last `limit` messages for a given user."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT message, response FROM chat_history WHERE user_id = %s ORDER BY timestamp DESC LIMIT %s"
    cursor.execute(query, (user_id, limit))
    history = cursor.fetchall()
    cursor.close()
    connection.close()
    return history

# Function to fetch all suppliers
def fetch_suppliers():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM suppliers;")
        suppliers = cursor.fetchall()
        cursor.close()
        connection.close()
        return suppliers
    return []

# Function to fetch all products
def fetch_products():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products;")
        products = cursor.fetchall()
        cursor.close()
        connection.close()
        return products
    return []

# Function to fetch products by brand
def fetch_products_by_brand(brand):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE brand = %s;", (brand,))
        products = cursor.fetchall()
        cursor.close()
        connection.close()
        return products
    return []

# Function to fetch suppliers by product category
def fetch_suppliers_by_category(category: str):
    """Fetch suppliers providing products in a given category."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM suppliers WHERE product_categories LIKE %s"
    cursor.execute(query, (f"%{category}%",))  # ✅ Use LIKE for partial matches

    suppliers = cursor.fetchall()
    connection.close()
    return suppliers


