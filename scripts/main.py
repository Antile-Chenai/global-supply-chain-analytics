import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
data = {
    "Supplier": np.random.choice(["Supplier A", "Supplier B", "Supplier C"], 100),
    "Region": np.random.choice(["North", "South", "East", "West"], 100),
    "LeadTimeDays": np.random.randint(1, 30, 100),
    "UnitsShipped": np.random.randint(10, 500, 100),
    "Delay": np.random.randint(0, 10, 100)
}
df = pd.DataFrame(data)
df["Delay"] = df["Delay"].apply(lambda x: max(x, 0))
print(df.head())
supplier_summary = df.groupby("Supplier").agg({"UnitsShipped":"sum","LeadTimeDays":"mean","Delay":"mean"}).reset_index()
region_summary = df.groupby("Region").agg({"UnitsShipped":"sum","LeadTimeDays":"mean","Delay":"mean"}).reset_index()
plt.figure(figsize=(10,6))
sns.barplot(x="Supplier", y="UnitsShipped", data=supplier_summary)
plt.savefig("units_by_supplier.png")
plt.close()
plt.figure(figsize=(10,6))
sns.barplot(x="Region", y="UnitsShipped", data=region_summary)
plt.savefig("units_by_region.png")
plt.close()
plt.figure(figsize=(10,6))
sns.scatterplot(x="LeadTimeDays", y="Delay", hue="Supplier", data=df)
plt.savefig("leadtime_vs_delay.png")
plt.close()
print("Analysis complete. Plots saved.")
