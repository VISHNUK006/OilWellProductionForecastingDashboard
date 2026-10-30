import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Oil Well Production Forecasting Dashboard", page_icon="🛢️", layout="wide")
st.title("🛢️ Oil Well Production Forecasting Dashboard")
st.caption("Historical production analysis, decline-trend assessment, and short-term forecasting")

@st.cache_data
def load_data():
    return pd.read_csv("data/sample_production.csv", parse_dates=["date"]).sort_values(["well", "date"])

df = load_data()

st.sidebar.header("Controls")
wells = sorted(df["well"].unique())
selected = st.sidebar.multiselect("Select wells", wells, default=wells)
horizon = st.sidebar.slider("Forecast horizon (months)", 3, 24, 12)

if not selected:
    st.warning("Select at least one well.")
    st.stop()

filtered = df[df["well"].isin(selected)].copy()
latest = filtered[filtered["date"] == filtered["date"].max()]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Latest Oil Rate", f"{latest['oil_bbl_day'].mean():,.0f} bbl/day")
c2.metric("Latest Gas Rate", f"{latest['gas_mscf_day'].mean():,.0f} Mscf/day")
c3.metric("Avg. Water Cut", f"{latest['water_cut_pct'].mean():.1f}%")
c4.metric("Avg. Uptime", f"{latest['uptime_pct'].mean():.1f}%")

st.subheader("Historical Oil Production")
fig = px.line(filtered, x="date", y="oil_bbl_day", color="well",
              labels={"oil_bbl_day":"Oil rate (bbl/day)", "date":"Date"})
st.plotly_chart(fig, use_container_width=True)

def forecast_well(well_df, horizon):
    x = well_df.sort_values("date").copy()
    x["t"] = np.arange(len(x))
    x = x[x["oil_bbl_day"] > 0]
    model = LinearRegression().fit(x[["t"]], np.log(x["oil_bbl_day"]))
    future_t = np.arange(len(x), len(x) + horizon)
    pred = np.exp(model.predict(future_t.reshape(-1, 1)))
    decline = (1 - np.exp(model.coef_[0])) * 100
    future_dates = pd.date_range(
        well_df["date"].max() + pd.offsets.MonthBegin(1),
        periods=horizon, freq="MS"
    )
    hist = well_df[["date","well","oil_bbl_day"]].copy()
    hist["type"] = "Historical"
    fc = pd.DataFrame({
        "date": future_dates, "well": well_df["well"].iloc[0],
        "oil_bbl_day": pred, "type": "Forecast"
    })
    return hist, fc, decline

hist_parts, fc_parts, decline_rows = [], [], []
for well in selected:
    h, f, d = forecast_well(df[df["well"] == well], horizon)
    hist_parts.append(h)
    fc_parts.append(f)
    decline_rows.append({"well": well, "estimated_monthly_decline_pct": round(d, 2)})

combined = pd.concat(hist_parts + fc_parts, ignore_index=True)

st.subheader("Production Forecast")
fig2 = px.line(combined, x="date", y="oil_bbl_day", color="well", line_dash="type",
               labels={"oil_bbl_day":"Oil rate (bbl/day)", "date":"Date"})
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Estimated Decline Indicators")
st.dataframe(pd.DataFrame(decline_rows), use_container_width=True, hide_index=True)

st.subheader("Water-Cut Trend")
fig3 = px.line(filtered, x="date", y="water_cut_pct", color="well",
               labels={"water_cut_pct":"Water cut (%)", "date":"Date"})
st.plotly_chart(fig3, use_container_width=True)

with st.expander("View production data"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)

st.info("Demo uses synthetic data. The forecast is an exponential-decline baseline and should be calibrated with real field, reservoir, and operational data before engineering use.")
