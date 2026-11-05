"""
Swiggy Financial Dashboard  -  built with Python (Streamlit + Plotly + pandas)
Source: Swiggy Limited Annual Report FY 2024-25 (consolidated numbers).

Run:  streamlit run app.py
"""
import inspect

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

import data as D

# ------------------------------------------------------------------ theme --
ORANGE, DARK, PLUM = "#FC8019", "#3D4152", "#7A1F4B"
GREEN, RED, GREY = "#2E9E5B", "#D64545", "#A9ABB3"
SEG_COLORS = {
    "Food Delivery": ORANGE,
    "Quick Commerce (Instamart)": PLUM,
    "Instamart": PLUM,
    "Out-of-home Consumption": "#F2B33D",
    "Out-of-home": "#F2B33D",
    "Supply Chain & Distribution": DARK,
    "Platform Innovations": GREY,
}

st.set_page_config(page_title="Swiggy Financial Dashboard", page_icon="🛵", layout="wide")

st.markdown(
    f"""
    <style>
      .block-container {{ padding-top: 1.4rem; }}
      div[data-testid="stMetric"] {{
          background: #FFF7F0; border: 1px solid #FFE0C7; border-left: 5px solid {ORANGE};
          padding: 12px 16px; border-radius: 10px;
      }}
      div[data-testid="stMetricLabel"] p {{ font-size: 0.85rem; color: {DARK}; }}
      .hero {{ background: linear-gradient(90deg, {ORANGE} 0%, #FF9E4A 100%);
               padding: 18px 26px; border-radius: 14px; color: white; margin-bottom: 14px; }}
      .hero h1 {{ margin: 0; font-size: 2rem; color: white; }}
      .hero p  {{ margin: 4px 0 0 0; opacity: .95; }}
      .insight {{ background: #F6F7FB; border-left: 4px solid {PLUM}; padding: 10px 14px;
                  border-radius: 6px; margin: 6px 0; color: {DARK}; }}
    </style>
    <div class="hero">
      <h1>🛵 Swiggy Limited - Financial Dashboard</h1>
      <p>Consolidated results, FY 2024-25 vs FY 2023-24 &nbsp;|&nbsp; Source: Annual Report 2024-25</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- helpers --
def show(fig):
    """st.plotly_chart that works across Streamlit versions."""
    fig.update_layout(template="plotly_white", margin=dict(t=50, b=30, l=10, r=10),
                      font=dict(color=DARK))
    if "width" in inspect.signature(st.plotly_chart).parameters:
        st.plotly_chart(fig, width="stretch")
    else:
        st.plotly_chart(fig, use_container_width=True)


def table(df, **kw):
    if "width" in inspect.signature(st.dataframe).parameters:
        st.dataframe(df, width="stretch", **kw)
    else:
        st.dataframe(df, use_container_width=True, **kw)


def insight(text):
    st.markdown(f'<div class="insight">💡 {text}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------- sidebar --
st.sidebar.header("⚙️ Controls")
unit = st.sidebar.radio("Show financials in", ["₹ Crore", "₹ Million"], horizontal=True)
DIV = 10.0 if unit == "₹ Crore" else 1.0
SHORT = "Cr" if unit == "₹ Crore" else "Mn"
year = st.sidebar.radio("Focus year", ["FY25", "FY24"], horizontal=True,
                        help="Used by the waterfall charts and donuts")
kpi_years = st.sidebar.select_slider("Operating KPI range", options=D.YEARS_KPI,
                                     value=(D.YEARS_KPI[0], D.YEARS_KPI[-1]))
st.sidebar.caption("FY25 = year ended 31 Mar 2025. All statement figures are consolidated "
                   "and converted from ₹ Million as printed in the report.")


def conv(v):
    return v / DIV


def money(v, decimals=0):
    sign = "-" if v < 0 else ""
    return f"{sign}₹{abs(conv(v)):,.{decimals}f} {SHORT}"


def pct_change(new, old):
    return (new - old) / abs(old) * 100


YI = 0 if year == "FY25" else 1           # tuple index for the focus year

rev, rev_py = D.INCOME["Revenue from operations"]
exp, exp_py = D.TOTAL_EXPENSES
loss, loss_py = D.NET_LOSS
adj, adj_py = D.ADJ_EBITDA

tabs = st.tabs(["📊 Overview", "🧾 P&L", "🏦 Balance sheet & cash", "🧩 Segments",
                "📈 Operating KPIs", "📁 Data & sources"])

# ================================================================ OVERVIEW ==
with tabs[0]:
    c = st.columns(4)
    c[0].metric("Revenue from operations", money(rev), f"{pct_change(rev, rev_py):+.1f}% YoY")
    c[1].metric("Adjusted EBITDA (mgmt.)", money(adj), f"{money(adj - adj_py)} YoY")
    c[2].metric("Loss for the year", money(loss), f"{money(loss - loss_py)} YoY")
    c[3].metric("Net margin", f"{loss / rev * 100:.1f}%",
                f"{loss / rev * 100 - loss_py / rev_py * 100:+.1f} pp YoY")

    s = D.SNAPSHOT
    c = st.columns(4)
    c[0].metric("B2C GOV (FY25)", f"₹{s['B2C GOV (INR Crore)']:,} Cr", "+33% YoY")
    c[1].metric("B2C orders", f"{s['B2C orders (million)']:.0f} mn")
    c[2].metric("Avg monthly transacting users", f"{s['Avg monthly transacting users (mn)']} mn")
    c[3].metric("Orders / user / month", f"{s['Platform frequency (orders/user/month)']}")

    left, right = st.columns([1, 1])
    with left:
        fig = go.Figure()
        for name, vals, col in [("Revenue", (rev, rev_py), ORANGE),
                                ("Total expenses", (exp, exp_py), DARK),
                                ("Loss for the year", (loss, loss_py), RED)]:
            fig.add_bar(name=name, x=["FY24", "FY25"], y=[conv(vals[1]), conv(vals[0])],
                        marker_color=col, text=[f"{conv(vals[1]):,.0f}", f"{conv(vals[0]):,.0f}"],
                        textposition="outside")
        fig.update_layout(title=f"Revenue vs expenses vs loss ({unit})", barmode="group",
                          legend=dict(orientation="h", y=-0.15))
        show(fig)
    with right:
        # Revenue -> loss waterfall for the focus year
        labels = ["Revenue", "Other income"] + list(D.EXPENSES) + ["Associate & exceptional", "Loss for the year"]
        vals = ([D.INCOME["Revenue from operations"][YI], D.INCOME["Other income"][YI]]
                + [-v[YI] for v in D.EXPENSES.values()]
                + [D.ASSOCIATE_LOSS[YI] + D.EXCEPTIONAL[YI]])
        fig = go.Figure(go.Waterfall(
            x=labels, y=[conv(v) for v in vals] + [0],
            measure=["absolute", "relative"] + ["relative"] * (len(D.EXPENSES) + 1) + ["total"],
            increasing=dict(marker=dict(color=GREEN)), decreasing=dict(marker=dict(color=RED)),
            totals=dict(marker=dict(color=DARK)),
            connector=dict(line=dict(color=GREY)),
        ))
        fig.update_layout(title=f"Where did each rupee go? Revenue to loss, {year} ({unit})",
                          xaxis_tickangle=-35, showlegend=False)
        show(fig)

    # auto-generated insights (numbers computed, not typed)
    cogs, ad, deliv = (D.EXPENSES["Cost of goods & materials"], D.EXPENSES["Advertising & sales promotion"],
                       D.EXPENSES["Delivery & related charges"])
    st.subheader("Key takeaways")
    insight(f"Revenue grew <b>{pct_change(rev, rev_py):.1f}%</b> to {money(rev)}, but total expenses grew "
            f"<b>{pct_change(exp, exp_py):.1f}%</b>, so the loss widened by <b>{pct_change(loss, loss_py):.1f}%</b> "
            f"(net margin {loss / rev * 100:.1f}%).")
    insight(f"Advertising and sales promotion cost {money(ad[0])} (<b>{ad[0] / rev * 100:.1f}%</b> of revenue) and "
            f"delivery charges {money(deliv[0])} (<b>{deliv[0] / rev * 100:.1f}%</b>) - growth is being bought "
            f"through customer acquisition and last-mile logistics.")
    insight(f"Share-based payments were {money(D.SHARE_BASED_PAYMENT[0])}, up "
            f"{pct_change(*D.SHARE_BASED_PAYMENT):.0f}% YoY. This non-cash ESOP charge is excluded from Adjusted "
            f"EBITDA, which explains much of the gap between Adjusted EBITDA ({money(adj)}) and the reported loss.")
    fd = D.segments_with_margin().iloc[0]
    insight(f"Food Delivery turned profitable at segment level ({money(fd['Result FY25'])} vs "
            f"{money(fd['Result FY24'])}), while Quick Commerce is the main drag "
            f"({money(D.SEGMENTS.iloc[1]['Result FY25'])}).")

# ===================================================================== P&L ==
with tabs[1]:
    st.subheader("Consolidated Statement of Profit & Loss")
    pnl = D.pnl_table()
    disp = pnl.copy()
    disp[["FY25", "FY24"]] = disp[["FY25", "FY24"]] / DIV
    disp = disp.rename(columns={"FY25": f"FY25 ({unit})", "FY24": f"FY24 ({unit})"})
    table(disp.style.format({f"FY25 ({unit})": "{:,.1f}", f"FY24 ({unit})": "{:,.1f}", "YoY %": "{:+.1f}%"}))

    c1, c2 = st.columns(2)
    with c1:
        names = list(D.EXPENSES)
        fig = go.Figure()
        for y_i, y_lab in [(1, "FY24"), (0, "FY25")]:
            fig.add_bar(name=y_lab, x=names, y=[D.EXPENSES[n][y_i] / D.INCOME["Revenue from operations"][y_i] * 100
                                                 for n in names],
                        marker_color=GREY if y_lab == "FY24" else ORANGE)
        fig.update_layout(title="Cost structure - each cost as % of revenue", barmode="group",
                          yaxis_title="% of revenue", xaxis_tickangle=-30, legend=dict(orientation="h", y=-0.35))
        show(fig)
    with c2:
        fig = px.pie(names=list(D.EXPENSES), values=[v[YI] for v in D.EXPENSES.values()], hole=0.55,
                     color_discrete_sequence=[DARK, ORANGE, PLUM, "#F2B33D", GREY, "#5B8DEF", RED])
        fig.update_layout(title=f"Expense mix, {year}")
        show(fig)

    # Segment result -> net loss bridge
    labels = ["Segment results"] + [n for n, _ in D.BRIDGE[year]] + ["Loss for the year"]
    vals = [D.SEGMENT_RESULT_TOTAL[YI]] + [v for _, v in D.BRIDGE[year]] + [0]
    fig = go.Figure(go.Waterfall(
        x=labels, y=[conv(v) for v in vals],
        measure=["absolute"] + ["relative"] * len(D.BRIDGE[year]) + ["total"],
        increasing=dict(marker=dict(color=GREEN)), decreasing=dict(marker=dict(color=RED)),
        totals=dict(marker=dict(color=DARK))))
    fig.update_layout(title=f"From segment results to reported loss, {year} ({unit})", showlegend=False)
    show(fig)
    st.caption("Segment results exclude share-based payments, D&A, finance costs, other income and exceptional items.")

# ====================================================== BALANCE SHEET & CASH ==
with tabs[2]:
    bs = D.BS_TOTALS
    cur_ratio = [bs["Total current assets"][i] / bs["Total current liabilities"][i] for i in (0, 1)]
    de = [D.DEBT[i] / bs["Total equity"][i] for i in (0, 1)]
    eq_ratio = [bs["Total equity"][i] / bs["Total assets"][i] * 100 for i in (0, 1)]
    cfo = D.CASH_FLOW["Operating activities"]
    runway = [D.LIQUID_FUNDS[i] / abs(cfo[i]) for i in (0, 1)]

    c = st.columns(5)
    c[0].metric("Total assets", money(bs["Total assets"][0]),
                f"{pct_change(bs['Total assets'][0], bs['Total assets'][1]):+.0f}% YoY")
    c[1].metric("Total equity", money(bs["Total equity"][0]),
                f"{pct_change(bs['Total equity'][0], bs['Total equity'][1]):+.0f}% YoY")
    c[2].metric("Current ratio", f"{cur_ratio[0]:.2f}x", f"{cur_ratio[0] - cur_ratio[1]:+.2f}")
    c[3].metric("Debt* / equity", f"{de[0]:.2f}x", f"{de[0] - de[1]:+.2f}", delta_color="inverse")
    c[4].metric("Liquid funds", money(D.LIQUID_FUNDS[0]),
                f"{pct_change(D.LIQUID_FUNDS[0], D.LIQUID_FUNDS[1]):+.1f}% YoY")
    st.caption("*Debt = borrowings + lease liabilities. Liquid funds = cash + other bank balances + current investments.")

    c1, c2 = st.columns(2)
    with c1:
        b = D.BALANCE
        assets = b.iloc[:11]
        liabs = b.iloc[11:]
        fig = go.Figure()
        pal = px.colors.qualitative.Set3
        for i, (name, row) in enumerate(assets.iterrows()):
            fig.add_bar(name=name, x=["FY24 assets", "FY25 assets"], y=[conv(row["FY24"]), conv(row["FY25"])],
                        marker_color=pal[i % len(pal)], legendgroup="a")
        fig.update_layout(title=f"Asset composition ({unit})", barmode="stack",
                          legend=dict(font=dict(size=10)))
        show(fig)
    with c2:
        fig = go.Figure()
        for name, col in [("Equity", GREEN), ("Non-current liabilities", PLUM),
                          ("Trade payables", ORANGE), ("Other current liabilities", GREY)]:
            fig.add_bar(name=name, x=["FY24", "FY25"],
                        y=[conv(D.BALANCE.loc[name, "FY24"]), conv(D.BALANCE.loc[name, "FY25"])],
                        marker_color=col)
        fig.update_layout(title=f"Funding: equity vs liabilities ({unit})", barmode="stack")
        show(fig)

    st.subheader("Cash flow")
    c1, c2 = st.columns([3, 2])
    with c1:
        fig = go.Figure()
        cats = list(D.CASH_FLOW) + ["Capex (within investing)"]
        for y_i, y_lab, col in [(1, "FY24", GREY), (0, "FY25", ORANGE)]:
            ys = [conv(v[y_i]) for v in D.CASH_FLOW.values()] + [conv(D.CAPEX[y_i])]
            fig.add_bar(name=y_lab, x=cats, y=ys, marker_color=col,
                        text=[f"{v:,.0f}" for v in ys], textposition="outside")
        fig.update_layout(title=f"Cash flow by activity ({unit})", barmode="group",
                          legend=dict(orientation="h", y=-0.2))
        show(fig)
    with c2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=runway[0],
            number=dict(suffix=" yrs", valueformat=".1f"),
            title=dict(text="Cash runway at FY25 operating burn<br><span style='font-size:0.7em'>"
                            "liquid funds ÷ operating cash outflow</span>"),
            delta=dict(reference=runway[1], valueformat=".1f"),
            gauge=dict(axis=dict(range=[0, 5]), bar=dict(color=ORANGE),
                       steps=[dict(range=[0, 1], color="#F8C9C9"), dict(range=[1, 2], color="#FDE7C8"),
                              dict(range=[2, 5], color="#D4EFDF")])))
        fig.update_layout(height=320)
        show(fig)
    insight(f"The company raised {money(D.CASH_FLOW['Financing activities'][0])} in FY25 (IPO and pre-IPO funding) "
            f"to fund an operating cash burn of {money(abs(cfo[0]))} and capex of {money(abs(D.CAPEX[0]))}. "
            f"Operating cash outflow rose {pct_change(abs(cfo[0]), abs(cfo[1])):.0f}% YoY.")
    st.caption("Runway is an illustrative simple ratio (it ignores non-current deposits and future changes in burn), "
               "not a figure from the report.")

# ================================================================ SEGMENTS ==
with tabs[3]:
    seg = D.segments_with_margin()
    picked = st.multiselect("Segments to show", list(seg["Segment"]), default=list(seg["Segment"]))
    sv = seg[seg["Segment"].isin(picked)]
    if sv.empty:
        st.info("Select at least one segment.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            fig.add_bar(name="FY24", x=sv["Segment"], y=sv["Revenue FY24"] / DIV, marker_color=GREY)
            fig.add_bar(name="FY25", x=sv["Segment"], y=sv["Revenue FY25"] / DIV, marker_color=ORANGE)
            fig.update_layout(title=f"Segment revenue ({unit})", barmode="group", xaxis_tickangle=-20,
                              legend=dict(orientation="h", y=-0.3))
            show(fig)
        with c2:
            fig = go.Figure()
            fig.add_bar(name="FY24", x=sv["Segment"], y=sv["Result FY24"] / DIV, marker_color=GREY)
            fig.add_bar(name="FY25", x=sv["Segment"], y=sv["Result FY25"] / DIV, marker_color=PLUM)
            fig.update_layout(title=f"Segment result - profit / (loss) ({unit})", barmode="group",
                              xaxis_tickangle=-20, legend=dict(orientation="h", y=-0.3))
            show(fig)

        c1, c2 = st.columns(2)
        with c1:
            fig = px.treemap(sv, path=["Segment"], values="Revenue FY25", color="Segment",
                             color_discrete_map=SEG_COLORS)
            fig.update_layout(title=f"FY25 revenue mix")
            show(fig)
        with c2:
            fig = go.Figure()
            fig.add_bar(name="FY24", x=sv["Segment"], y=sv["Margin FY24 %"], marker_color=GREY)
            fig.add_bar(name="FY25", x=sv["Segment"], y=sv["Margin FY25 %"], marker_color=ORANGE)
            fig.update_layout(title="Segment margin (result ÷ revenue, %)", barmode="group",
                              xaxis_tickangle=-20, legend=dict(orientation="h", y=-0.3))
            show(fig)

        out = sv.copy()
        for col in ["Revenue FY25", "Revenue FY24", "Result FY25", "Result FY24"]:
            out[col] = out[col] / DIV
        table(out.set_index("Segment").style.format("{:,.1f}"))
        insight("Supply Chain & Distribution is the largest segment by revenue, but it is a low-margin B2B "
                "business - for consumer scale, use GOV on the Operating KPIs tab, which tracks what customers spend.")

# ============================================================= OPERATING KPIs ==
with tabs[4]:
    lo, hi = D.YEARS_KPI.index(kpi_years[0]), D.YEARS_KPI.index(kpi_years[1])
    yrs = D.YEARS_KPI[lo:hi + 1]
    kf = D.kpi_frame()
    kf = kf[kf["Year"].isin(yrs)]

    c1, c2 = st.columns([2, 2])
    metric = c1.selectbox("Metric", list(D.KPI["Food Delivery"].keys()), index=1)
    which = c2.multiselect("Businesses", ["Food Delivery", "Instamart"], default=["Food Delivery", "Instamart"])
    d = kf[(kf["Metric"] == metric) & (kf["Segment"].isin(which))]

    if d.empty or len(yrs) < 2:
        st.info("Pick at least one business and a range of two or more years.")
    else:
        is_pct = "%" in metric
        if is_pct:
            fig = px.line(d, x="Year", y="Value", color="Segment", markers=True, color_discrete_map=SEG_COLORS)
            fig.add_hline(y=0, line_dash="dot", line_color=GREY)
        else:
            fig = px.bar(d, x="Year", y="Value", color="Segment", barmode="group", text_auto=".4g",
                         color_discrete_map=SEG_COLORS)
        fig.update_layout(title=metric, legend=dict(orientation="h", y=-0.2), yaxis_title=None)
        show(fig)

        # CAGR / change cards
        cols = st.columns(len(which))
        for col, seg_name in zip(cols, which):
            v = d[d["Segment"] == seg_name].sort_values("Year")["Value"].tolist()
            if is_pct:
                col.metric(f"{seg_name}: change", f"{v[-1]:+.1f}%", f"{v[-1] - v[0]:+.1f} pp since {yrs[0]}")
            elif v[0] > 0:
                n = len(v) - 1
                cagr = ((v[-1] / v[0]) ** (1 / n) - 1) * 100
                col.metric(f"{seg_name}: {yrs[0]}→{yrs[-1]} CAGR", f"{cagr:.1f}%", f"latest {v[-1]:,.4g}")

    st.subheader("Network & scale")
    c1, c2, c3 = st.columns(3)
    with c1:
        mix = D.B2C_GOV_FY25
        fig = px.pie(names=list(mix), values=list(mix.values()), hole=0.55,
                     color=list(mix), color_discrete_map=SEG_COLORS)
        fig.update_layout(title="FY25 B2C GOV mix (₹ Crore)")
        show(fig)
    with c2:
        fig = go.Figure()
        fig.add_bar(x=D.DARK_STORE_QTRS["Quarter"], y=D.DARK_STORE_QTRS["Dark stores"],
                    name="Dark stores", marker_color=PLUM)
        fig.add_scatter(x=D.DARK_STORE_QTRS["Quarter"], y=D.DARK_STORE_QTRS["Area (mn sq ft)"],
                        name="Area (mn sq ft)", yaxis="y2", mode="lines+markers", line=dict(color=ORANGE))
        fig.update_layout(title="Instamart dark-store footprint", legend=dict(orientation="h", y=-0.25),
                          yaxis2=dict(overlaying="y", side="right", showgrid=False))
        show(fig)
    with c3:
        fig = go.Figure(go.Scatter(x=D.YEARS_KPI, y=D.RESTAURANT_PARTNERS_K, mode="lines+markers+text",
                                   text=[f"{v:.0f}k" for v in D.RESTAURANT_PARTNERS_K], textposition="top center",
                                   line=dict(color=ORANGE)))
        fig.update_layout(title="Avg monthly transacting restaurant partners ('000)")
        show(fig)

    s = D.SNAPSHOT
    c = st.columns(4)
    dp = s["Delivery partners ('000)"]
    c[0].metric("Delivery partners", f"{dp}k")
    c[1].metric("Cities covered", f"{s['Cities covered']}")
    c[2].metric("Active dark stores", f"{s['Active dark stores']:,}")
    c[3].metric("Employees", f"{s['Employees']:,}")

# ============================================================ DATA & SOURCES ==
with tabs[5]:
    st.subheader("All extracted data")
    st.write("Every number in this dashboard comes from the Swiggy Annual Report 2024-25. "
             "`data.py` contains a self-check that reconciles the figures with the totals printed in the report.")
    sets = {
        "P&L (₹ Million)": D.pnl_table().reset_index().rename(columns={"index": "Line item"}),
        "Balance sheet (₹ Million)": D.BALANCE.reset_index().rename(columns={"index": "Line item"}),
        "Segments (₹ Million)": D.segments_with_margin(),
        "Operating KPIs FY22-FY25": D.kpi_frame(),
    }
    for name, df in sets.items():
        with st.expander(name):
            table(df)
            st.download_button(f"Download {name} as CSV", df.to_csv(index=False).encode("utf-8"),
                               file_name=name.split(" (")[0].lower().replace(" ", "_") + ".csv",
                               mime="text/csv", key=f"dl_{name}")
    st.markdown(
        """
        **Where it comes from (PDF page numbers of the uploaded file):** Consolidated Balance Sheet p.103 ·
        Statement of Profit & Loss p.104 · Statement of Cash Flows pp.105-106 · Operating segments note p.131 ·
        Management KPI charts (Food Delivery, Instamart) in the Corporate Overview, e.g. p.18 for Instamart.

        **Definitions:** *GOV* = gross order value at MRP/menu price; *AOV* = GOV ÷ orders;
        *Contribution margin* and *Adjusted EBITDA* are management-defined measures (Adjusted EBITDA excludes
        share-based payments, other income and ex-IND-AS-116 lease effects) and are not audited IND AS figures.

        *Educational project - not investment advice.*
        """
    )
