import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import types

# Load data
@st.cache_data(hash_funcs={types.FunctionType: id})
def load_data():
    day_url = 'https://raw.githubusercontent.com/nikogilang/analisis-data-python/main/Bike-sharing-dataset/day.csv'
    df_day = pd.read_csv(day_url)
    return df_day

df_day = load_data()

# Set page title
st.title("Bike Share Dashboard")

# Display sidebar information
st.sidebar.title("Informasi:")
st.sidebar.markdown("**• Nama: [Nama Anda]**")  # Ganti dengan nama Anda

# Dataset bike share
st.sidebar.title("Dataset Bike Share")
if st.sidebar.checkbox("Tampilkan Dataset"):
    st.subheader("Data Mentah")
    st.write(df_day)

# Display summary statistics
if st.sidebar.checkbox("Tampilkan Statistik Ringkas"):
    st.subheader("Statistik Ringkas")
    st.write(df_day.describe())

# Sidebar visualization options
st.sidebar.title("Pilihan Visualisasi")
visualization_option = st.sidebar.radio("Pilih visualisasi:", ["Penyewaan Sepeda: Hari Kerja vs. Hari Libur",
                                                               "Pengaruh Suhu terhadap Penyewaan Sepeda"])

# Visualisasi Penyewaan Sepeda berdasarkan Hari Kerja dan Hari Libur
if visualization_option == "Penyewaan Sepeda: Hari Kerja vs. Hari Libur":
    st.header("Jumlah Penyewaan Sepeda pada Hari Kerja vs. Hari Libur")
    
    # Data untuk grafik
    data_rentals = {
        'Tipe': ['Hari Kerja', 'Hari Libur'],
        'Jumlah': [df_day[df_day['weekday'].isin([1, 2, 3, 4, 5])]['cnt'].sum(), 
                          df_day[df_day['weekday'].isin([0, 6])]['cnt'].sum()]
    }
    df_rentals = pd.DataFrame(data_rentals)

    # Bar chart
    fig_bar = px.bar(df_rentals, x='Tipe', y='Jumlah', title='Jumlah Penyewaan Sepeda',
                     labels={'Jumlah': 'Jumlah Penyewaan', 'Tipe': 'Tipe Hari'})
    st.plotly_chart(fig_bar)

# Visualisasi Pengaruh Suhu
elif visualization_option == "Pengaruh Suhu terhadap Penyewaan Sepeda":
    st.header("Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda")
    
    # Grafik suhu vs jumlah penyewaan
    fig_line = px.scatter(df_day, x='temp', y='cnt', title='Hubungan Suhu dan Jumlah Penyewaan Sepeda',
                          labels={'temp': 'Suhu (Normalisasi)', 'cnt': 'Jumlah Penyewaan'})
    fig_line.update_traces(marker=dict(size=10, opacity=0.8))
    st.plotly_chart(fig_line)

    # Menambahkan garis tren
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df_day['temp'], y=df_day['cnt'], mode='markers', name='Data Penyewaan'))
    fig_trend.add_trace(go.Scatter(x=df_day['temp'], y=df_day['cnt'].rolling(window=30).mean(), mode='lines', name='Trend'))
    fig_trend.update_layout(title='Hubungan Suhu dan Jumlah Penyewaan Sepeda dengan Trend',
                            xaxis_title='Suhu (Normalisasi)',
                            yaxis_title='Jumlah Penyewaan Sepeda')
    st.plotly_chart(fig_trend)

# Kesimpulan
st.header("Kesimpulan")
st.write("""
1. Penyewaan sepeda pada hari kerja lebih tinggi daripada hari libur.
2. Suhu yang lebih tinggi cenderung meningkatkan jumlah penyewaan sepeda, namun terdapat batas tertentu di mana fluktuasi mulai terjadi, terutama ketika suhu sudah terlalu tinggi atau mendekati ekstrem.
""")
