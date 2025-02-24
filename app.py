import streamlit as st
import pandas as pd
import datetime

def calculate_bmi(weight, height):
    if height > 0:
        return round(weight / (height ** 2), 2)
    return None

def save_to_txt(data):
    with open("health_data.txt", "a") as file:
        file.write(f"{data}\n")

st.title("🏋️‍♂️ Health Tracker App")
st.sidebar.header("User Input")

date = st.sidebar.date_input("Select Date", datetime.date.today())
steps = st.sidebar.number_input("Enter Steps Walked", min_value=0, value=0)
water_intake = st.sidebar.number_input("Water Intake (Liters)", min_value=0.0, value=0.0, step=0.1)
calories = st.sidebar.number_input("Calories Consumed", min_value=0, value=0)
weight = st.sidebar.number_input("Weight (kg)", min_value=0.0, value=60.0, step=0.1)
height = st.sidebar.number_input("Height (m)", min_value=0.5, value=1.7, step=0.01)

bmi = calculate_bmi(weight, height)

if st.sidebar.button("Save Data"):
    entry = {
        "Date": date,
        "Steps": steps,
        "Water Intake (L)": water_intake,
        "Calories": calories,
        "Weight (kg)": weight,
        "Height (m)": height,
        "BMI": bmi
    }
    st.session_state.setdefault("health_data", []).append(entry)
    save_to_txt(entry)
    st.success("Data Saved Successfully! ✅")

# Show Data
st.subheader("📊 Health Data Log")
if "health_data" in st.session_state and st.session_state["health_data"]:
    df = pd.DataFrame(st.session_state["health_data"])
    st.dataframe(df)
    st.line_chart(df.set_index("Date")["Steps"])  # Show steps trend
else:
    st.info("No data recorded yet.")

# Show BMI
if bmi:
    st.subheader("📌 Your BMI: ")
    st.write(f"### {bmi}")
    if bmi < 18.5:
        st.warning("Underweight 😟")
    elif 18.5 <= bmi < 24.9:
        st.success("Normal Weight ✅")
    elif 25 <= bmi < 29.9:
        st.warning("Overweight ⚠️")
    else:
        st.error("Obese 🚨")
