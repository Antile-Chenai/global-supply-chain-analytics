# scripts/main.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Simulate supply chain dataset
np.random.seed(42)
data = {
    "Supplier": np.random.choice(["Supplier A", "Supplier B", "Supplier C"], 100),
    "Region": np.random.choice(["North", "South", "East", "West"], 100),
    "LeadTimeDays": np.random.randint(1, 30, 100),
    "UnitsShipped": np.random.randint(10, 500, 100),
    "Delay": np.random.randint(0, 10, 100)
}

df = pd.DataFrame(data)

# Data Cleaning
df["Delay"] = df["Delay"].apply(lambda x: max(x, 0))
print("First 5 rows of dataset:")
print(df.head())

# Summary Statistics
print("\nSummary Statistics:")
print(df.describe())

# Aggregation by Supplier
supplier_summary = df.groupby("Supplier").agg({
    "UnitsShipped": "sum",
    "LeadTimeDays": "mean",
    "Delay": "mean"
}).reset_index()
print("\nSupplier Summary:")
print(supplier_summary)

# Aggregation by Region
region_summary = df.groupby("Region").agg({
    "UnitsShipped": "sum",
    "LeadTimeDays": "mean",
    "Delay": "mean"
}).reset_index()
print("\nRegion Summary:")
print(region_summary)

# Visualizations
plt.figure(figsize=(10,6))
sns.barplot(x="Supplier", y="UnitsShipped", data=supplier_summary)
plt.title("Total Units Shipped by Supplier")
plt.savefig("units_by_supplier.png")
plt.close()

plt.figure(figsize=(10,6))
sns.barplot(x="Region", y="UnitsShipped", data=region_summary)
plt.title("Total Units Shipped by Region")
plt.savefig("units_by_region.png")
plt.close()

plt.figure(figsize=(10,6))
sns.scatterplot(x="LeadTimeDays", y="Delay", hue="Supplier", data=df)
plt.title("Lead Time vs Delay by Supplier")
plt.savefig("leadtime_vs_delay.png")
plt.close()

print("\nAnalysis complete. Plots saved as PNG files.")
