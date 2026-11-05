# 🛵 Swiggy Financial Dashboard

An interactive financial dashboard for **Swiggy Limited**, built entirely in **Python**
(Streamlit + Plotly + pandas). All numbers are extracted from the
**Swiggy Annual Report FY 2024-25** (consolidated figures).

## What it shows

| Tab | Contents |
|---|---|
| **Overview** | Headline KPI cards (revenue, adjusted EBITDA, loss, B2C GOV, orders, users), revenue-vs-loss chart, revenue-to-loss waterfall, auto-generated takeaways |
| **P&L** | Full P&L table with YoY %, cost structure (% of revenue), expense mix, segment-result-to-net-loss bridge |
| **Balance sheet & cash** | Current ratio, debt/equity, liquid funds, asset & funding composition, cash flow by activity, cash-runway gauge |
| **Segments** | Revenue, results and margins for Food Delivery, Instamart, Out-of-home, Supply Chain & Distribution, Platform Innovations |
| **Operating KPIs** | FY22-FY25 trends for orders, GOV, AOV, MTUs, contribution margin and adjusted EBITDA (Food Delivery vs Instamart), dark-store footprint |
| **Data & sources** | Every dataset with CSV download and PDF page references |

Sidebar controls: ₹ Crore / ₹ Million, focus year, KPI year range. Charts are also
interactive (hover, zoom, click legend items to hide series).

## Run it locally

```bash
git clone <your-repo-url>
cd swiggy-dashboard
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

It opens at http://localhost:8501.

## Put it on GitHub

```bash
git init
git add .
git commit -m "Swiggy financial dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/swiggy-dashboard.git
git push -u origin main
```

**Free live link for your class:** go to https://share.streamlit.io, sign in with GitHub, choose this
repo, set the main file to `app.py`, and deploy. Add the URL to this README.

## Project structure

```
app.py            # the dashboard (layout, charts, KPI cards)
data.py           # all extracted data + a self-check that reconciles totals to the report
requirements.txt
.streamlit/config.toml   # Swiggy-orange theme
```

Run `python data.py` to verify the extracted numbers still add up
(P&L, balance sheet, cash flow, segment bridge).

## Data notes

* Statement figures are in ₹ Million as printed; the dashboard converts to ₹ Crore (÷10).
* *Adjusted EBITDA*, *contribution margin*, *GOV* and *AOV* are management-defined metrics, not audited Ind AS figures.
* "Cash runway" and the ratios on the Balance sheet tab are simple calculations by the author, not figures from the report.
* Educational project, not investment advice.
