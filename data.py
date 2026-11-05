"""
Swiggy Limited - data extracted from the Annual Report FY 2024-25.

Units
-----
* Financial statements (P&L, balance sheet, cash flow, segments): INR Million,
  exactly as printed in the *consolidated* statements.
* Operating KPIs (orders, GOV, AOV ...): as printed in the management KPI pages
  (GOV and revenue in INR Crore, orders / users in million).

FY25 = year ended 31 March 2025, FY24 = year ended 31 March 2024.
"""
import pandas as pd

YEARS_FIN = ["FY25", "FY24"]

# --------------------------------------------------------------------------
# 1. Consolidated Statement of Profit & Loss   (INR Million)  [PDF p.104]
# --------------------------------------------------------------------------
INCOME = {
    "Revenue from operations": (152267.55, 112473.90),
    "Other income":            (3961.70,   3869.59),
}

# Cost of materials + purchases of stock-in-trade + inventory change are grouped
# into one line ("Cost of goods & materials") to keep the charts readable.
EXPENSES = {
    "Cost of goods & materials":    (283.60 + 59854.42 - 122.75, 610.83 + 45547.50 - 116.34),
    "Delivery & related charges":   (44292.03, 33510.59),
    "Advertising & sales promotion": (27117.00, 18507.99),
    "Employee benefits":            (25488.62, 20121.64),
    "Other expenses":               (23212.96, 16371.75),
    "Depreciation & amortisation":  (6122.75,  4205.85),
    "Finance costs":                (1005.86,  714.03),
}

TOTAL_EXPENSES = (187254.49, 139473.84)
ASSOCIATE_LOSS = (-25.74, -66.14)
EXCEPTIONAL    = (-117.01, -305.94)
NET_LOSS       = (-31167.99, -23502.43)      # loss before tax = loss for the year (no tax)
EPS            = (-13.72, -10.70)            # INR per share, basic & diluted
SHARE_BASED_PAYMENT = (11728.45, 5962.62)    # ESOP expense (non-cash) [segment note]

# Management-defined "Adjusted EBITDA" (MD&A, INR Crore -> converted to Million)
ADJ_EBITDA = (-1911.66 * 10, -1835.57 * 10)

# --------------------------------------------------------------------------
# 2. Consolidated Balance Sheet (INR Million)  [PDF p.103]
# --------------------------------------------------------------------------
BALANCE = pd.DataFrame(
    {
        "FY25": {
            "Property, plant & equipment": 10591.67,
            "Right-of-use assets": 16246.31,
            "Goodwill & intangibles": 6964.67 + 2505.19,
            "Non-current investments": 12962.39 + 577.83,
            "Other non-current assets": 8883.13 + 1251.70 + 1014.79,
            "Inventories": 554.88,
            "Current investments": 13230.57,
            "Trade receivables": 24625.46,
            "Cash & cash equivalents": 12305.68,
            "Other bank balances": 20690.46,
            "Other current assets": 16098.08 + 3550.37,
            "Equity": 102194.87,
            "Non-current liabilities": 13982.33,
            "Trade payables": 18180.43,
            "Other current liabilities": 35875.98 - 18180.43,
        },
        "FY24": {
            "Property, plant & equipment": 4527.85,
            "Right-of-use assets": 5877.99,
            "Goodwill & intangibles": 6964.67 + 3043.11,
            "Non-current investments": 13822.84 + 603.58,
            "Other non-current assets": 948.89 + 1603.01 + 535.99,
            "Inventories": 486.90,
            "Current investments": 37284.70,
            "Trade receivables": 9638.50,
            "Cash & cash equivalents": 8870.51,
            "Other bank balances": 38.00,
            "Other current assets": 8268.00 + 2779.67,
            "Equity": 77914.61,
            "Non-current liabilities": 6311.58,
            "Trade payables": 8808.98,
            "Other current liabilities": 21068.02 - 8808.98,
        },
    }
)

BS_TOTALS = {
    "Total non-current assets": (60997.68, 37927.93),
    "Total current assets":     (91055.50, 67366.28),
    "Total assets":             (152053.18, 105294.21),
    "Total equity":             (102194.87, 77914.61),
    "Total non-current liabilities": (13982.33, 6311.58),
    "Total current liabilities":     (35875.98, 21068.02),
    "Total liabilities":        (49858.31, 27379.60),
}

# Debt-like items: borrowings + lease liabilities (current + non-current)
DEBT = (282.34 + 0 + 13173.12 + 3573.99, 959.77 + 1152.09 + 4670.59 + 1859.45)
LIQUID_FUNDS = (12305.68 + 20690.46 + 13230.57, 8870.51 + 38.00 + 37284.70)

# --------------------------------------------------------------------------
# 3. Consolidated Cash Flow (INR Million)  [PDF p.105-106]
# --------------------------------------------------------------------------
CASH_FLOW = {
    "Operating activities": (-21694.72, -13127.35),
    "Investing activities": (-13724.42, 14584.58),
    "Financing activities": (39033.73,  -1227.95),
}
CAPEX = (-7508.11, -3517.14)
NET_CASH_CHANGE = (3614.59, 229.28)

# --------------------------------------------------------------------------
# 4. Segment note (INR Million)  [PDF p.131]  - external revenue & segment result
# --------------------------------------------------------------------------
SEGMENTS = pd.DataFrame(
    {
        "Segment": [
            "Food Delivery", "Quick Commerce (Instamart)", "Out-of-home Consumption",
            "Supply Chain & Distribution", "Platform Innovations",
        ],
        "Revenue FY25": [63528.94, 21295.84, 2384.50, 64175.00, 883.27],
        "Revenue FY24": [51601.25, 9785.50, 1571.86, 47796.05, 1719.24],
        "Result FY25":  [6025.44, -18960.68, -282.54, -2177.90, -734.20],
        "Result FY24":  [-94.27, -11846.09, -1735.96, -1338.53, -1102.59],
    }
)

# Bridge from total segment result to loss for the year
BRIDGE = {
    "FY25": [("Other income", 3961.70), ("Share-based payments", -11728.45),
             ("Finance costs", -1005.86), ("Depreciation & amort.", -6122.75),
             ("Exceptional items", -117.01), ("Associate loss", -25.74)],
    "FY24": [("Other income", 3869.59), ("Share-based payments", -5962.62),
             ("Finance costs", -714.03), ("Depreciation & amort.", -4205.85),
             ("Exceptional items", -305.94), ("Associate loss", -66.14)],
}
SEGMENT_RESULT_TOTAL = (-16129.88, -16117.44)

# --------------------------------------------------------------------------
# 5. Operating KPIs, FY22 - FY25  (management KPI pages of the report)
# --------------------------------------------------------------------------
YEARS_KPI = ["FY22", "FY23", "FY24", "FY25"]

KPI = {
    "Food Delivery": {
        "Total orders (million)":               [454.1, 516.9, 577.74, 628.9],
        "GOV (INR Crore)":                      [18479, 21517, 24717, 28783],
        "AOV (INR per order)":                  [407, 416, 428, 458],
        "Gross revenue (INR Crore)":            [4430, 5179, 6082, 7265],
        "Avg monthly transacting users (mn)":   [9.9, 11.6, 12.7, 14.7],
        "Contribution margin (% of GOV)":       [1.6, 2.9, 5.7, 7.1],
        "Adjusted EBITDA (% of GOV)":           [-7.6, -4.8, -0.2, 2.0],
    },
    "Instamart": {
        "Total orders (million)":               [41.7, 128.5, 175.5, 285.5],
        "GOV (INR Crore)":                      [1643, 5118, 8069, 14683],
        "AOV (INR per order)":                  [394, 398, 460, 514],
        "Gross revenue (INR Crore)":            [124, 547, 1088, 2252],
        "Avg monthly transacting users (mn)":   [1.1, 3.2, 4.2, 7.1],
        "Contribution margin (% of GOV)":       [-32.3, -23.5, -6.0, -4.0],
        "Adjusted EBITDA (% of GOV)":           [-53.7, -39.6, -16.2, -14.3],
    },
}

RESTAURANT_PARTNERS_K = [129.0, 174.6, 196.5, 238.1]      # '000, Food Delivery
DARK_STORES_YEARLY    = [301, 421, 523, 1021]             # Instamart, FY22-FY25

DARK_STORE_QTRS = pd.DataFrame(
    {
        "Quarter": ["Q4 FY24", "Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25"],
        "Dark stores": [523, 557, 609, 705, 1021],
        "Area (mn sq ft)": [1.5, 1.7, 1.9, 2.5, 4.0],
    }
)

# B2C GOV mix FY25 (INR Crore). Out-of-home GOV = INR 3,084 Cr (+41% YoY)
B2C_GOV_FY25 = {"Food Delivery": 28783, "Instamart": 14683, "Out-of-home": 3084}

# Group-level snapshot (CEO letter / highlights page)
SNAPSHOT = {
    "B2C GOV (INR Crore)": 46549,
    "B2C orders (million)": 923.31,
    "Avg monthly transacting users (mn)": 17.7,
    "Platform frequency (orders/user/month)": 4.43,
    "Restaurant partners ('000)": 238,
    "Delivery partners ('000)": 515,
    "Active dark stores": 1021,
    "Cities covered": 718,
    "Employees": 7431,
}

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def pnl_table() -> pd.DataFrame:
    rows = {}
    rows.update(INCOME)
    rows["Total income"] = tuple(a + b for a, b in zip(*INCOME.values()))
    rows.update(EXPENSES)
    rows["Total expenses"] = TOTAL_EXPENSES
    rows["Adjusted EBITDA (mgmt.)"] = ADJ_EBITDA
    rows["Loss for the year"] = NET_LOSS
    df = pd.DataFrame(rows, index=YEARS_FIN).T
    df["YoY %"] = (df["FY25"] - df["FY24"]) / df["FY24"].abs() * 100
    return df


def segments_with_margin() -> pd.DataFrame:
    s = SEGMENTS.copy()
    s["Margin FY25 %"] = s["Result FY25"] / s["Revenue FY25"] * 100
    s["Margin FY24 %"] = s["Result FY24"] / s["Revenue FY24"] * 100
    s["Revenue growth %"] = (s["Revenue FY25"] / s["Revenue FY24"] - 1) * 100
    return s


def kpi_frame() -> pd.DataFrame:
    recs = []
    for seg, metrics in KPI.items():
        for metric, vals in metrics.items():
            for yr, v in zip(YEARS_KPI, vals):
                recs.append({"Segment": seg, "Metric": metric, "Year": yr, "Value": v})
    return pd.DataFrame(recs)


def _selfcheck() -> None:
    """Reconcile extracted numbers with totals printed in the report."""
    tot = sum(v[0] for v in EXPENSES.values())
    assert abs(tot - TOTAL_EXPENSES[0]) < 0.05, tot
    tot24 = sum(v[1] for v in EXPENSES.values())
    assert abs(tot24 - TOTAL_EXPENSES[1]) < 0.05, tot24
    for i in (0, 1):
        loss = (INCOME["Revenue from operations"][i] + INCOME["Other income"][i]
                - TOTAL_EXPENSES[i] + ASSOCIATE_LOSS[i] + EXCEPTIONAL[i])
        assert abs(loss - NET_LOSS[i]) < 0.05, (i, loss)
        assert abs(sum(v[i] for v in CASH_FLOW.values()) - NET_CASH_CHANGE[i]) < 0.05
        yr = YEARS_FIN[i]
        assert abs(BALANCE[yr].iloc[:11].sum() - BS_TOTALS["Total assets"][i]) < 0.1
        assert abs(BALANCE[yr].iloc[11:].sum() - BS_TOTALS["Total assets"][i]) < 0.1
        br = SEGMENT_RESULT_TOTAL[i] + sum(v for _, v in BRIDGE[yr])
        assert abs(br - NET_LOSS[i]) < 0.1, (yr, br)
    assert abs(SEGMENTS["Revenue FY25"].sum() - INCOME["Revenue from operations"][0]) < 0.1
    assert abs(SEGMENTS["Revenue FY24"].sum() - INCOME["Revenue from operations"][1]) < 0.1
    for seg, m in KPI.items():
        for a, b, c in zip(m["GOV (INR Crore)"], m["Total orders (million)"], m["AOV (INR per order)"]):
            assert abs(a * 10 / b - c) / c < 0.01, (seg, a, b, c)


if __name__ == "__main__":
    _selfcheck()
    print("All reconciliation checks passed.")
