import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# --- CONFIG ---
N_CUSTOMERS = 500
N_ORDERS    = 3000
START_DATE  = datetime(2023, 1, 1)
END_DATE    = datetime(2023, 12, 31)

CATEGORIES  = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Sports", "Beauty"]
PRODUCTS    = {
    "Electronics":    [("Wireless Earbuds", 1299), ("Smart Watch", 3499), ("Laptop Stand", 899),  ("USB Hub", 499),     ("Bluetooth Speaker", 1599)],
    "Clothing":       [("Men's T-Shirt", 399),     ("Women's Kurta", 599),("Running Shoes", 1999),("Casual Jeans", 999), ("Hoodie", 1199)],
    "Home & Kitchen": [("Air Fryer", 2999),         ("Water Bottle", 299), ("Chopping Board", 199),("Coffee Mug Set", 499),("Storage Box", 349)],
    "Books":          [("Data Science 101", 499),   ("Python Crash Course", 399), ("Atomic Habits", 299), ("Think Again", 349), ("Deep Work", 319)],
    "Sports":         [("Yoga Mat", 799),            ("Resistance Bands", 349), ("Skipping Rope", 199), ("Gym Gloves", 299), ("Water Sipper", 399)],
    "Beauty":         [("Face Serum", 899),          ("Sunscreen SPF50", 499),  ("Lip Balm Set", 249),  ("Moisturizer", 699), ("Hair Oil", 349)],
}
CITIES      = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
PAYMENT     = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]
STATUS      = ["Delivered", "Returned", "Cancelled", "Pending"]
STATUS_PROB = [0.78, 0.08, 0.09, 0.05]

# --- CUSTOMERS ---
customers = pd.DataFrame({
    "customer_id":   [f"CUST{str(i).zfill(4)}" for i in range(1, N_CUSTOMERS+1)],
    "customer_name": [f"Customer_{i}" for i in range(1, N_CUSTOMERS+1)],
    "city":          np.random.choice(CITIES, N_CUSTOMERS),
    "signup_date":   [START_DATE - timedelta(days=random.randint(30, 730)) for _ in range(N_CUSTOMERS)],
    "age_group":     np.random.choice(["18-24", "25-34", "35-44", "45-54", "55+"], N_CUSTOMERS, p=[0.15, 0.35, 0.28, 0.14, 0.08]),
})

# --- ORDERS ---
order_rows = []
for i in range(1, N_ORDERS+1):
    category    = random.choice(CATEGORIES)
    product, base_price = random.choice(PRODUCTS[category])
    qty         = random.randint(1, 4)
    discount    = random.choice([0, 0, 0, 5, 10, 15, 20])
    unit_price  = base_price
    total       = round(unit_price * qty * (1 - discount/100), 2)
    order_date  = START_DATE + timedelta(days=random.randint(0, 364))
    cust        = f"CUST{str(random.randint(1, N_CUSTOMERS)).zfill(4)}"
    status      = np.random.choice(STATUS, p=STATUS_PROB)
    order_rows.append({
        "order_id":       f"ORD{str(i).zfill(5)}",
        "customer_id":    cust,
        "product_name":   product,
        "category":       category,
        "quantity":       qty,
        "unit_price":     unit_price,
        "discount_pct":   discount,
        "total_amount":   total,
        "order_date":     order_date.strftime("%Y-%m-%d"),
        "payment_method": random.choice(PAYMENT),
        "order_status":   status,
        "city":           customers.loc[customers.customer_id == cust, "city"].values[0],
    })

orders = pd.DataFrame(order_rows)

os.makedirs(os.path.dirname(__file__) or ".", exist_ok=True)
customers.to_csv(os.path.join(os.path.dirname(__file__), "customers.csv"), index=False)
orders.to_csv(os.path.join(os.path.dirname(__file__), "orders.csv"), index=False)
print(f"Generated {len(customers)} customers and {len(orders)} orders.")
