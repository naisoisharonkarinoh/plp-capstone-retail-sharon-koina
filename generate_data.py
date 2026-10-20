import pandas as pd
import numpy as np
from pathlib import Path

# Reproducible synthetic supermarket dataset
np.random.seed(42)

# Save files in the same folder as this script
DATA_DIR = Path(__file__).resolve().parent
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 1. Products table
products = pd.DataFrame({
    "product_id": range(1, 21),
    "product_name": [
        "Rice", "Sugar", "Cooking Oil", "Maize Flour",
        "Wheat Flour", "Milk", "Bread", "Eggs",
        "Tea", "Coffee", "Soap", "Toothpaste",
        "Detergent", "Biscuits", "Juice", "Water",
        "Pasta", "Beans", "Salt", "Cereal"
    ],
    "category": [
        "Groceries", "Groceries", "Groceries", "Groceries",
        "Groceries", "Dairy", "Bakery", "Dairy",
        "Beverages", "Beverages", "Household", "Personal Care",
        "Household", "Snacks", "Beverages", "Beverages",
        "Groceries", "Groceries", "Groceries", "Breakfast"
    ],
    "unit_price": [
        180, 160, 350, 120, 150, 70, 65, 25, 120, 300,
        100, 150, 250, 50, 100, 50, 130, 170, 40, 220
    ]
})

# 2. Branches table
branches = pd.DataFrame({
    "branch_id": [1, 2, 3, 4, 5],
    "branch_name": [
        "Nairobi", "Kisumu", "Nakuru", "Mombasa", "Eldoret"
    ]
})

# 3. Customers table
number_of_customers = 5000

customers = pd.DataFrame({
    "customer_id": range(1, number_of_customers + 1),
    "customer_segment": np.random.choice(
        ["Regular", "Occasional", "Premium"],
        size=number_of_customers,
        p=[0.50, 0.35, 0.15]
    )
})

# 4. Generate 50,000 transactions
number_of_transactions = 50000

transactions = pd.DataFrame({
    "transaction_id": range(1, number_of_transactions + 1),
    "date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2025-01-01", "2025-12-31"),
            size=number_of_transactions
        )
    ),
    "customer_id": np.random.randint(
        1, number_of_customers + 1,
        size=number_of_transactions
    ),
    "product_id": np.random.randint(
        1, len(products) + 1,
        size=number_of_transactions
    ),
    "branch_id": np.random.randint(
        1, len(branches) + 1,
        size=number_of_transactions
    ),
    "quantity": np.random.randint(
        1, 11, size=number_of_transactions
    )
})

# Add product prices and calculate revenue
transactions = transactions.merge(
    products[["product_id", "unit_price"]],
    on="product_id",
    how="left"
)

transactions["sales_amount"] = (
    transactions["quantity"] * transactions["unit_price"]
)

# Save the four tables
transactions.to_csv(DATA_DIR / "transactions.csv", index=False)
products.to_csv(DATA_DIR / "products.csv", index=False)
branches.to_csv(DATA_DIR / "branches.csv", index=False)
customers.to_csv(DATA_DIR / "customers.csv", index=False)

print("Dataset generation complete.")
print(f"Transactions: {len(transactions):,}")
print(f"Products: {len(products):,}")
print(f"Branches: {len(branches):,}")
print(f"Customers: {len(customers):,}")
