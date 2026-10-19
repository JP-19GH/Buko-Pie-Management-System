from datetime import datetime
from database import conn, cursor
from inventory import MATERIAL_UNITS

# Amount of each material used for one Buko Pie.
# These values preserve the recipe calculation from the original program.
REQUIRED_MATERIALS = {
    "Buko": 1 / 15,
    "AFP": 1 / 15,
    "Sugar": 1 / 15,
    "Milk": 1 / 15,
    "Dragon": 1 / 15
}

SELLING_PRICE = 250


def create_order():
    """Check ingredient stocks, calculate the order, and save the sale."""

    print("\n=== CREATE ORDER ===")
    customer_name = input("Enter customer name: ").strip()

    if not customer_name:
        print("Customer name cannot be empty.\n")
        return

    try:
        quantity = int(input("Enter quantity: "))
        if quantity <= 0:
            print("Quantity must be greater than zero.\n")
            return
    except ValueError:
        print("Invalid quantity. Enter a whole number.\n")
        return

    # Check whether all required materials exist and have enough stock.
    missing_materials = []
    insufficient_materials = []

    for material, amount_per_pie in REQUIRED_MATERIALS.items():
        cursor.execute(
            "SELECT quantity FROM inventory WHERE product_name=?",
            (material,)
        )
        result = cursor.fetchone()

        if result is None:
            missing_materials.append(material)
            continue

        stock = result[0]
        needed = round(amount_per_pie * quantity, 2)

        if stock < needed:
            unit = MATERIAL_UNITS.get(material, "")
            insufficient_materials.append(
                f"{material} (Needed: {needed} {unit}, "
                f"Available: {stock} {unit})"
            )

    # Stop the order if a required material is missing.
    if missing_materials:
        print("\nThe following materials are missing in inventory:")
        for item in missing_materials:
            print("-", item)
        print()
        return

    # Stop the order if there is not enough stock.
    if insufficient_materials:
        print("\nInsufficient material stocks:")
        for item in insufficient_materials:
            print("-", item)
        print()
        return

    # Calculate the cost of materials used for this order.
    material_cost = 0
    for material, amount_per_pie in REQUIRED_MATERIALS.items():
        cursor.execute(
            "SELECT price FROM inventory WHERE product_name=?",
            (material,)
        )
        material_price = cursor.fetchone()[0]
        amount_needed = round(amount_per_pie * quantity, 2)
        material_cost += material_price * amount_needed

    # Deduct used materials from inventory.
    for material, amount_per_pie in REQUIRED_MATERIALS.items():
        amount_needed = round(amount_per_pie * quantity, 2)
        cursor.execute("""
        UPDATE inventory
        SET quantity = quantity - ?
        WHERE product_name=?
        """, (amount_needed, material))

    # Calculate revenue and profit.
    product_name = "Buko Pie"
    total_revenue = SELLING_PRICE * quantity
    profit = total_revenue - material_cost
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save the completed order. The total_cost field stores profit,
    # matching the calculation used in the original program.
    cursor.execute("""
    INSERT INTO orders
    (customer_name, product_name, quantity, total_cost, order_status, order_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        customer_name,
        product_name,
        quantity,
        profit,
        "Completed",
        order_date
    ))

    conn.commit()

    # Print a receipt for the customer/order record.
    print("\n========== RECEIPT ==========")
    print(f"Customer Name : {customer_name}")
    print(f"Product Name  : {product_name}")
    print(f"Quantity      : {quantity}")
    print(f"Selling Price : ₱{SELLING_PRICE:.2f}")
    print(f"Revenue       : ₱{total_revenue:.2f}")
    print(f"Material Cost : ₱{material_cost:.2f}")
    print(f"Profit        : ₱{profit:.2f}")
    print("Status        : Completed")
    print("==============================\n")
