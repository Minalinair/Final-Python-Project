import sqlite3
import os

db_name = "shopping_system.db"

def init_db():
    # Initializes the database and creates the required related tables.
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Enable foreign key support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Users Table (Authentication and Role Authorization)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Admin', 'Customer'))
        )
    ''')
    
    # 2. Products Table (Inventory managed by Admins)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price REAL NOT NULL CHECK(price >= 0),
            stock INTEGER NOT NULL CHECK(stock >= 0)
        )
    ''')
    
    # 3. Orders Table (Transactions linking Users and Products via Foreign Keys)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
        )
    ''')
    
    # Default administrator account if it doesn't exist
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       ('admin', 'admin123', 'Admin'))
    except sqlite3.IntegrityError:
        pass  # Admin already exists
        
    conn.commit()
    conn.close()

def get_non_empty_input(prompt):
    # Ensures input strings are not empty or purely whitespace.
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Error: Input cannot be empty.")

def get_positive_float(prompt):
    # Ensures input numeric values are positive decimal points.
    while True:
        try:
            val = float(get_non_empty_input(prompt))
            if val >= 0:
                return val
            print("Error: Value must be 0 or higher.")
        except ValueError:
            print("Error: Please enter a valid decimal number.")

def get_positive_int(prompt):
# Ensures input numeric values are positive integers.
    while True:
        try:
            val = int(get_non_empty_input(prompt))
            if val > 0:
                return val
            print("Error: Value must be greater than 0.")
        except ValueError:
            print("Error: Please enter a valid whole number.")


# where the user has to register as admin or user
def register_user():
    print("\n--- User Registration ---")
    username = get_non_empty_input("Enter new username: ")
    password = get_non_empty_input("Enter password: ")
    
    print("Select Role:\n1. Customer\n2. Admin")
    choice = input("Enter choice (1-2): ").strip()
    role = "Admin" if choice == '2' else "Customer"
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, password, role))
        conn.commit()
        print(f"🎉 Account successfully created as [{role}]!")
    except sqlite3.IntegrityError:
        print("❌ Error: Username already exists. Choose a different name.")
    finally:
        conn.close()
# login if user is registered
def login_user():
    print("\n--- User Login ---")
    username = get_non_empty_input("Username: ")
    password = get_non_empty_input("Password: ")
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, role FROM users WHERE username = ? AND password = ?", 
                   (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        print(f"\n✅ Welcome back, {user[1]}! Logged in as [{user[2]}].")
        return {"id": user[0], "username": user[1], "role": user[2]}
    else:
        print("❌ Invalid username or password.")
        return None


# operations performed only by the admin
def create_product():
    print("\n--- Add New Product ---")
    name = get_non_empty_input("Product Name: ")
    price = get_positive_float("Product Price ($): ")
    stock = get_positive_int("Initial Stock Quantity: ")
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", 
                       (name, price, stock))
        conn.commit()
        print("📦 Product added successfully!")
    except sqlite3.IntegrityError:
        print("❌ Error: A product with that name already exists.")
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()

def view_all_products():
    print("\n--- Available Inventory ---")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    
    if not products:
        print("No products available in the shop.")
        return False
        
    print(f"{'ID':<5} | {'Product Name':<20} | {'Price':<10} | {'Stock Remaining':<15}")
    print("-" * 60)
    for p in products:
        print(f"{p[0]:<5} | {p[1]:<20} | ${p[2]:<9.2f} | {p[3]:<15}")
    return True

def update_product():
    print("\n--- Update Existing Product ---")
    if not view_all_products():
        return
        
    product_id = get_positive_int("Enter the Product ID to update: ")
    new_price = get_positive_float("Enter new price ($): ")
    new_stock = get_positive_int("Enter new stock level: ")
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE products SET price = ?, stock = ? WHERE product_id = ?", 
                       (new_price, new_stock, product_id))
        if cursor.rowcount > 0:
            conn.commit()
            print("🔄 Product values updated successfully!")
        else:
            print("❌ Error: Product ID not found.")
    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")
    finally:
        conn.close()

def delete_product():
    print("\n--- Delete Product ---")
    if not view_all_products():
        return
        
    product_id = get_positive_int("Enter Product ID to remove permanently: ")
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print("🗑️ Product removed from catalogue successfully.")
        else:
            print("❌ Error: Product ID not found.")
    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")
    finally:
        conn.close()

# operations for the customers
def place_order(user_id):
    print("\n--- Place an Order ---")
    if not view_all_products():
        return
        
    product_id = get_positive_int("Enter the Product ID you wish to buy: ")
    quantity = get_positive_int("Quantity to purchase: ")
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        # Check stock verification safely
        cursor.execute("SELECT stock, name FROM products WHERE product_id = ?", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            print("❌ Error: Selected Product ID does not exist.")
            return
            
        current_stock, product_name = product[0], product[1]
        
        if current_stock < quantity:
            print(f"❌ Insufficient Stock! Only {current_stock} items of '{product_name}' left.")
            return
            
        # Complete Transaction Processing: Update Stock and Insert Order
        cursor.execute("UPDATE products SET stock = stock - ? WHERE product_id = ?", (quantity, product_id))
        cursor.execute("INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)", 
                       (user_id, product_id, quantity))
        conn.commit()
        print(f"🛒 Successfully bought {quantity} unit(s) of '{product_name}'!")
        
    except sqlite3.Error as e:
        print(f"❌ Transaction failed due to database runtime error: {e}")
    finally:
        conn.close()

def view_customer_orders(user_id):
    print("\n--- Your Order History ---")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.order_id, p.name, o.quantity, (o.quantity * p.price), o.order_date 
        FROM orders o 
        JOIN products p ON o.product_id = p.product_id 
        WHERE o.user_id = ?
    ''', (user_id,))
    orders = cursor.fetchall()
    conn.close()
    
    if not orders:
        print("You haven't placed any orders yet.")
        return
        
    print(f"{'Order ID':<10} | {'Product Name':<20} | {'Qty':<5} | {'Total Cost':<12} | {'Date/Time':<20}")
    print("-" * 75)
    for o in orders:
        print(f"{o[0]:<10} | {o[1]:<20} | {o[2]:<5} | ${o[3]:<11.2f} | {o[4]:<20}")


# a dashboard layout for customer and admin-separate
def admin_menu():
    while True:
        print("\n=== ADMINISTRATOR DASHBOARD ===")
        print("1. Add New Product (Create)")
        print("2. View All Products (Read)")
        print("3. Update Product Details (Update)")
        print("4. Delete Product (Delete)")
        print("5. Log Out")
        choice = input("Select operation (1-5): ").strip()
        if choice == '1': 
            create_product()
        elif choice == '2':
            view_all_products()
        elif choice == '3':
            update_product()
        elif choice == '4': 
            delete_product()
        elif choice == '5':
            print("Logging out of admin console...")
            break
        else:
            print("Invalid entry. Choose option 1-5.")
def customer_menu(user):
    while True:
        print(f"\n=== CUSTOMER STOREFRONT - Logged in as: {user['username']} ===")
        print("1. View Store Catalogue")
        print("2. Buy Product / Place Order")
        print("3. View My Order History")
        print("4. Log Out")
        choice = input("Select operation (1-4): ").strip()
        if choice == '1': 
            view_all_products()
        elif choice == '2': 
            place_order(user['id'])
        elif choice == '3': 
            view_customer_orders(user['id'])
        elif choice == '4':
            print("Logging out of store session...")
            break
        else:
            print("Invalid entry. Choose option 1-4.")
def main():
    init_db()
    while True:
        print("\n======================================")
        print("  ONLINE SHOPPING TERMINAL PORTAL  ")
        print("======================================")
        print("1. Register Account")
        print("2. Login")
        print("3. Shut Down System")
        choice = input("Choose action (1-3): ").strip()
        if choice == '1':
            register_user()
        elif choice == '2':
            user = login_user()
            if user:
                if user['role'] == 'Admin':
                    admin_menu()
                else:
                    customer_menu(user)
        elif choice == '3':
            print("\nShutting down system. Goodbye!")
            break
        else:
            print("Invalid selection. Try again.")
if __name__ == "__main__":
    main()