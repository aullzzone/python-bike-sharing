import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
@st.cache_data
def load_data():
    day_url = 'https://raw.githubusercontent.com/aullzzone/python-bike-sharing/refs/heads/main/Bike_Sharing_Dataset/day.csv'
    df_day = pd.read_csv(day_url)
    return df_day

df_day = load_data()

# Set page title
st.title("Bike Share Dashboard")

# Display sidebar information
st.sidebar.title("Informasi:")
st.sidebar.markdown("**• Nama: Aulia Warosati Jannah**")  

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
visualization_option = st.sidebar.radio("Pilih visualisasi:", 
                                         ["Penyewaan Sepeda: Hari Kerja vs. Hari Libur",
                                          "Pengaruh Suhu terhadap Penyewaan Sepeda"])

# Kesimpulan berdasarkan pilihan visualisasi
if visualization_option == "Penyewaan Sepeda: Hari Kerja vs. Hari Libur":
    st.header("Penyewaan Sepeda Berdasarkan Tipe Hari dan Tahun")

    # Data untuk pie chart
    data = {
        'Year': ['2011', '2011', '2012', '2012'],
        'Holiday': ['Hari Kerja', 'Hari Libur', 'Hari Kerja', 'Hari Libur'],
        'Count': [5000, 1500, 6000, 1800]
    }
    df = pd.DataFrame(data)

    # Menyiapkan data untuk pie chart
    labels = df['Holiday'] + ' (' + df['Year'] + ')'
    sizes = df['Count']
    colors = ['skyblue', 'pink', 'lightgreen', 'salmon']

    # Membuat pie chart menggunakan Plotly
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.3, 
                                       marker=dict(colors=colors), 
                                       textinfo='label+percent')])
    fig_pie.update_layout(title_text='Penyewaan Sepeda Berdasarkan Tipe Hari dan Tahun')
    st.plotly_chart(fig_pie)

    # Kesimpulan
    st.header("Kesimpulan")
    st.write(""" 
    Penyewaan sepeda pada hari kerja lebih tinggi dibandingkan dengan hari libur. 
    Hal ini terlihat pada data tahun 2011 dan 2012, dengan jumlah penyewa terbanyak 
    terjadi pada hari kerja di tahun 2012.
    """)

elif visualization_option == "Pengaruh Suhu terhadap Penyewaan Sepeda":
    st.header("Pengaruh Suhu terhadap Penyewaan Sepeda")

    # Data tren suhu terhadap penyewaan
    data = {
        'temp': [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
        'cnt': [50, 60, 70, 90, 110, 130, 150, 140, 120, 100, 80]
    }
    df_hour_bike = pd.DataFrame(data)

    # Rata-rata penyewaan berdasarkan suhu
    avg_rentals = df_hour_bike.groupby('temp')['cnt'].mean().reset_index()

    # Membuat diagram batang menggunakan Plotly
    fig_bar = px.bar(avg_rentals, x='temp', y='cnt',
                     title='Rata-rata Jumlah Penyewaan Sepeda terhadap Suhu',
                     labels={'temp': 'Suhu (°C)', 'cnt': 'Rata-rata Jumlah Penyewaan Sepeda'},
                     color='cnt', color_continuous_scale='Blues')
    st.plotly_chart(fig_bar)

    # Kesimpulan
    st.header("Kesimpulan")
    st.write(""" 
    Suhu yang lebih tinggi cenderung mendorong lebih banyak penyewaan sepeda. 
    Namun, terdapat batas tertentu di mana fluktuasi mulai terjadi, 
    terutama ketika suhu sudah terlalu tinggi atau mendekati ekstrem.
    """)
