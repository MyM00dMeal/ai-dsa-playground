# import streamlit as st
# import requests
# import random
# from datetime import datetime, timezone
# import pandas as pd
# from streamlit_autorefresh import st_autorefresh

# # ------------------ CONFIG ------------------

# API_URL = "http://localhost:8000"
# REQUEST_TIMEOUT = 3  # seconds

# # ------------------ PAGE CONFIG ------------------
# st.set_page_config(
#     page_title="AI API Usage Monitor",
#     layout="wide",
# )

# st.title("AI API Usage Monitor")

# # ------------------ AUTO REFRESH ------------------
# st_autorefresh(interval=5000, key="data_refresh")  # 5 seconds

# # ------------------ SIDEBAR: LOG SIMULATOR ------------------
# st.sidebar.header(" Log Simulator")

# if st.sidebar.button("Generate Logs"):
#     for _ in range(30):
#         log = {
#             "timestamp": datetime.now(timezone.utc).isoformat(),
#             "user_id": random.choice(["alice", "bob", "carol"]),
#             "latency_ms": random.randint(100, 2000),
#             "tokens_used": random.randint(100, 3000),
#             "is_error": random.random() < 0.1,
#         }

#         try:
#             requests.post(
#                 f"{API_URL}/ingest",
#                 json=log,
#                 timeout=REQUEST_TIMEOUT,
#             )
#         except requests.RequestException:
#             st.sidebar.error("Failed to send logs")
#             break

#     st.sidebar.success("Logs sent successfully!")

# # ------------------ FETCH METRICS ------------------
# try:
#     response = requests.get(
#         f"{API_URL}/metrics",
#         timeout=REQUEST_TIMEOUT,
#     )
#     response.raise_for_status()
#     data = response.json()
# except requests.RequestException:
#     st.error(" Backend not reachable. Start FastAPI server.")
#     st.stop()

# # ------------------ KPI METRICS ------------------
# st.subheader(" Real-Time Metrics")

# c1, c2, c3, c4 = st.columns(4)
# c1.metric("Requests / Min", data["requests_per_min"])
# c2.metric("Avg Latency (ms)", f"{data['avg_latency']:.1f}")
# c3.metric("Error Rate", f"{data['error_rate'] * 100:.1f}%")
# c4.metric("Estimated Cost ($)", f"{data['estimated_cost_usd']:.4f}")

# # ------------------ LATENCY PERCENTILES ------------------
# st.subheader(" Latency Percentiles")

# p1, p2, p3 = st.columns(3)
# p1.metric("P50 (Median)", f"{data['p50_latency']:.1f} ms")
# p2.metric("P95", f"{data['p95_latency']:.1f} ms")
# p3.metric("P99", f"{data['p99_latency']:.1f} ms")

# # ------------------ PER USER USAGE ------------------
# st.subheader(" Per-User Request Distribution")

# user_df = pd.DataFrame.from_dict(
#     data["per_user_requests"],
#     orient="index",
#     columns=["Requests"]
# ).sort_values("Requests", ascending=False)

# st.bar_chart(user_df)

# # ------------------ ANOMALIES ------------------
# st.subheader(" Detected Anomalies")

# if data["anomalies"]:
#     for anomaly in data["anomalies"]:
#         if anomaly.startswith("CRITICAL"):
#             st.error(anomaly)
#         else:
#             st.warning(anomaly)
# else:
#     st.success("No anomalies detected")

# # ------------------ FOOTER ------------------
# st.caption("🔁 Dashboard auto-refreshes every 5 seconds")





# import streamlit as st
# import requests
# import random
# from datetime import datetime, timezone
# import pandas as pd
# from streamlit_autorefresh import st_autorefresh

# # ------------------ CONFIG ------------------
# API_URL = "http://localhost:8000"
# REQUEST_TIMEOUT = 3 

# # ------------------ PAGE CONFIG ------------------
# st.set_page_config(
#     page_title="AI API Real-Time Monitor",
#     page_icon="📊",
#     layout="wide",
# )

# # ------------------ CUSTOM STYLING ------------------
# st.markdown("""
#     <style>
#     .main { background-color: #0e1117; }
#     div[data-testid="stMetric"] {
#         background-color: #1a1c24;
#         border: 1px solid #2d2e35;
#         padding: 15px;
#         border-radius: 10px;
#     }
#     h1, h2, h3 { color: #ffffff !important; }
#     section[data-testid="stSidebar"] { background-color: #161b22; }
#     </style>
#     """, unsafe_allow_html=True)

# # ------------------ AUTO REFRESH (5 Seconds) ------------------
# st_autorefresh(interval=5000, key="data_refresh")

# # ------------------ SIDEBAR ------------------
# with st.sidebar:
#     st.title("⚙️ Settings")
#     stream_active = st.toggle("Start/Stop Stream", value=True)
    
#     st.slider("Latency Threshold (k)", 0.5, 3.0, 1.5)
#     st.slider("Error Rate Threshold", 0.01, 0.10, 0.05)
    
#     st.divider()
#     if st.button("Generate Synthetic Logs", use_container_width=True):
#         for _ in range(20):
#             log = {
#                 "timestamp": datetime.now(timezone.utc).isoformat(),
#                 "user_id": random.choice(["user_007", "user_123", "user_045"]),
#                 "latency_ms": random.randint(50, 600),
#                 "tokens_used": random.randint(100, 4000),
#                 "is_error": random.random() < 0.05,
#             }
#             try:
#                 requests.post(f"{API_URL}/ingest", json=log, timeout=REQUEST_TIMEOUT)
#             except:
#                 pass
#         st.sidebar.success("Logs sent!")

# # ------------------ DATA FETCHING ------------------
# try:
#     response = requests.get(f"{API_URL}/metrics", timeout=REQUEST_TIMEOUT)
#     data = response.json()
# except:
#     st.error("Backend unreachable. Please ensure FastAPI is running.")
#     st.stop()

# # ------------------ HEADER ------------------
# st.title("AI API Real-Time Monitor")

# # ------------------ TOP ROW: KPI CARDS ------------------
# with st.container():
#     c1, c2, c3 = st.columns(3)
#     with c1:
#         val = data.get('requests_per_min', 0)
#         st.metric(label="Throughput", value=f"{val:,} RPM")
#     with c2:
#         err = data.get('error_rate', 0.0)
#         st.metric(label="Error Rate", value=f"{err * 100:.2f}%", delta_color="inverse")
#     with c3:
#         cost = data.get('estimated_cost_usd', 0.0)
#         st.metric(label="Cost (Est)", value=f"${cost:.3f} USD")

# st.markdown("---")

# # ------------------ MIDDLE ROW: CHARTS ------------------
# col_left, col_right = st.columns([1.5, 1])

# with col_left:
#     st.subheader("Latency Percentiles (ms)")
#     chart_data = pd.DataFrame({
#         "Metric": ["P50", "P95", "P99"],
#         "Latency": [
#             data.get('p50_latency', 0), 
#             data.get('p95_latency', 0), 
#             data.get('p99_latency', 0)
#         ]
#     }).set_index("Metric")
#     st.area_chart(chart_data, height=250)

# with col_right:
#     st.subheader("Top Users by Requests")
#     user_counts = data.get("per_user_requests", {})
#     if user_counts:
#         user_df = pd.DataFrame.from_dict(user_counts, orient="index", columns=["Count"])
#         user_df = user_df.sort_values("Count", ascending=True).tail(5)
#         st.bar_chart(user_df, horizontal=True, height=250, color="#29b5e8")
#     else:
#         st.info("No active users in current window.")

# # ------------------ BOTTOM ROW: ALERTS ------------------
# st.subheader("⚠️ Active Alerts")
# alert_container = st.container(border=True) # THIS WAS MISSING

# with alert_container:
#     anomalies = data.get("anomalies", [])
#     if anomalies:
#         for anomaly in anomalies:
#             if "CRITICAL" in anomaly.upper():
#                 st.error(f"🔴 {anomaly}")
#             else:
#                 st.warning(f"🟡 {anomaly}")
#     else:
#         st.success("✅ All systems nominal. No anomalies detected.")

# # ------------------ FOOTER ------------------
# st.write(f"<p style='text-align: right; color: gray;'>Last updated: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)






import streamlit as st
import requests
import random
from datetime import datetime, timezone
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ------------------ CONFIG ------------------
API_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 3 

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI API Real-Time Monitor",
    page_icon="📊",
    layout="wide",
)

# ------------------ CUSTOM STYLING (Professional Dark Mode) ------------------
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background-color: #1a1c24;
        border: 1px solid #2d2e35;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    h1, h2, h3 { color: #ffffff !important; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #161b22; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ------------------ SESSION STATE (Persistent History) ------------------
# This stores past events so the graphs have data even when the backend window resets
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Time", "Throughput", "ErrorRate"])

# ------------------ AUTO REFRESH ------------------
st_autorefresh(interval=5000, key="data_refresh")

# ------------------ SIDEBAR: LOG SIMULATOR ------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.title("Settings")
    
    stream_active = st.toggle("Live Stream Simulation", value=True)
    k_threshold = st.slider("Anomaly Sensitivity (k)", 0.5, 3.0, 1.5)
    
    st.divider()
    if st.button("🚀 Generate Burst Logs", use_container_width=True):
        for _ in range(30):
            log = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "user_id": random.choice(["alice_001", "bob_002", "charlie_003"]),
                "latency_ms": random.randint(100, 1500),
                "tokens_used": random.randint(50, 2000),
                "is_error": random.random() < 0.08,
            }
            try:
                requests.post(f"{API_URL}/ingest", json=log, timeout=1)
            except:
                pass
        st.sidebar.success("Burst sent to API!")

# ------------------ DATA FETCHING ------------------
try:
    response = requests.get(f"{API_URL}/metrics", timeout=REQUEST_TIMEOUT)
    data = response.json()
    
    # Update History Dataframe
    new_entry = {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Throughput": data.get('requests_per_min', 0),
        "ErrorRate": data.get('error_rate', 0.0) * 100
    }
    st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_entry])], ignore_index=True)
    st.session_state.history = st.session_state.history.tail(20) # Keep last 20 snapshots

except Exception as e:
    st.error("⚠️ Backend unreachable. Ensure FastAPI server is running.")
    st.stop()

# ------------------ MAIN UI ------------------
st.title("AI API Real-Time Monitor")

# --- TOP ROW: KPI CARDS ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Throughput", f"{data.get('requests_per_min', 0)} RPM")
    with c2:
        err = data.get('error_rate', 0.0)
        st.metric("Error Rate", f"{err*100:.1f}%", delta_color="inverse")
    with c3:
        st.metric("P95 Latency", f"{data.get('p95_latency', 0):.0f} ms")
    with c4:
        st.metric("Est. Cost", f"${data.get('estimated_cost_usd', 0.0):.4f}")

st.markdown("---")

# --- MIDDLE ROW: PERFORMANCE TRENDS ---
st.subheader("📈 Performance Trends")
t_col1, t_col2 = st.columns(2)

with t_col1:
    st.write("**Throughput (Requests/Min)**")
    st.area_chart(st.session_state.history.set_index("Time")["Throughput"], color="#29b5e8")

with t_col2:
    st.write("**Error Rate (%)**")
    st.line_chart(st.session_state.history.set_index("Time")["ErrorRate"], color="#ff4b4b")

# --- BOTTOM ROW: DISTRIBUTION ---
st.markdown("---")
col_l, col_r = st.columns([1, 1])

with col_l:
    st.subheader("⏱️ Latency Percentiles")
    lat_data = pd.DataFrame({
        "Level": ["P50", "P95", "P99"],
        "ms": [data.get('p50_latency', 0), data.get('p95_latency', 0), data.get('p99_latency', 0)]
    }).set_index("Level")
    st.bar_chart(lat_data, color="#7f00ff")

with col_r:
    st.subheader("👥 User Distribution")
    user_counts = data.get("per_user_requests", {})
    if user_counts:
        user_df = pd.DataFrame.from_dict(user_counts, orient="index", columns=["Requests"])
        st.bar_chart(user_df.sort_values("Requests"), horizontal=True, color="#29b5e8")
    else:
        st.info("No active user data in window.")

# --- FOOTER: ALERTS ---
st.markdown("---")
st.subheader("⚠️ Incident Log")
alert_box = st.container(border=True)
with alert_box:
    anomalies = data.get("anomalies", [])
    if anomalies:
        for alert in anomalies:
            if "CRITICAL" in alert.upper():
                st.error(f"🔴 {alert}")
            else:
                st.warning(f"🟡 {alert}")
    else:
        st.success("✅ All systems nominal. No anomalies detected.")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")