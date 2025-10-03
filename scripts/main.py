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
    'ProductID': range(1, 16),
    'Warehouse': np.random.choice(['WH1','WH2','WH3'], 15),
    'Stock': np.random.randint(100,500,15)
})

shipments = pd.DataFrame({
    'ShipmentID': range(101,116),
    'ProductID': range(1,16),
    'QuantityShipped': np.random.randint(20,200,15),
    'Destination': np.random.choice(['NY','CA','TX'], 15)
})

orders = pd.DataFrame({
    'OrderID': range(1001,1016),
    'ProductID': range(1,16),
    'QuantityOrdered': np.random.randint(10,180,15),
    'OrderDate': pd.date_range('2025-01-01', periods=15)
})

# -------------------------
# 2. Merge & Clean Data
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
    'Stock':'sum',
    'QuantityShipped':'sum',
    'QuantityOrdered':'sum'
}).reset_index()
print("\nWarehouse Summary:\n", warehouse_summary)

total_products = data['ProductID'].nunique()
total_orders = data['QuantityOrdered'].sum()
total_shipped = data['QuantityShipped'].sum()

print(f"\nTotal Products: {total_products}")
print(f"Total Orders: {total_orders}")
print(f"Total Quantity Shipped: {total_shipped}")

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

print("\nGlobal Supply Chain Analytics Project Completed!")
