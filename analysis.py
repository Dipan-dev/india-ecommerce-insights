"""
E-Commerce Sales Analysis — Full Dashboard & Visualizations
Author  : Dipan Shil
Dataset : 3,000 orders | 500 customers | Jan–Dec 2023
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import warnings, os

warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.abspath(__file__))
DATA   = os.path.join(BASE, "data")
VIZ    = os.path.join(BASE, "visualizations")
os.makedirs(VIZ, exist_ok=True)

# ── Theme ──────────────────────────────────────────────────
BLUE       = "#185FA5"
LIGHT_BLUE = "#B5D4F4"
GREEN      = "#3B6D11"
AMBER      = "#BA7517"
CORAL      = "#993C1D"
GRAY       = "#5F5E5A"
LIGHT_GRAY = "#F1EFE8"
BG         = "#FAFAFA"
PALETTE    = [BLUE, "#378ADD", "#85B7EB", LIGHT_BLUE, "#E6F1FB"]
CAT_COLORS = [BLUE, GREEN, AMBER, CORAL, GRAY, "#534AB7"]

plt.rcParams.update({
    "font.family":      "DejaVu Sans",
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.facecolor":   BG,
    "figure.facecolor": BG,
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.titlecolor":  "#1A1A1A",
    "axes.labelsize":   10,
    "axes.labelcolor":  GRAY,
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
    "xtick.color":      GRAY,
    "ytick.color":      GRAY,
    "grid.color":       "#E0E0E0",
    "grid.linewidth":   0.5,
})

# ── Load & prep data ────────────────────────────────────────
orders    = pd.read_csv(os.path.join(DATA, "orders.csv"), parse_dates=["order_date"])
customers = pd.read_csv(os.path.join(DATA, "customers.csv"))

delivered = orders[orders["order_status"] == "Delivered"].copy()
delivered["month"]     = delivered["order_date"].dt.to_period("M")
delivered["month_str"] = delivered["order_date"].dt.strftime("%b")
delivered["month_num"] = delivered["order_date"].dt.month

print(f"Dataset loaded: {len(orders):,} orders | {len(customers):,} customers")
print(f"Delivered orders: {len(delivered):,} | Total revenue: ₹{delivered['total_amount'].sum():,.0f}\n")

# ═══════════════════════════════════════════════════════════
# CHART 1 — Monthly Revenue Trend
# ═══════════════════════════════════════════════════════════
monthly = (delivered.groupby(["month_num", "month_str"])
           .agg(revenue=("total_amount", "sum"), orders=("order_id", "count"))
           .reset_index().sort_values("month_num"))

fig, ax1 = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor(BG)

bars = ax1.bar(monthly["month_str"], monthly["revenue"] / 1e5,
               color=BLUE, alpha=0.85, width=0.55, zorder=2)
ax1.set_ylabel("Revenue (₹ Lakhs)", color=BLUE)
ax1.tick_params(axis="y", labelcolor=BLUE)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("₹%.1fL"))
ax1.set_ylim(0, monthly["revenue"].max() / 1e5 * 1.25)
ax1.grid(axis="y", zorder=0)

ax2 = ax1.twinx()
ax2.plot(monthly["month_str"], monthly["orders"], color=AMBER,
         marker="o", linewidth=2, markersize=6, zorder=3)
ax2.set_ylabel("No. of Orders", color=AMBER)
ax2.tick_params(axis="y", labelcolor=AMBER)
ax2.spines["right"].set_visible(True)
ax2.spines["right"].set_color(AMBER)

for bar, rev in zip(bars, monthly["revenue"]):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f"₹{rev/1e5:.1f}L", ha="center", va="bottom", fontsize=8, color=BLUE, fontweight="bold")

ax1.set_title("Monthly Revenue & Order Volume — 2023", pad=14)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, "01_monthly_revenue_trend.png"), dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 1: Monthly Revenue Trend")

# ═══════════════════════════════════════════════════════════
# CHART 2 — Category Revenue Breakdown (Horizontal Bar)
# ═══════════════════════════════════════════════════════════
cat_rev = (delivered.groupby("category")["total_amount"]
           .sum().sort_values(ascending=True).reset_index())

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(BG)

colors = [BLUE if i == len(cat_rev)-1 else LIGHT_BLUE for i in range(len(cat_rev))]
bars   = ax.barh(cat_rev["category"], cat_rev["total_amount"] / 1e5,
                 color=colors, height=0.55, zorder=2)
ax.set_xlabel("Revenue (₹ Lakhs)")
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("₹%.0fL"))
ax.grid(axis="x", zorder=0)

for bar, val in zip(bars, cat_rev["total_amount"]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f"₹{val/1e5:.1f}L", va="center", fontsize=9, color=GRAY, fontweight="bold")

ax.set_title("Revenue by Product Category", pad=14)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, "02_category_revenue.png"), dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 2: Category Revenue")

# ═══════════════════════════════════════════════════════════
# CHART 3 — Order Status Donut
# ═══════════════════════════════════════════════════════════
status_counts = orders["order_status"].value_counts()
status_colors = [GREEN, CORAL, AMBER, GRAY]

fig, ax = plt.subplots(figsize=(7, 6))
fig.patch.set_facecolor(BG)
wedges, texts, autotexts = ax.pie(
    status_counts, labels=status_counts.index,
    colors=status_colors, autopct="%1.1f%%",
    startangle=90, pctdistance=0.78,
    wedgeprops=dict(width=0.5, edgecolor=BG, linewidth=2)
)
for t in autotexts:
    t.set_fontsize(10); t.set_fontweight("bold"); t.set_color("white")
for t in texts:
    t.set_fontsize(10); t.set_color("#1A1A1A")

centre = plt.Circle((0, 0), 0.50, color=BG)
ax.add_artist(centre)
ax.text(0, 0, f"{len(orders):,}\nOrders", ha="center", va="center",
        fontsize=13, fontweight="bold", color="#1A1A1A")
ax.set_title("Order Status Distribution", pad=14)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, "03_order_status_donut.png"), dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 3: Order Status Donut")

# ═══════════════════════════════════════════════════════════
# CHART 4 — Top 10 Cities by Revenue
# ═══════════════════════════════════════════════════════════
city_rev = (delivered.groupby("city")["total_amount"]
            .sum().sort_values(ascending=False).head(10).reset_index())

fig, ax = plt.subplots(figsize=(11, 5))
fig.patch.set_facecolor(BG)
bar_colors = [BLUE if i < 3 else LIGHT_BLUE for i in range(len(city_rev))]
bars = ax.bar(city_rev["city"], city_rev["total_amount"] / 1e5,
              color=bar_colors, width=0.55, zorder=2)
ax.set_ylabel("Revenue (₹ Lakhs)")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("₹%.0fL"))
ax.grid(axis="y", zorder=0)

for bar, val in zip(bars, city_rev["total_amount"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f"₹{val/1e5:.1f}L", ha="center", va="bottom", fontsize=8, color=GRAY)

ax.set_title("Top 10 Cities by Sales Revenue", pad=14)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, "04_city_revenue.png"), dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 4: City Revenue")

# ═══════════════════════════════════════════════════════════
# CHART 5 — Payment Method Usage
# ═══════════════════════════════════════════════════════════
pay = (delivered.groupby("payment_method")["order_id"]
       .count().sort_values(ascending=False).reset_index())
pay.columns = ["method", "count"]
pay["pct"] = (pay["count"] / pay["count"].sum() * 100).round(1)

fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor(BG)
bars = ax.barh(pay["method"], pay["pct"],
               color=[BLUE, "#378ADD", "#85B7EB", LIGHT_BLUE, "#E6F1FB"],
               height=0.5, zorder=2)
ax.set_xlabel("Share of Orders (%)")
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax.grid(axis="x", zorder=0)

for bar, pct in zip(bars, pay["pct"]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f"{pct}%", va="center", fontsize=9, color=GRAY, fontweight="bold")

ax.set_title("Payment Method Preference", pad=14)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, "05_payment_methods.png"), dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 5: Payment Methods")

# ═══════════════════════════════════════════════════════════
# CHART 6 — Customer Segmentation (RFM Lite)
# ═══════════════════════════════════════════════════════════
cust_stats = (delivered.groupby("customer_id")
              .agg(order_count=("order_id","count"), total_spent=("total_amount","sum"))
              .reset_index())

def segment(n):
    if n >= 10: return "Champion"
    if n >= 5:  return "Loyal"
    if n >= 2:  return "Potential"
    return "One-Time"

cust_stats["segment"] = cust_stats["order_count"].apply(segment)
seg_summary = (cust_stats.groupby("segment")
               .agg(customers=("customer_id","count"), avg_ltv=("total_spent","mean"))
               .reset_index().sort_values("avg_ltv", ascending=False))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.patch.set_facecolor(BG)
seg_colors = [BLUE, "#378ADD", "#85B7EB", LIGHT_BLUE]

ax1.bar(seg_summary["segment"], seg_summary["customers"],
        color=seg_colors, width=0.5, zorder=2)
ax1.set_ylabel("Number of Customers")
ax1.set_title("Customers by Segment", pad=10)
ax1.grid(axis="y", zorder=0)
for i, (seg, cnt) in enumerate(zip(seg_summary["segment"], seg_summary["customers"])):
    ax1.text(i, cnt + 2, str(cnt), ha="center", fontsize=10, fontweight="bold", color=GRAY)

ax2.bar(seg_summary["segment"], seg_summary["avg_ltv"],
        color=seg_colors, width=0.5, zorder=2)
ax2.set_ylabel("Avg Lifetime Value (₹)")
ax2.set_title("Avg Lifetime Value by Segment", pad=10)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
ax2.grid(axis="y", zorder=0)
for i, (seg, val) in enumerate(zip(seg_summary["segment"], seg_summary["avg_ltv"])):
    ax2.text(i, val + 50, f"₹{val:,.0f}", ha="center", fontsize=9, fontweight="bold", color=GRAY)

fig.suptitle("Customer Segmentation Analysis", fontsize=14, fontweight="bold", color="#1A1A1A", y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, "06_customer_segments.png"), dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 6: Customer Segments")

# ═══════════════════════════════════════════════════════════
# CHART 7 — Discount Impact on Revenue
# ═══════════════════════════════════════════════════════════
def disc_tier(p):
    if p == 0:  return "No Discount"
    if p <= 10: return "Low (1–10%)"
    return "Medium (11–20%)"

delivered["disc_tier"] = delivered["discount_pct"].apply(disc_tier)
disc = (delivered.groupby("disc_tier")
        .agg(orders=("order_id","count"), avg_val=("total_amount","mean"),
             revenue=("total_amount","sum")).reset_index())

fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor(BG)
x = np.arange(len(disc))
b1 = ax.bar(x - 0.2, disc["revenue"] / 1e5, width=0.35, color=BLUE,  label="Total Revenue (₹L)", zorder=2)
b2 = ax.bar(x + 0.2, disc["avg_val"],        width=0.35, color=AMBER, label="Avg Order Value (₹)", zorder=2)
ax.set_xticks(x); ax.set_xticklabels(disc["disc_tier"])
ax.legend(fontsize=9); ax.grid(axis="y", zorder=0)
ax.set_title("Discount Tier vs Revenue & Avg Order Value", pad=14)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v:,.0f}"))
plt.tight_layout()
plt.savefig(os.path.join(VIZ, "07_discount_impact.png"), dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 7: Discount Impact")

# ═══════════════════════════════════════════════════════════
# CHART 8 — EXECUTIVE DASHBOARD (Summary KPI tiles)
# ═══════════════════════════════════════════════════════════
total_rev    = delivered["total_amount"].sum()
total_orders = len(delivered)
unique_custs = delivered["customer_id"].nunique()
avg_ov       = delivered["total_amount"].mean()
return_rate  = (orders[orders["order_status"]=="Returned"].shape[0] / len(orders) * 100)
top_category = delivered.groupby("category")["total_amount"].sum().idxmax()

fig = plt.figure(figsize=(14, 9))
fig.patch.set_facecolor(BG)
gs  = gridspec.GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.35)

# KPI tiles
kpis = [
    ("Total Revenue",     f"₹{total_rev/1e5:.1f}L",       BLUE),
    ("Orders Delivered",  f"{total_orders:,}",              GREEN),
    ("Unique Customers",  f"{unique_custs:,}",              AMBER),
    ("Avg Order Value",   f"₹{avg_ov:,.0f}",               CORAL),
    ("Return Rate",       f"{return_rate:.1f}%",            GRAY),
    ("Top Category",      top_category,                     "#534AB7"),
]
for idx, (label, value, color) in enumerate(kpis):
    row, col = divmod(idx, 3)
    ax = fig.add_subplot(gs[row, col])
    ax.set_facecolor(BG)
    ax.axis("off")
    rect = FancyBboxPatch((0.05, 0.1), 0.9, 0.8, boxstyle="round,pad=0.05",
                          linewidth=1.5, edgecolor=color, facecolor="white",
                          transform=ax.transAxes, zorder=2)
    ax.add_patch(rect)
    ax.text(0.5, 0.68, value, transform=ax.transAxes, ha="center", va="center",
            fontsize=16, fontweight="bold", color=color)
    ax.text(0.5, 0.28, label, transform=ax.transAxes, ha="center", va="center",
            fontsize=9, color=GRAY)

# Mini monthly trend in dashboard
ax_trend = fig.add_subplot(gs[0:2, 3])
ax_trend.set_facecolor(BG)
ax_trend.plot(monthly["month_str"], monthly["revenue"] / 1e5,
              color=BLUE, linewidth=2, marker="o", markersize=4)
ax_trend.fill_between(range(len(monthly)), monthly["revenue"] / 1e5,
                      alpha=0.12, color=BLUE)
ax_trend.set_xticks(range(len(monthly)))
ax_trend.set_xticklabels(monthly["month_str"], fontsize=7, rotation=45)
ax_trend.yaxis.set_major_formatter(mticker.FormatStrFormatter("₹%.0fL"))
ax_trend.set_title("Monthly Revenue", fontsize=10, fontweight="bold")
ax_trend.grid(axis="y")

# Mini category bar in dashboard
ax_cat = fig.add_subplot(gs[2, :])
ax_cat.set_facecolor(BG)
cat_sorted = delivered.groupby("category")["total_amount"].sum().sort_values(ascending=False)
ax_cat.bar(cat_sorted.index, cat_sorted.values / 1e5, color=CAT_COLORS, width=0.5, zorder=2)
ax_cat.set_ylabel("Revenue (₹L)", fontsize=9)
ax_cat.yaxis.set_major_formatter(mticker.FormatStrFormatter("₹%.0fL"))
ax_cat.set_title("Revenue by Category", fontsize=10, fontweight="bold")
ax_cat.grid(axis="y", zorder=0)

fig.suptitle("E-Commerce Sales Dashboard — 2023", fontsize=16,
             fontweight="bold", color="#1A1A1A", y=1.01)
plt.savefig(os.path.join(VIZ, "08_executive_dashboard.png"), dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 8: Executive Dashboard")

# ── Final summary ───────────────────────────────────────────
print("\n" + "="*55)
print("  ALL CHARTS GENERATED SUCCESSFULLY")
print("="*55)
print(f"\n  Output folder : {VIZ}")
print(f"  Charts created: 8")
print(f"\n  Quick stats:")
print(f"  • Total Revenue    : ₹{total_rev:,.0f}")
print(f"  • Delivered Orders : {total_orders:,}")
print(f"  • Unique Customers : {unique_custs:,}")
print(f"  • Avg Order Value  : ₹{avg_ov:,.0f}")
print(f"  • Return Rate      : {return_rate:.1f}%")
print(f"  • Top Category     : {top_category}")
print("="*55)
