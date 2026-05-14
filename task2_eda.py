import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings("ignore")

# -------------------------------------------------------
# TASK 2: EXPLORATORY DATA ANALYSIS (EDA)
# -------------------------------------------------------
# EDA = "getting to know your data before doing anything serious"
# Like meeting someone new — you ask questions, look at them, 
# spot anything weird, then decide what to do next.

np.random.seed(42)

def create_dataset():
    """Create a realistic sales dataset"""
    n = 200
    regions    = np.random.choice(["North", "South", "East", "West"], n)
    categories = np.random.choice(["Electronics", "Clothing", "Food", "Books", "Sports"], n)
    months     = np.random.choice(range(1, 13), n)
    
    base_sales = {"Electronics": 500, "Clothing": 200, "Food": 80, "Books": 30, "Sports": 150}
    sales = [
        round(base_sales[cat] * np.random.uniform(0.5, 2.0) + np.random.normal(0, 20), 2)
        for cat in categories
    ]
    
    # Inject some issues EDA should catch
    sales[10] = -50      # Negative sale (error!)
    sales[25] = 9999     # Extreme outlier
    sales[40] = None     # Missing value
    sales[75] = None     # Missing value
    
    df = pd.DataFrame({
        "Month":      months,
        "Region":     regions,
        "Category":   categories,
        "Sales":      sales,
        "Units_Sold": np.random.randint(1, 50, n),
        "Discount_%": np.random.choice([0, 5, 10, 15, 20, 25], n),
    })
    return df

def run_eda(df):
    print("=" * 60)
    print("  📊 EXPLORATORY DATA ANALYSIS — Sales Dataset")
    print("=" * 60)

    # ── 1. Shape ─────────────────────────────────────────────────
    print(f"\n📐 STEP 1: SHAPE OF THE DATA")
    print(f"   Rows (records) : {df.shape[0]}")
    print(f"   Columns        : {df.shape[1]}")
    print(f"   Columns list   : {list(df.columns)}")

    # ── 2. Data types ─────────────────────────────────────────────
    print(f"\n🔠 STEP 2: DATA TYPES")
    for col, dtype in df.dtypes.items():
        print(f"   {col:<15} → {dtype}")

    # ── 3. Missing values ─────────────────────────────────────────
    print(f"\n❓ STEP 3: MISSING VALUES")
    missing = df.isnull().sum()
    total_missing = missing.sum()
    if total_missing == 0:
        print("   ✅ No missing values found!")
    else:
        for col, count in missing.items():
            if count > 0:
                pct = (count / len(df)) * 100
                print(f"   ⚠️  {col:<15} → {count} missing ({pct:.1f}%)")
    
    # Fix: fill missing sales with column median
    df["Sales"] = df["Sales"].fillna(df["Sales"].median())
    print(f"   ✅ Fixed: filled missing Sales with median")

    # ── 4. Descriptive statistics ─────────────────────────────────
    print(f"\n📈 STEP 4: DESCRIPTIVE STATISTICS")
    stats = df[["Sales", "Units_Sold", "Discount_%"]].describe().round(2)
    print(stats.to_string())

    # ── 5. Detect anomalies ───────────────────────────────────────
    print(f"\n🚨 STEP 5: ANOMALY DETECTION")
    neg_sales = df[df["Sales"] < 0]
    if not neg_sales.empty:
        print(f"   ⚠️  Found {len(neg_sales)} negative sales — likely data errors!")
        df.loc[df["Sales"] < 0, "Sales"] = 0
        print(f"   ✅ Fixed: replaced negative sales with 0")

    Q1, Q3 = df["Sales"].quantile(0.25), df["Sales"].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df["Sales"] < Q1 - 1.5*IQR) | (df["Sales"] > Q3 + 1.5*IQR)]
    print(f"   📌 Outliers detected (IQR method): {len(outliers)} records")
    
    # ── 6. Category & region summaries ───────────────────────────
    print(f"\n🏷️  STEP 6: SALES BY CATEGORY")
    cat_summary = df.groupby("Category")["Sales"].agg(["mean","sum","count"]).round(2)
    cat_summary.columns = ["Avg Sale", "Total Sales", "Count"]
    print(cat_summary.sort_values("Total Sales", ascending=False).to_string())

    print(f"\n🌍 STEP 7: SALES BY REGION")
    reg_summary = df.groupby("Region")["Sales"].agg(["mean","sum"]).round(2)
    reg_summary.columns = ["Avg Sale", "Total Sales"]
    print(reg_summary.sort_values("Total Sales", ascending=False).to_string())

    return df

def create_eda_charts(df):
    """Create a 2x2 grid of EDA charts"""
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle("📊 Exploratory Data Analysis — Sales Dataset", fontsize=16, fontweight="bold", y=0.98)
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

    colors = ["#4C72B0","#DD8452","#55A868","#C44E52","#8172B2"]

    # Chart 1: Sales distribution (histogram)
    ax1 = fig.add_subplot(gs[0, 0])
    clean = df[df["Sales"] >= 0]["Sales"]
    ax1.hist(clean, bins=25, color="#4C72B0", edgecolor="white", alpha=0.85)
    ax1.set_title("Sales Distribution", fontweight="bold")
    ax1.set_xlabel("Sales ($)")
    ax1.set_ylabel("Frequency")
    ax1.axvline(clean.mean(), color="red", linestyle="--", linewidth=1.5, label=f"Mean: ${clean.mean():.0f}")
    ax1.legend(fontsize=9)

    # Chart 2: Total sales by category (bar)
    ax2 = fig.add_subplot(gs[0, 1])
    cat_totals = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    bars = ax2.bar(cat_totals.index, cat_totals.values, color=colors, edgecolor="white")
    ax2.set_title("Total Sales by Category", fontweight="bold")
    ax2.set_ylabel("Total Sales ($)")
    ax2.tick_params(axis="x", rotation=15)
    for bar, val in zip(bars, cat_totals.values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                 f"${val:,.0f}", ha="center", va="bottom", fontsize=8, fontweight="bold")

    # Chart 3: Sales by region (pie)
    ax3 = fig.add_subplot(gs[1, 0])
    reg_totals = df.groupby("Region")["Sales"].sum()
    ax3.pie(reg_totals.values, labels=reg_totals.index, autopct="%1.1f%%",
            colors=colors, startangle=90, pctdistance=0.8)
    ax3.set_title("Sales Share by Region", fontweight="bold")

    # Chart 4: Discount % vs Sales (scatter)
    ax4 = fig.add_subplot(gs[1, 1])
    scatter_colors = [colors[["Electronics","Clothing","Food","Books","Sports"].index(c)] 
                      for c in df["Category"]]
    ax4.scatter(df["Discount_%"], df["Sales"], c=scatter_colors, alpha=0.5, s=40)
    ax4.set_title("Discount % vs Sales", fontweight="bold")
    ax4.set_xlabel("Discount (%)")
    ax4.set_ylabel("Sales ($)")

    plt.savefig("task2_eda_charts.png", dpi=130, bbox_inches="tight")
    plt.close()
    print("\n💾 EDA charts saved as 'task2_eda_charts.png'")

def main():
    df = create_dataset()
    df = run_eda(df)
    create_eda_charts(df)
    df.to_csv("task2_cleaned_dataset.csv", index=False)
    print("💾 Cleaned dataset saved as 'task2_cleaned_dataset.csv'")
    print("\n✅ EDA complete!\n")

if __name__ == "__main__":
    main()
