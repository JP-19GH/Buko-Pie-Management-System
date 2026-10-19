# Main file for the Buko Pie Inventory Management System.
# Run this file to use the entire program.

from database import conn
from inventory import (
    add_product,
    view_inventory,
    update_product,
    delete_product,
    search_product,
    reset_system
)
from orders import create_order
from reports import (
    sales_report,
    generate_summary_report,
    export_report_csv
)


def main_menu():
    """Display the menu and run the feature selected by the user."""

    while True:
        print("========================================")
        print(" BUKO PIE INVENTORY MANAGEMENT SYSTEM ")
        print("========================================")
        print("[1] Add Material")
        print("[2] View Inventory")
        print("[3] Update Material")
        print("[4] Delete Material")
        print("[5] Search Material")
        print("[6] Create Order")
        print("[7] Sales Report")
        print("[8] Summary Report")
        print("[9] Export CSV Report")
        print("[10] Reset System")
        print("[11] Exit")
        print("========================================")

        choice = input("Enter your choice: ").strip()

        # Run the feature that matches the user's menu selection.
        if choice == "1":
            add_product()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            search_product()
        elif choice == "6":
            create_order()
        elif choice == "7":
            sales_report()
        elif choice == "8":
            generate_summary_report()
        elif choice == "9":
            export_report_csv()
        elif choice == "10":
            reset_system()
        elif choice == "11":
            print("System closed.")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__": # Start the menu only when this file is run directly.
    try:
        main_menu()
    finally:
        conn.close() # Close the database connection when the user exits or an error occurs.
