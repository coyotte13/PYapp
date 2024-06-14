import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import io

# Function to calculate the number of weekdays in a date range
def calculate_weekdays(start_date, end_date, weekdays):
    current_date = start_date
    count = 0
    dates = []
    while current_date <= end_date:
        if current_date.weekday() in weekdays:
            count += 1
            dates.append(current_date)
        current_date += timedelta(days=1)
    return count, dates

# Function to generate a yearly calendar with highlighted dates
def create_yearly_calendar(dates, title):
    fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(20, 15))
    plt.suptitle(title, fontsize=16)
    dates_set = set(dates)
    year_month_pairs = sorted({(date.year, date.month) for date in dates})

    month_pos = {i: (i // 4, i % 4) for i in range(12)}

    for idx, (year, month) in enumerate(year_month_pairs):
        row, col = month_pos[idx]
        ax = axes[row, col]
        cal = calendar.monthcalendar(year, month)
        ax.set_title(f"{calendar.month_name[month]} {year}", fontsize=12)
        ax.axis('off')

        table_data = []
        for week in cal:
            week_data = []
            for day in week:
                if day == 0:
                    week_data.append("")
                elif datetime(year, month, day) in dates_set:
                    week_data.append(f"{day:02d}")
                else:
                    week_data.append(f"{day:02d}")
            table_data.append(week_data)
        
        table = ax.table(cellText=table_data, cellLoc='center', loc='center', colLabels=['L', 'M', 'M', 'J', 'V', 'S', 'D'])
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        for key, cell in table.get_celld().items():
            cell.set_edgecolor('grey')
            if cell.get_text().get_text() in [f"{date.day:02d}" for date in dates_set if date.month == month and date.year == year]:
                cell.set_facecolor('lightblue')
            cell.set_height(0.1)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

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
    session1_days_count, session1_dates = calculate_weekdays(session1_start, session1_end, session1_days_indices)
    session2_days_count, session2_dates = calculate_weekdays(session2_start, session2_end, session2_days_indices)
    total_hours = (session1_days_count + session2_days_count) * hours_per_day

    st.write(f"Nombre de jours de stage dans la première session : {session1_days_count}")
    st.write(f"Nombre de jours de stage dans la deuxième session : {session2_days_count}")
    st.write(f"Nombre total d'heures de stage : {total_hours}")

    # Combine all dates
    all_stage_dates = session1_dates + session2_dates

    # Plot yearly calendar
    fig = create_yearly_calendar(all_stage_dates, 'Calendrier des jours de stage')
    st.pyplot(fig)

    # Export to Excel
    excel_buffer = io.BytesIO()
    all_stage_dates_df = pd.DataFrame(all_stage_dates, columns=['Date'])
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        all_stage_dates_df.to_excel(writer, sheet_name='Stage Calendar')
    st.download_button(
        label="Télécharger le calendrier en Excel",
        data=excel_buffer,
        file_name='stage_calendar.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Export to PDF
    pdf_buffer = io.BytesIO()
    fig.savefig(pdf_buffer, format='pdf')
    st.download_button(
        label="Télécharger le calendrier en PDF",
        data=pdf_buffer,
        file_name='stage_calendar.pdf',
        mime='application/pdf'
    )

# Run this app with the command `streamlit run your_script_name.py`
