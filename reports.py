import csv
from database import cursor


def sales_report():
    """Display all saved order records."""

    cursor.execute("SELECT * FROM orders")
    reports = cursor.fetchall()

    print("\n========== SALES REPORT ==========")
    if not reports:
        print("No sales records found.\n")
        return

    print(
        f"{'ID':<5} {'CUSTOMER':<15} {'PRODUCT':<15} "
        f"{'QTY':<5} {'TOTAL/PROFIT':<15} {'STATUS':<12} {'DATE'}"
    )

    for report in reports:
        print(
            f"{report[0]:<5} {report[1]:<15} {report[2]:<15} "
            f"{report[3]:<5} ₱{report[4]:<14.2f} "
            f"{report[5]:<12} {report[6]}"
        )
    print()


def generate_summary_report():
    """Show totals for orders, recorded sales/profit, and pies sold."""

    print("\n========== SUMMARY REPORT ==========")

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    # The original program stores profit in the total_cost column.
    cursor.execute("SELECT SUM(total_cost) FROM orders")
    result = cursor.fetchone()[0]
    total_profit = result if result is not None else 0

    cursor.execute("SELECT SUM(quantity) FROM orders")
    result = cursor.fetchone()[0]
    total_quantity = result if result is not None else 0

    print(f"Total Orders         : {total_orders}")
    print(f"Total Recorded Profit: ₱{total_profit:.2f}")
    print(f"Total Buko Pie Sold  : {total_quantity}")

    # Display remaining quantities for all materials.
    print("\n====== INVENTORY STOCKS ======")
    cursor.execute("SELECT product_name, quantity FROM inventory")
    materials = cursor.fetchall()

    if materials:
        for material in materials:
            print(f"{material[0]} Remaining : {material[1]}")
    else:
        print("No materials available.")

    print("\n====================================\n")


def export_report_csv():
    """Export order records into a CSV file that can open in spreadsheet apps."""

    cursor.execute("SELECT * FROM orders")
    reports = cursor.fetchall()
    filename = "sales_report.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Column headings for the exported report.
        writer.writerow([
            "ID", "Customer Name", "Product Name", "Quantity",
            "Total Cost (stored as Profit)", "Order Status", "Order Date"
        ])
        writer.writerows(reports)

    print("\nSales report exported successfully!")
    print(f"File saved as: {filename}\n")
