from database import conn, cursor

# Units used when displaying the available ingredients.
MATERIAL_UNITS = {
    "Buko": "kl",
    "AFP": "sack",
    "Dragon": "sack",
    "Milk": "can",
    "Sugar": "kl"
}


def add_product():
    """Add a new material to the inventory."""

    print("\n=== ADD MATERIAL ===")
    name = input("Enter material name (AFP, Dragon, Buko, Sugar, Milk): ").strip()

    if not name or name.isdigit():
        print("Invalid material name.\n")
        return

    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: ₱"))

        # Do not allow negative values.
        if quantity < 0 or price < 0:
            print("Quantity and price cannot be negative.\n")
            return
    except ValueError:
        print("Invalid input. Enter numbers only.\n")
        return

    # Check whether the material is already recorded.
    cursor.execute(
        "SELECT id FROM inventory WHERE LOWER(product_name)=LOWER(?)",
        (name,)
    )
    if cursor.fetchone():
        print("Material already exists in inventory!\n")
        return

    # Save the new material.
    cursor.execute("""
    INSERT INTO inventory (product_name, quantity, price)
    VALUES (?, ?, ?)
    """, (name, quantity, price))
    conn.commit()

    print("Material added successfully!\n")


def view_inventory():
    """Display all materials currently in inventory."""

    cursor.execute("SELECT * FROM inventory")
    products = cursor.fetchall()

    print("\n========== INVENTORY RECORDS ==========")
    if not products:
        print("No materials available.\n")
        return

    print(f"{'ID':<5} {'MATERIAL':<20} {'QUANTITY':<15} {'PRICE'}")

    for product in products:
        unit = MATERIAL_UNITS.get(product[1], "")
        quantity_text = f"{product[2]} {unit}".strip()

        print(
            f"{product[0]:<5} "
            f"{product[1]:<20} "
            f"{quantity_text:<15} "
            f"₱{product[3]:.2f}"
        )
    print()


def update_product():
    """Change the quantity and price of an existing material."""

    view_inventory()

    try:
        product_id = int(input("Enter material ID to update: "))
        new_quantity = int(input("Enter new quantity: "))
        new_price = float(input("Enter new price: "))

        if new_quantity < 0 or new_price < 0:
            print("Quantity and price cannot be negative.\n")
            return
    except ValueError:
        print("Invalid input. Enter numbers only.\n")
        return

    cursor.execute("SELECT id FROM inventory WHERE id=?", (product_id,))
    if cursor.fetchone():
        cursor.execute("""
        UPDATE inventory
        SET quantity=?, price=?
        WHERE id=?
        """, (new_quantity, new_price, product_id))
        conn.commit()
        print("Material updated successfully!\n")
    else:
        print("Material ID not found.\n")


def delete_product():
    """Delete a material from inventory."""

    view_inventory()

    try:
        product_id = int(input("Enter material ID to delete: "))
    except ValueError:
        print("Invalid input. Enter a number.\n")
        return

    cursor.execute("SELECT id FROM inventory WHERE id=?", (product_id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM inventory WHERE id=?", (product_id,))
        conn.commit()
        print("Material deleted successfully!\n")
    else:
        print("Material ID not found.\n")


def search_product():
    """Find materials by entering all or part of a material name."""

    keyword = input("\nEnter material name to search: ").strip()
    if not keyword or keyword.isdigit():
        print("Invalid input.\n")
        return

    cursor.execute("""
    SELECT * FROM inventory
    WHERE product_name LIKE ?
    """, (f"%{keyword}%",))
    results = cursor.fetchall()

    print("\n========== SEARCH RESULTS ==========")
    if results:
        print(f"{'ID':<5} {'MATERIAL':<20} {'QUANTITY':<15} {'PRICE'}")
        for row in results:
            unit = MATERIAL_UNITS.get(row[1], "")
            quantity_text = f"{row[2]} {unit}".strip()
            print(
                f"{row[0]:<5} {row[1]:<20} "
                f"{quantity_text:<15} ₱{row[3]:.2f}"
            )
    else:
        print("No material found.")
    print()


def reset_system():
    """Delete all inventory and order records after confirmation."""

    confirm = input(
        "Are you sure you want to reset the whole system? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        cursor.execute("DELETE FROM inventory")
        cursor.execute("DELETE FROM orders")
        conn.commit()
        print("\nSystem reset successfully!")
        print("Inventory and order records were cleared.\n")
    else:
        print("Reset cancelled.\n")
