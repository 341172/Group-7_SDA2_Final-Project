"""
master_data.py - ONE shared set of customers, products, stores, warehouses
and devices, used by all four producers.

This is what joins the four data sources into one business:
  * the same customer browses (Stream 2), buys (Stream 1),
    owns a smart appliance (Stream 4) and raises service tickets (Stream 4)
  * the same product is carted (2), sold (1), stocked and shipped (3)
    and serviced (4)

A fixed random seed keeps this master data identical every time and in
every producer.
"""

import random

_rng = random.Random(42)

CITIES = ["Jaipur", "Mumbai", "Bangalore", "Delhi", "Kolkata"]

PRODUCTS = [
    {"id": "P1001", "name": "55-inch Smart LED TV",           "category": "Television",        "price": 42999, "smart": True},
    {"id": "P1002", "name": "Double Door Refrigerator 260L",  "category": "Refrigerator",      "price": 28999, "smart": True},
    {"id": "P1003", "name": "1.5 Ton Split Inverter AC",      "category": "Air Conditioner",   "price": 34999, "smart": True},
    {"id": "P1004", "name": "Front Load Washing Machine 7Kg", "category": "Washing Machine",   "price": 26999, "smart": True},
    {"id": "P1005", "name": "Microwave Oven 23L Convection",  "category": "Kitchen Appliance", "price": 10999, "smart": False},
]
PRODUCT_BY_ID = {p["id"]: p for p in PRODUCTS}
SMART_PRODUCTS = [p for p in PRODUCTS if p["smart"]]

STORES = {
    "Store-Jaipur-01": "Jaipur",
    "Store-Mumbai-04": "Mumbai",
    "Store-Bangalore-02": "Bangalore",
    "Store-Delhi-07": "Delhi",
}
STORE_BY_CITY = {city: store for store, city in STORES.items()}

WAREHOUSES = {
    "WH-North": "Delhi",
    "WH-South": "Bangalore",
    "WH-West": "Mumbai",
    "WH-East": "Kolkata",
}

# 200 customers, each with a home city
CUSTOMERS = {f"CUST{1000 + i}": _rng.choice(CITIES) for i in range(200)}
CUSTOMER_IDS = list(CUSTOMERS)
RISKY_CUSTOMERS = CUSTOMER_IDS[:2]   # these two behave suspiciously in Stream 1

# 40 smart appliances already sold to customers (Stream 4 telemetry)
DEVICES = []
for i in range(40):
    product = SMART_PRODUCTS[i % len(SMART_PRODUCTS)]
    owner = _rng.choice(CUSTOMER_IDS)
    DEVICES.append({
        "device_id": f"DEV{5000 + i}",
        "customer_id": owner,
        "city": CUSTOMERS[owner],
        "product_id": product["id"],
        "product_name": product["name"],
        "category": product["category"],
    })
HOT_DEVICE_IDS = {d["device_id"] for d in _rng.sample(DEVICES, 4)}   # running hot
