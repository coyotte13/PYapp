import streamlit as st
from datetime import datetime, timedelta

# Function to calculate the number of weekdays in a date range
def calculate_weekdays(start_date, end_date, weekdays):
    current_date = start_date
    count = 0
    while current_date <= end_date:
        if current_date.weekday() in weekdays:
            count += 1
        current_date += timedelta(days=1)
    return count

st.title("Calculateur d'heures de stage")

# Input for session 1
st.header("Session 1")
session1_start = st.date_input("Date de début de la première session", datetime(2024, 9, 1))
session1_end = st.date_input("Date de fin de la première session", datetime(2024, 12, 20))
session1_days = st.multiselect("Jours de stage pour la première session", ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'], ['Lundi', 'Mardi', 'Mercredi'])
session1_days_indices = [i for i, day in enumerate(['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']) if day in session1_days]

# Input for session 2
st.header("Session 2")
session2_start = st.date_input("Date de début de la deuxième session", datetime(2025, 1, 5))
session2_end = st.date_input("Date de fin de la deuxième session", datetime(2025, 6, 30))
session2_days = st.multiselect("Jours de stage pour la deuxième session", ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'], ['Jeudi'])
session2_days_indices = [i for i, day in enumerate(['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']) if day in session2_days]

# Input for hours per day
hours_per_day = st.number_input("Nombre d'heures par jour de stage", min_value=1, max_value=24, value=7)

if st.button("Calculer le total des heures de stage"):
    session1_days_count = calculate_weekdays(session1_start, session1_end, session1_days_indices)
    session2_days_count = calculate_weekdays(session2_start, session2_end, session2_days_indices)
    total_hours = (session1_days_count + session2_days_count) * hours_per_day

    st.write(f"Nombre de jours de stage dans la première session : {session1_days_count}")
    st.write(f"Nombre de jours de stage dans la deuxième session : {session2_days_count}")
    st.write(f"Nombre total d'heures de stage : {total_hours}")

# Run this app with the command `streamlit run your_script_name.py`

