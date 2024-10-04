import streamlit as st
import pandas as pd
import plotly.express as px

main_data = pd.read_csv("dashboard/main_data.csv")

st.title('Dashboard Analisis Bike Sharing')

st.sidebar.header('Perbandingan')

season_options = ['Spring', 'Summer', 'Fall', 'Winter']
selected_season = st.sidebar.selectbox('Pilih Musim (Season)', options=season_options)

param_options = ['weathersit', 'weekday', 'yr', 'mnth']
selected_param = st.sidebar.selectbox('Pilih Karakteristik Pengguna untuk Visualisasi', param_options)

filtered_data = main_data[main_data['season'] == selected_season]

st.subheader(f'Data untuk Musim {selected_season}')
st.write(filtered_data)

st.subheader(f'Visualisasi untuk {selected_param} di Musim {selected_season}')
if selected_param in ['weathersit', 'weekday', 'yr']:
    chart_data = filtered_data[selected_param].value_counts().reset_index()
    chart_data.columns = [selected_param, 'count']
    fig = px.bar(chart_data, x=selected_param, y='count', title=f'Distribusi {selected_param} di Musim {selected_season}')
else:
    fig = px.histogram(filtered_data, x=selected_param, nbins=20, title=f'Distribusi {selected_param} di Musim {selected_season}')

st.plotly_chart(fig)

year = 2011
filtered_data_2011 = main_data[main_data['yr'] == year]

st.subheader(f'Pengaruh Cuaca Terhadap Penyewaan Sepeda pada Tahun {year}')
weather_rental_data = filtered_data_2011.groupby('weathersit')['cnt_y'].mean().reset_index()

fig1 = px.bar(weather_rental_data, x='weathersit', y='cnt_y', 
              labels={'cnt_y': 'Rata-rata Penyewaan Sepeda', 'weathersit': 'Kondisi Cuaca'},
              title=f'Pengaruh Cuaca terhadap Penyewaan Sepeda di Tahun {year}')
st.plotly_chart(fig1)

st.subheader('Penyewaan Sepeda 10 Terbanyak di Musim Gugur')

fall_data = main_data[main_data['season'] == "Fall"]  

top_10_rental_hours = fall_data.groupby('hr')['cnt_x'].mean().reset_index().nlargest(10, 'cnt_x')

fig2 = px.bar(top_10_rental_hours, x='hr', y='cnt_x', 
              labels={'cnt_x': 'Rata-rata Penyewaan Sepeda', 'hr': 'Jam'}, 
              title='10 Jam dengan Penyewaan Sepeda Terbanyak di Musim Gugur')
st.plotly_chart(fig2)
