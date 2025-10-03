# Global Supply Chain Analytics
# Author: Antile Kaba
# Date: 2025-10-02

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# 1. Load Sample Data
# -------------------------
inventory = pd.DataFrame({
    'ProductID': range(1, 11),
    'Warehouse': ['WH1','WH2','WH1','WH3','WH2','WH1','WH3','WH2','WH1','WH3'],
    'Stock': [150, 200, 120, 300, 180, 250, 270, 190, 160, 220]
})

shipments = pd.DataFrame({
    'ShipmentID': range(101, 111),
    'ProductID': range(1, 11),
    'QuantityShipped': [50, 70, 60, 120, 80, 90, 110, 60, 70, 100],
    'Destination': ['NY','CA','TX','NY','CA','TX','NY','CA','TX','NY']
})

orders = pd.DataFrame({
    'OrderID': range(1001,1011),
    'ProductID': range(1,11),
    'QuantityOrdered': [40, 60, 50, 100, 70, 80, 90, 50, 60, 95],
    'OrderDate': pd.date_range('2025-01-01', periods=10)
})

# -------------------------
# 2. Data Cleaning & Merge
# -------------------------
data = pd.merge(inventory, shipments, on='ProductID')
data = pd.merge(data, orders, on='ProductID')

print("Missing values per column:\n", data.isnull().sum())

data['StockAfterShipment'] = data['Stock'] - data['QuantityShipped']
data['StockVsOrder'] = data['StockAfterShipment'] - data['QuantityOrdered']

# -------------------------
# 3. Analytics
# -------------------------
low_stock = data[data['StockVsOrder'] < 0]
print("\nProducts with stock deficit:\n", low_stock[['ProductID','StockVsOrder']])

warehouse_summary = data.groupby('Warehouse').agg({
    'Stock': 'sum',
    'QuantityShipped': 'sum',
    'QuantityOrdered': 'sum'
}).reset_index()
print("\nWarehouse Summary:\n", warehouse_summary)

# -------------------------
# 4. Visualizations
# -------------------------
sns.set_style('whitegrid')

plt.figure(figsize=(8,5))
sns.barplot(x='Warehouse', y='Stock', data=warehouse_summary)
plt.title('Total Stock per Warehouse')
plt.savefig('stock_per_warehouse.png')
plt.close()

plt.figure(figsize=(8,5))
warehouse_summary.plot(x='Warehouse', y=['QuantityShipped','QuantityOrdered'], kind='bar')
plt.title('Shipments vs Orders per Warehouse')
plt.savefig('shipments_vs_orders.png')
plt.close()

if not low_stock.empty:
    plt.figure(figsize=(8,5))
    sns.barplot(x='ProductID', y='StockVsOrder', data=low_stock)
    plt.title('Products with Stock Deficit')
    plt.savefig('stock_deficit.png')
    plt.close()

# -------------------------
# 5. Summary Metrics
# -------------------------
total_products = data['ProductID'].nunique()
total_orders = data['QuantityOrdered'].sum()
total_shipped = data['QuantityShipped'].sum()

print(f"\nTotal Products: {total_products}")
print(f"Total Orders: {total_orders}")
print(f"Total Quantity Shipped: {total_shipped}")
print("\nGlobal Supply Chain Analytics Project Completed!")
