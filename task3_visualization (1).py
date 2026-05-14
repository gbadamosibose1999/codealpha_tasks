import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings("ignore")

# -------------------------------------------------------
# TASK 3: DATA VISUALIZATION
# -------------------------------------------------------
# Turning numbers into pictures so anyone can understand them.
# "A picture is worth a thousand rows of data!" 😄

np.random.seed(7)

def create_dataset():
    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]
    products = ["Laptop","Phone","Tablet","Headphones","Smartwatch"]

    records = []
    base = {"Laptop":900,"Phone":600,"Tablet":400,"Headphones":150,"Smartwatch":250}
    for month in months:
        for product in products:
            sales = max(0, base[product] * np.random.uniform(0.7, 1.5) + np.random.normal(0, 30))
            units = int(sales / base[product] * np.random.randint(5, 30))
            records.append({"Month": month, "Product": product,
                             "Revenue": round(sales, 2), "Units": units})

    df = pd.DataFrame(records)
    df["Month_Num"] = df["Month"].apply(lambda m: 
        ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].index(m)+1)
    return df.sort_values("Month_Num")

def build_dashboard(df):
    months_order = ["Jan","Feb","Mar","Apr","May","Jun",
                    "Jul","Aug","Sep","Oct","Nov","Dec"]
    products     = df["Product"].unique()
    palette      = ["#2196F3","#FF9800","#4CAF50","#E91E63","#9C27B0"]
    prod_colors  = dict(zip(products, palette))

    fig = plt.figure(figsize=(18, 14))
    fig.patch.set_facecolor("#F8F9FA")
    fig.suptitle("🖥️  Electronics Sales Dashboard — Full Year Analysis",
                 fontsize=18, fontweight="bold", y=0.98)

    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.5, wspace=0.35)

    # ── Chart 1: Monthly revenue trend (line) ─────────────────────
    ax1 = fig.add_subplot(gs[0, :2])
    monthly = df.groupby("Month")["Revenue"].sum().reindex(months_order)
    ax1.plot(months_order, monthly.values, color="#2196F3", linewidth=2.5,
             marker="o", markersize=7, markerfacecolor="white", markeredgewidth=2)
    ax1.fill_between(range(12), monthly.values, alpha=0.12, color="#2196F3")
    ax1.set_title("📈 Monthly Total Revenue", fontweight="bold", fontsize=13)
    ax1.set_ylabel("Revenue ($)")
    ax1.set_xticks(range(12))
    ax1.set_xticklabels(months_order, rotation=30)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax1.set_facecolor("#FAFAFA")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    peak_idx = monthly.values.argmax()
    ax1.annotate(f"Peak: ${monthly.values[peak_idx]:,.0f}",
                 xy=(peak_idx, monthly.values[peak_idx]),
                 xytext=(peak_idx + 0.5, monthly.values[peak_idx] + 200),
                 arrowprops=dict(arrowstyle="->", color="red"),
                 fontsize=9, color="red")

    # ── Chart 2: Revenue share by product (donut) ─────────────────
    ax2 = fig.add_subplot(gs[0, 2])
    prod_rev = df.groupby("Product")["Revenue"].sum()
    wedges, texts, autotexts = ax2.pie(
        prod_rev.values, labels=None, autopct="%1.1f%%",
        colors=palette, startangle=90, pctdistance=0.75,
        wedgeprops={"width": 0.55, "edgecolor": "white", "linewidth": 2})
    for at in autotexts:
        at.set_fontsize(8)
    ax2.legend(prod_rev.index, loc="lower center", bbox_to_anchor=(0.5, -0.15),
               ncol=2, fontsize=8)
    ax2.set_title("🍩 Revenue Share\nby Product", fontweight="bold", fontsize=12)

    # ── Chart 3: Stacked bar — revenue per product per month ──────
    ax3 = fig.add_subplot(gs[1, :])
    pivot = df.pivot_table(index="Month", columns="Product",
                           values="Revenue", aggfunc="sum").reindex(months_order)
    bottom = np.zeros(12)
    for prod, color in zip(products, palette):
        vals = pivot[prod].values
        ax3.bar(months_order, vals, bottom=bottom, label=prod,
                color=color, alpha=0.88, edgecolor="white")
        bottom += vals
    ax3.set_title("📊 Monthly Revenue Breakdown by Product (Stacked)", 
                  fontweight="bold", fontsize=13)
    ax3.set_ylabel("Revenue ($)")
    ax3.legend(loc="upper right", fontsize=9)
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax3.tick_params(axis="x", rotation=30)
    ax3.set_facecolor("#FAFAFA")
    ax3.grid(axis="y", linestyle="--", alpha=0.4)

    # ── Chart 4: Units sold by product (horizontal bar) ───────────
    ax4 = fig.add_subplot(gs[2, 0])
    prod_units = df.groupby("Product")["Units"].sum().sort_values()
    bars = ax4.barh(prod_units.index, prod_units.values,
                    color=[prod_colors[p] for p in prod_units.index],
                    edgecolor="white", height=0.6)
    for bar, val in zip(bars, prod_units.values):
        ax4.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                 str(val), va="center", fontsize=9, fontweight="bold")
    ax4.set_title("📦 Total Units Sold\nby Product", fontweight="bold", fontsize=12)
    ax4.set_xlabel("Units Sold")
    ax4.set_facecolor("#FAFAFA")

    # ── Chart 5: Avg revenue per unit (bar + value labels) ────────
    ax5 = fig.add_subplot(gs[2, 1])
    prod_avg = (df.groupby("Product")["Revenue"].sum() /
                df.groupby("Product")["Units"].sum()).sort_values(ascending=False)
    bars5 = ax5.bar(prod_avg.index, prod_avg.values,
                    color=[prod_colors[p] for p in prod_avg.index],
                    edgecolor="white")
    for bar, val in zip(bars5, prod_avg.values):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f"${val:.0f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax5.set_title("💰 Avg Revenue\nper Unit", fontweight="bold", fontsize=12)
    ax5.set_ylabel("$ per Unit")
    ax5.tick_params(axis="x", rotation=20)
    ax5.set_facecolor("#FAFAFA")

    # ── Chart 6: Revenue heatmap (month × product) ────────────────
    ax6 = fig.add_subplot(gs[2, 2])
    heatmap_data = pivot.T  # products as rows, months as columns
    im = ax6.imshow(heatmap_data.values, aspect="auto", cmap="YlOrRd")
    ax6.set_xticks(range(12))
    ax6.set_xticklabels(months_order, rotation=45, fontsize=7)
    ax6.set_yticks(range(len(products)))
    ax6.set_yticklabels(heatmap_data.index, fontsize=8)
    ax6.set_title("🌡️ Revenue Heatmap\n(Month × Product)", fontweight="bold", fontsize=12)
    plt.colorbar(im, ax=ax6, fraction=0.046, pad=0.04)

    import os
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task3_dashboard.png")
    plt.savefig(save_path, dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print(f"\n💾 Dashboard saved at:\n   {save_path}")
    plt.show()
    plt.close()

def main():
    print("=" * 55)
    print("  📊 DATA VISUALIZATION — Electronics Dashboard")
    print("=" * 55)
    print("\n🔨 Building dataset...")
    df = create_dataset()
    print(f"✅ Dataset ready: {len(df)} records\n")
    print("🎨 Creating 6-chart dashboard...")
    build_dashboard(df)
    df.to_csv("task3_sales_data.csv", index=False)
    print("💾 Data saved as 'task3_sales_data.csv'")
    print("\n✅ Data visualization complete!\n")

if __name__ == "__main__":
    main()
