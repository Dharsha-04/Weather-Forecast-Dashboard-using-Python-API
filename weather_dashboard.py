import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geocoder

# PAGE SETTINGS

st.set_page_config(page_title="Weather Dashboard", page_icon="🌦️", layout="wide")

st.title("🌦️ Weather Forecast Dashboard")

# API KEY

API_KEY = "5f75a68559e64301ef1cfa4dc0607cf2"

# AUTO LOCATION

g = geocoder.ip('me')
auto_city = g.city

# USER INPUT

st.sidebar.header("🔎 Search City")

city = st.sidebar.text_input("Enter City Name", auto_city)

get_data = st.sidebar.button("Get Weather Data")

# FUNCTION TO FETCH DATA

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] != "200":
        st.error("❌ City not found. Try again.")
        return None
    
    dates, temps, conditions = [], [], []
    
    for item in data["list"]:
        dates.append(item["dt_txt"])
        temps.append(item["main"]["temp"])
        conditions.append(item["weather"][0]["main"])
    
    df = pd.DataFrame({
        "Date": dates,
        "Temperature": temps,
        "Condition": conditions
    })
    
    return df

# MAIN DISPLAY

if get_data:
    df = fetch_weather(city)
    
    if df is not None:
        st.success(f"📍 Showing weather for: {city}")

        
# SHOW DATA TABLE

        st.subheader("📋 Forecast Data")
        st.dataframe(df)

# DOWNLOAD CSV
    
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download CSV", csv, "weather_data.csv", "text/csv")

# LINE CHART

        st.subheader("🌈 Temperature Trend")

        fig1, ax1 = plt.subplots(figsize=(10,4))
        ax1.plot(df["Date"], df["Temperature"], marker='o')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig1)

# PIE CHART

        st.subheader("📊 Weather Distribution")

        condition_counts = df["Condition"].value_counts()

        fig2, ax2 = plt.subplots()
        ax2.pie(condition_counts, labels=condition_counts.index, autopct='%1.1f%%')
        st.pyplot(fig2)