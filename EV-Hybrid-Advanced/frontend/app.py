import streamlit as st
import requests
import pandas as pd
import json

API_BASE = st.secrets.get("general", {}).get("api_base", "http://127.0.0.1:8000")

st.set_page_config(page_title="EV Hybrid Advanced", layout="wide")

page = st.sidebar.radio("Navigation", ["Dashboard", "History", "About", "Create Admin"], index=0, key="nav_radio")

if "token" not in st.session_state:
    st.session_state.token = None

def login_to_api(username, password):
    try:
        r = requests.post(f"{API_BASE}/login", data={"username": username, "password": password}, timeout=5)
        if r.status_code == 200:
            return r.json()["access_token"]
        else:
            return None
    except Exception as e:
        st.error(f"Login error: {e}")
        return None

if st.session_state.token is None and page != "Create Admin":
    st.title("EV Hybrid System Login")
    username = st.text_input("Username", key="login_user_input")
    password = st.text_input("Password", type="password", key="login_pass_input")
    if st.button("Login", key="login_btn"):
        token = login_to_api(username, password)
        if token:
            st.session_state.token = token
            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid username or password")
    st.stop()

if page == "Dashboard":
    st.title("Dashboard")
    st.write("Enter VIN and telemetry to predict motor status.")

    vin = st.text_input("VIN", "VIN0001", key="dash_vin")
    battery = st.number_input("Battery Level (%)", min_value=0.0, max_value=100.0, value=80.0, key="dash_batt")
    motor_temp = st.number_input("Motor Temperature (°C)", value=60.0, key="dash_temp")
    mileage = st.number_input("Mileage (km)", value=10000.0, key="dash_mileage")
    cycles = st.number_input("Charging Cycles", value=200, step=1, key="dash_cycles")

    if st.button("Predict", key="predict_btn"):
        payload = {
            "vin": vin,
            "battery_level": float(battery),
            "motor_temp": float(motor_temp),
            "mileage": float(mileage),
            "charging_cycles": int(cycles)
        }
        try:
            r = requests.post(f"{API_BASE}/predict", json=payload, timeout=10)
            if r.status_code == 200:
                res = r.json()
                st.success(f"Label: {res['label']} (score: {res['score']})")
            else:
                st.error(f"Prediction failed: {r.text}")
        except Exception as e:
            st.error(f"Request error: {e}")

elif page == "History":
    st.title("Prediction History")
    vin_query = st.text_input("VIN to query", "VIN0001", key="history_vin")
    if st.button("Load History", key="history_load_btn"):
        try:
            r = requests.get(f"{API_BASE}/vehicle/history/{vin_query}", timeout=8)
            if r.status_code == 200:
                data = r.json()
                if not data:
                    st.info("No history found for VIN")
                else:
                    df = pd.json_normalize(data)
                    st.dataframe(df, use_container_width=True)
            else:
                st.error(f"Failed to load: {r.text}")
        except Exception as e:
            st.error(f"Error: {e}")

elif page == "Create Admin":
    st.title("Create Admin Account")
    new_user = st.text_input("Admin username", key="create_user")
    new_pass = st.text_input("Admin password", type="password", key="create_pass")
    full_name = st.text_input("Full name", key="create_fullname")
    if st.button("Create Admin Account", key="create_admin_btn"):
        if not new_user or not new_pass:
            st.error("username and password required")
        else:
            try:
                r = requests.post(f"{API_BASE}/create-admin", data={"username": new_user, "password": new_pass, "full_name": full_name}, timeout=8)
                if r.status_code == 200:
                    st.success("Admin created")
                else:
                    st.error(f"Failed: {r.text}")
            except Exception as e:
                st.error(f"Request error: {e}")

elif page == "About":
    st.title("About EV Hybrid Advanced")
    st.write("Simple demo of a backend + Streamlit frontend for EV motor early fault detection.")
