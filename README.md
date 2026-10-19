DESCRIPTION
This is a Python-based Buko Pie Inventory Management System that uses an
SQLite database to manage ingredients/materials and record Buko Pie orders.
It helps the user monitor available stocks, update material information,
calculate order revenue and profit, review sales records, and export reports
to a CSV file.

FILES
- main.py: Main menu and program entry point.
- database.py: SQLite connection and table creation.
- inventory.py: Add, view, update, delete, search, and reset inventory.
- orders.py: Create orders, check material stocks, deduct materials, and
  calculate the receipt totals.
- reports.py: Sales report, summary report, and CSV export.
- buko_pie_system.db: Database file created automatically when run.

HOW TO RUN
1. Keep all Python files in the same folder.
2. Open a terminal or VS Code terminal in that folder.
3. Run: python main.py
4. Select a number from the menu.

IMPORTANT NOTES
- The current recipe uses 1/15 of each listed material per pie, as in the
  original program. Check that these amounts match your real recipe and units.
- The current selling price is ₱250 per pie.
- To preserve compatibility with the original code, the orders table's
  total_cost field currently stores profit, not revenue or material cost.
  The report labels explain this. For a more accurate long-term design, the
  database should store revenue, material cost, and profit in separate columns.
- Back up buko_pie_system.db before manually changing or deleting records.

