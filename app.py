import altair as alt
import joblib
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Karachi AirWatch", page_icon="🌫️", layout="centered")

FEATURES = ["aqi", "lag_1", "lag_2", "lag_7", "roll_3", "roll_7", "month"]
API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Bilingual Categories: English + Roman Urdu
CATEGORIES = [
    dict(
        upper=50, name="Good", urdu="Acha", color="#2E9E4F", text="white",
        headline_en="Air quality is clean. Enjoy normal outdoor activities.",
        headline_ur="Hawa saaf hai. Bahar ki sargarmiyan normal rakhein.",
        groups=[
            ("🧑", "General Public / Aam log", "Normal outdoor activities. / Bahar ki sargarmiyan normal."),
            ("🧒", "Children / Bachay", "Safe to play outside. / Bahar khelna bilkul theek."),
            ("👴", "Elderly / Bazurg", "Normal routine. / Normal routine."),
            ("🫁", "Asthma & Heart / Dama o Dil ke mareez", "Normal routine. Keep medicines handy. / Apni dawaiyan saath rakhein."),
        ],
        mask_en="No mask required.",
        mask_ur="Mask ki zaroorat nahi.",
    ),
    dict(
        upper=100, name="Moderate", urdu="Darmiyana", color="#F2C500", text="black",
        headline_en="Air quality is acceptable; very sensitive people should take care.",
        headline_ur="Hawa theek hai, lekin bohat hassas logon ko ehtiyat chahiye.",
        groups=[
            ("🧑", "General Public / Aam log", "Normal routine. / Normal routine."),
            ("🧒", "Children / Bachay", "Can play outside. / Bahar khel sakte hain."),
            ("👴", "Elderly / Bazurg", "Avoid prolonged heavy exertion. / Lambi bahar ki mehnat se bachein."),
            ("🫁", "Asthma & Heart / Dama o Dil ke mareez", "Limit heavy exertion. Keep inhaler/meds. / Lambi mehnat kam karein."),
        ],
        mask_en="Mask not required (optional for sensitive groups).",
        mask_ur="Mask zaroori nahi. Hassas log chahein to pehn sakte hain.",
    ),
    dict(
        upper=150, name="Unhealthy for Sensitive Groups", urdu="Hassas logon ke liye kharab",
        color="#F28C1E", text="black",
        headline_en="Children, elderly, and respiratory patients should limit outdoor time.",
        headline_ur="Bachay, bazurg aur mareez bahar kam jayein.",
        groups=[
            ("🧑", "General Public / Aam log", "Reduce prolonged outdoor exertion. / Bahar lambi mehnat kam karein."),
            ("🧒", "Children / Bachay", "Avoid playing outside for long hours. / Bahar der tak na khelein."),
            ("👴", "Elderly / Bazurg", "Reduce outdoor walks. / Bahar kam jayein."),
            ("🫁", "Asthma & Heart / Dama o Dil ke mareez", "Stay indoors as much as possible. / Bahar kam jayein, dawai saath rakhein."),
        ],
        mask_en="Wearing a mask outdoors is recommended for sensitive groups.",
        mask_ur="Bahar jaate waqt mask pehenna behtar hai.",
    ),
    dict(
        upper=200, name="Unhealthy", urdu="Kharab", color="#D63B3B", text="white",
        headline_en="Air is unhealthy. Everyone should reduce outdoor physical activity.",
        headline_ur="Hawa kharab hai. Sab bahar ki mehnat kam karein.",
        groups=[
            ("🧑", "General Public / Aam log", "Avoid outdoor workouts. / Bahar ki mehnat kam karein."),
            ("🧒", "Children / Bachay", "Play indoors. / Ghar ke andar khelein."),
            ("👴", "Elderly / Bazurg", "Stay indoors. / Ghar mein rahein."),
            ("🫁", "Asthma & Heart / Dama o Dil ke mareez", "Strictly stay indoors. Consult doctor if unwell. / Ghar mein rahein."),
        ],
        mask_en="Wear an N95 / KN95 mask when going outside.",
        mask_ur="Bahar jana ho to achha mask (N95 / KN95) pehnein.",
    ),
    dict(
        upper=300, name="Very Unhealthy", urdu="Bohat kharab", color="#7B3FA0", text="white",
        headline_en="Air is very unhealthy! Avoid going outside.",
        headline_ur="Hawa bohat kharab hai. Bahar jaane se parhez karein.",
        groups=[
            ("🧑", "General Public / Aam log", "Avoid all outdoor exertion. / Bahar ki mehnat bilkul na karein."),
            ("🧒", "Children / Bachay", "Keep strictly indoors. / Ghar mein rakhein."),
            ("👴", "Elderly / Bazurg", "Stay indoors and keep windows closed. / Ghar mein rahein, khidkiyan band rakhein."),
            ("🫁", "Asthma & Heart / Dama o Dil ke mareez", "Stay indoors. Seek medical help if needed. / Tabiyat bigray to doctor se rabta karein."),
        ],
        mask_en="N95 / KN95 mask is mandatory if going outside.",
        mask_ur="Bahar jana zaroori ho to N95 / KN95 mask pehnein.",
    ),
    dict(
        upper=10_000, name="Hazardous", urdu="Khatarnak", color="#7E0023", text="white",
        headline_en="Health Emergency! Air is hazardous. Stay indoors.",
        headline_ur="Hawa khatarnak hai. Bahar na niklein.",
        groups=[
            ("🧑", "General Public / Aam log", "Do not go outside. / Bahar na niklein."),
            ("🧒", "Children / Bachay", "Keep strictly indoors. / Ghar mein rakhein."),
            ("👴", "Elderly / Bazurg", "Stay indoors with closed windows. / Ghar mein rahein, khidkiyan band rakhein."),
            ("🫁", "Asthma & Heart / Dama o Dil ke mareez", "Emergency precaution: Stay indoors. / Foran ehtiyat karein aur ghar mein rahein."),
        ],
        mask_en="Strictly wear an N95 / KN95 respirator mask.",
        mask_ur="Bahar jana ho to N95 / KN95 mask zaroor pehnein.",
    ),
]


def get_category(aqi):
    for cat in CATEGORIES:
        if aqi <= cat["upper"]:
            return cat
    return CATEGORIES[-1]


def build_features(daily):
    d = daily.to_frame(name="aqi")
    d["lag_1"] = d["aqi"].shift(1)
    d["lag_2"] = d["aqi"].shift(2)
    d["lag_7"] = d["aqi"].shift(7)
    d["roll_3"] = d["aqi"].shift(1).rolling(3).mean()
    d["roll_7"] = d["aqi"].shift(1).rolling(7).mean()
    d["month"] = d.index.month
    return d


@st.cache_resource
def load_model():
    return joblib.load("xgb_model.joblib")


@st.cache_data(ttl=3600, show_spinner="Fetching live Karachi AQI data / Taaza data le rahe hain...")
def get_hourly():
    params = {
        "latitude": 24.8607,
        "longitude": 67.0011,
        "hourly": "us_aqi,pm2_5,pm10",
        "past_days": 31,
        "forecast_days": 1,
    }
    r = requests.get(API_URL, params=params, timeout=60)
    r.raise_for_status()
    hourly = pd.DataFrame(r.json()["hourly"])
    hourly["time"] = pd.to_datetime(hourly["time"])
    return hourly


@st.cache_data(show_spinner=False)
def run_backtest():
    raw = pd.read_csv("karachi_aqi_raw.csv", parse_dates=["time"])
    daily = raw.set_index("time")["us_aqi"].resample("D").mean()
    d = build_features(daily)
    d["target"] = d["aqi"].shift(-1)
    d = d.dropna()
    split = int(len(d) * 0.8)
    test = d.iloc[split:].copy()
    test["pred"] = load_model().predict(test[FEATURES])
    model_mae = float((test["pred"] - test["target"]).abs().mean())
    base_mae = float((test["aqi"] - test["target"]).abs().mean())
    return test, model_mae, base_mae


def line_chart(df, x, height=270):
    long = df.melt(x, var_name="Series", value_name="AQI")
    lines = (
        alt.Chart(long)
        .mark_line(strokeWidth=2.5)
        .encode(
            x=alt.X(f"{x}:T", title=None),
            y=alt.Y("AQI:Q", title="US AQI", scale=alt.Scale(zero=False)),
            color=alt.Color("Series:N", legend=alt.Legend(orient="bottom", title=None)),
        )
    )
    rules = (
        alt.Chart(pd.DataFrame({"y": [100, 150]}))
        .mark_rule(strokeDash=[4, 4], opacity=0.35)
        .encode(y="y:Q")
    )
    return (lines + rules).properties(height=height, width="container")


# ----------------------------------------------------------------- Header & Language Selector
col_title, col_lang = st.columns([2.2, 1])
with col_title:
    st.title("🌫️ Karachi AirWatch")
    st.caption("AI-Powered Daily AQI Forecaster | Kal Karachi ki hawa kaisi hogi? Aaj hi pata karo.")
with col_lang:
    lang = st.selectbox(
        "🌐 Language / Zuban",
        ["Both (EN + Urdu)", "English Only", "Roman Urdu Only"],
        index=0,
    )

try:
    model = load_model()
    hourly = get_hourly()
except Exception as e:
    st.error("Could not load data or model. Check internet connection. / Data ya model load nahi ho saka.")
    st.exception(e)
    st.stop()

daily_all = hourly.set_index("time")[["us_aqi", "pm2_5", "pm10"]].resample("D").mean()
daily = daily_all["us_aqi"]
feat = build_features(daily)
latest = feat.iloc[[-1]][FEATURES]

if latest.isna().any(axis=None):
    st.error("Incomplete data for forecast. Please try again later. / Abhi forecast ke liye poora data nahi mila.")
    st.stop()

pred = float(model.predict(latest)[0])
today_aqi = float(latest["aqi"].iloc[0])
pm25 = float(daily_all["pm2_5"].iloc[-1])
pm10 = float(daily_all["pm10"].iloc[-1])
pred_date = latest.index[0] + pd.Timedelta(days=1)
cat = get_category(pred)

# ----------------------------------------------------------------- Sidebar: Interactive What-If Simulator
with st.sidebar:
    st.header("🎛️ 'What-If' AQI Simulator")
    st.caption("Test how the XGBoost model reacts to changing air quality! / Model ko khud test karein!")
    sim_aqi = st.slider("Today's AQI (Aaj ka AQI)", 20.0, 300.0, float(round(today_aqi, 1)))
    sim_lag1 = st.slider("Yesterday's AQI (Kal ka AQI)", 20.0, 300.0, float(round(latest["lag_1"].iloc[0], 1)))
    sim_roll7 = st.slider("7-Day Rolling Avg (7 din ka avg)", 20.0, 300.0, float(round(latest["roll_7"].iloc[0], 1)))
    sim_month = st.selectbox("Month (Mahina)", list(range(1, 13)), index=int(latest["month"].iloc[0]) - 1)

    sim_input = pd.DataFrame([{
        "aqi": sim_aqi,
        "lag_1": sim_lag1,
        "lag_2": float(latest["lag_2"].iloc[0]),
        "lag_7": float(latest["lag_7"].iloc[0]),
        "roll_3": (sim_aqi + sim_lag1 + float(latest["lag_2"].iloc[0])) / 3,
        "roll_7": sim_roll7,
        "month": sim_month,
    }])[FEATURES]
    sim_pred = float(model.predict(sim_input)[0])
    sim_cat = get_category(sim_pred)
    st.markdown("---")
    st.metric("Simulated Next-Day Forecast", f"{sim_pred:.1f} AQI", f"{sim_pred - sim_aqi:+.1f} vs Today")
    st.markdown(f"**Category:** `{sim_cat['name']} ({sim_cat['urdu']})`")

# ----------------------------------------------------------------- Main Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 Forecast (Kal ka andaza)",
    "📈 Trends (Rujhan)",
    "🎯 Accuracy (Model kitna sahi?)",
    "ℹ️ About (Maloomat)"
])

# ----------------------------------------------------------------- Tab 1
with tab1:
    hero = f"""<div style="background:linear-gradient(135deg,{cat['color']},{cat['color']}cc);color:{cat['text']};padding:28px 20px;border-radius:18px;text-align:center;">
<div style="font-size:15px;opacity:.9;">Forecast for {pred_date.strftime('%A, %d %b %Y')} | {pred_date.strftime('%d %b %Y')} ka andaza</div>
<div style="font-size:84px;font-weight:800;line-height:1;margin:6px 0;">{pred:.0f}</div>
<div style="font-size:22px;font-weight:700;">{cat['name']} <span style="font-weight:500;">({cat['urdu']})</span></div>
</div>"""
    st.markdown(hero, unsafe_allow_html=True)

    segs = [(50, "#2E9E4F"), (50, "#F2C500"), (50, "#F28C1E"), (50, "#D63B3B"), (100, "#7B3FA0"), (50, "#7E0023")]
    bar = "".join(f'<div style="flex:{w};background:{c};height:10px;"></div>' for w, c in segs)
    pos = min(pred, 350) / 350 * 100
    scale = (
        f'<div style="position:relative;margin:22px 4px 4px;">'
        f'<div style="display:flex;border-radius:6px;overflow:hidden;">{bar}</div>'
        f'<div style="position:absolute;left:{pos}%;top:-16px;transform:translateX(-50%);font-size:15px;">▼</div></div>'
        f'<div style="display:flex;justify-content:space-between;font-size:12px;opacity:.7;margin:0 4px 8px;">'
        f'<span>Good (Acha)</span><span>Hazardous (Khatarnak)</span></div>'
    )
    st.markdown(scale, unsafe_allow_html=True)

    if lang == "English Only":
        st.info(f"**{cat['headline_en']}**")
    elif lang == "Roman Urdu Only":
        st.info(f"**{cat['headline_ur']}**")
    else:
        st.info(f"**EN:** {cat['headline_en']}\n\n**UR:** {cat['headline_ur']}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Today / Aaj AQI", f"{today_aqi:.0f}")
    c2.metric("Tomorrow / Kal", f"{pred:.0f}", f"{pred - today_aqi:+.0f}", delta_color="inverse")
    c3.metric("PM2.5 (Fine)", f"{pm25:.0f} µg/m³")
    c4.metric("PM10 (Dust)", f"{pm10:.0f} µg/m³")

    st.subheader("Health Advisory / Kis ke liye kya salah hai?")
    cols = st.columns(2)
    for i, (icon, who, advice) in enumerate(cat["groups"]):
        en_adv, ur_adv = advice.split(" / ")
        with cols[i % 2].container(border=True):
            st.markdown(f"**{icon} {who}**")
            if lang == "English Only":
                st.write(en_adv)
            elif lang == "Roman Urdu Only":
                st.write(ur_adv)
            else:
                st.write(f"• {en_adv}\n\n• *{ur_adv}*")

    if lang == "English Only":
        st.warning(f"😷 **Mask Advice:** {cat['mask_en']}")
    elif lang == "Roman Urdu Only":
        st.warning(f"😷 **Mask:** {cat['mask_ur']}")
    else:
        st.warning(f"😷 **Mask:** {cat['mask_en']} | *{cat['mask_ur']}*")

    st.subheader("Share Forecast / Dostoon ko bhejein")
    share = (
        f"🌫️ Karachi AirWatch Forecast ({pred_date.strftime('%d %b %Y')})\n"
        f"Predicted AQI: {pred:.0f} — {cat['name']} ({cat['urdu']})\n"
        f"EN: {cat['headline_en']}\n"
        f"UR: {cat['headline_ur']}\n"
        f"😷 {cat['mask_en']}"
    )
    st.code(share, language=None)

# ----------------------------------------------------------------- Tab 2
with tab2:
    st.subheader("Last 72 Hours (Hourly) / Pichle 3 din, ghante ke hisaab se")
    hr = hourly.tail(72).copy()
    hr["time"] = hr["time"] + pd.Timedelta(hours=5)  # Pakistan Standard Time
    
    # Best & Worst hour in last 24h
    last24 = hr.tail(24)
    best_row = last24.loc[last24["us_aqi"].idxmin()]
    worst_row = last24.loc[last24["us_aqi"].idxmax()]
    b1, b2 = st.columns(2)
    b1.success(f"🌿 **Cleanest Hour (Last 24h):** {best_row['time'].strftime('%I:%M %p')} (AQI: {best_row['us_aqi']:.0f})")
    b2.error(f"⚠️ **Peak Pollution (Last 24h):** {worst_row['time'].strftime('%I:%M %p')} (AQI: {worst_row['us_aqi']:.0f})")

    hr_chart = hr[["time", "us_aqi"]].rename(columns={"us_aqi": "Hourly AQI (Ghante ka AQI)"})
    st.altair_chart(line_chart(hr_chart, "time"))
    st.caption("Time is in PKT (UTC+5). / Waqt Pakistan ke hisaab se hai.")

    st.subheader("Last 30 Days (Daily Avg) / Pichle 30 din, roz ka average")
    dd = daily.tail(30).rename("Daily Avg AQI (Roz ka average)").reset_index()
    st.altair_chart(line_chart(dd, "time"))
    st.caption("Dashed lines show AQI 100 and 150 thresholds. / Dhundli lakeerein AQI 100 aur 150 dikhati hain.")

# ----------------------------------------------------------------- Tab 3
with tab3:
    st.subheader("Historical Backtesting / Model ne purane dino mein kaisa kaam kiya?")
    try:
        test, model_mae, base_mae = run_backtest()
    except Exception:
        st.info("Place 'karachi_aqi_raw.csv' in the app folder to view backtest. / Is hisse ke liye 'karachi_aqi_raw.csv' file folder mein honi chahiye.")
    else:
        gain = (base_mae - model_mae) / base_mae * 100
        m1, m2, m3 = st.columns(3)
        m1.metric("XGBoost MAE (Model ka farq)", f"{model_mae:.2f} AQI")
        m2.metric("Baseline MAE ('Kal = aaj')", f"{base_mae:.2f} AQI")
        m3.metric("Improvement (Behtari)", f"{gain:.1f}%")

        bt = test.tail(60).copy()
        bt["date"] = bt.index + pd.Timedelta(days=1)
        bt_chart = bt[["date", "target", "pred", "aqi"]].rename(
            columns={
                "target": "Actual AQI (Asal AQI)",
                "pred": "XGBoost Forecast (Model ka andaza)",
                "aqi": "Baseline ('Kal = Aaj')",
            }
        )
        st.altair_chart(line_chart(bt_chart, "date", height=300))
        st.write(
            f"**EN:** On 204 unseen test days (March–October 2026), our XGBoost model achieved an average error (MAE) of just **{model_mae:.2f} AQI points**, outperforming the baseline.\n\n"
            f"**UR:** Ye wo din hain jo model ne training mein kabhi nahi dekhe the. Model ka andaza asal AQI se aam tor par sirf **{model_mae:.1f} point** door raha."
        )
        csv_data = bt_chart.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Backtest Predictions (CSV)",
            data=csv_data,
            file_name="karachi_airwatch_backtest.csv",
            mime="text/csv",
        )

# ----------------------------------------------------------------- Tab 4
with tab4:
    st.subheader("How It Works / Ye forecast kaise bana?")
    st.write(
        "**EN:** An **XGBoost Machine Learning model** trained on 3 years of hourly Karachi air quality data (2024–2026, 24,576 records) learns from lag features (yesterday, 2 days ago, 7 days ago), rolling averages (3-day and 7-day), and seasonal month patterns to forecast tomorrow's US AQI. Live data is fetched hourly from the Open-Meteo Air Quality API.\n\n"
        "**UR:** Ek machine learning model (XGBoost) ne Karachi ke 2024 se 2026 tak ke hawa ke data se seekha hai ke pichle dino ki hawa aur mahine ko dekh kar agla din kaisa hoga. Roz taaza data Open-Meteo se liya jata hai."
    )
    st.subheader("Key Notes / Kuch baatein yaad rakhein")
    st.markdown(
        "- **City-wide Average:** Represents Karachi's overall average; local neighborhood AQI may vary. / *Ye poore Karachi ka aam andaza hai.*\n"
        "- **Expected Margin:** Typical daily error is ~5.86 AQI points, though sudden weather changes can cause larger shifts. / *Aam tor par kal ka asal AQI andaze se ~6 point door hota hai.*\n"
        "- **Medical Disclaimer:** For informational guidance only; patients should follow their doctor's advice. / *Ye aam rehnumai hai, doctor ka mashwara nahi.*"
    )
    st.caption("Data: Open-Meteo API | Model: XGBoost Regressor | Developed for University Project Competition")